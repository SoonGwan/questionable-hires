import Foundation
import Virtualization

final class Lifecycle: NSObject, VZVirtualMachineDelegate {
    func guestDidStop(_ virtualMachine: VZVirtualMachine) {
        print("QH_VM_GUEST_STOPPED")
        exit(0)
    }
    func virtualMachine(_ virtualMachine: VZVirtualMachine, didStopWithError error: Error) {
        print("QH_VM_ERROR \(error)")
        exit(1)
    }
}
let directory = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
let config = VZVirtualMachineConfiguration()
config.cpuCount = 1
config.memorySize = 1024 * 1024 * 1024
let loader = VZLinuxBootLoader(kernelURL: directory.appendingPathComponent("vmlinuz-virt"))
loader.initialRamdiskURL = directory.appendingPathComponent("initramfs-virt")
loader.commandLine = "console=hvc0 rdinit=/bin/sh panic=-1"
config.bootLoader = loader
config.entropyDevices = [VZVirtioEntropyDeviceConfiguration()]
let input = Pipe()
let console = VZVirtioConsoleDeviceSerialPortConfiguration()
console.attachment = VZFileHandleSerialPortAttachment(fileHandleForReading: input.fileHandleForReading, fileHandleForWriting: .standardOutput)
config.serialPorts = [console]
let translation = VZVirtioFileSystemDeviceConfiguration(tag: "rosetta")
translation.share = try VZLinuxRosettaDirectoryShare()
let layers = VZVirtioFileSystemDeviceConfiguration(tag: "layers")
layers.share = VZSingleDirectoryShare(directory: VZSharedDirectory(url: directory.appendingPathComponent("layers"), readOnly: true))
let root = VZVirtioFileSystemDeviceConfiguration(tag: "root")
root.share = VZSingleDirectoryShare(directory: VZSharedDirectory(url: directory.appendingPathComponent("root-mount"), readOnly: false))
config.directorySharingDevices = [translation, layers, root]
try config.validate()
let lifecycle = Lifecycle()
let machine = VZVirtualMachine(configuration: config)
machine.delegate = lifecycle
machine.start { result in
    switch result {
    case .success:
        print("QH_VM_STARTED")
        DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
            let commands = """
            /bin/busybox mount -t proc proc /proc
            /bin/busybox mount -t sysfs sysfs /sys
            /bin/busybox modprobe virtiofs
            /bin/busybox mkdir -p /ownedroot
            /bin/busybox mount -t virtiofs root /ownedroot
            /bin/busybox mkdir -p /ownedroot/_qh_probe_01/layers /ownedroot/_qh_probe_01/rosetta
            /bin/busybox mount -t virtiofs layers /ownedroot/_qh_probe_01/layers
            /bin/busybox mount -t virtiofs rosetta /ownedroot/_qh_probe_01/rosetta
            /bin/busybox cp /bin/busybox /ownedroot/_qh_probe_01/busybox
            /bin/busybox cp -L /lib/ld-musl-aarch64.so.1 /ownedroot/_qh_probe_01/ld-musl-aarch64.so.1
            QH_APPLIED=0
            for QH_LAYER in 0 1 2 3 4 5 6 7 8 9; do /bin/busybox chroot /ownedroot /_qh_probe_01/ld-musl-aarch64.so.1 /_qh_probe_01/busybox tar -xzf /_qh_probe_01/layers/$QH_LAYER.tar.gz -C /; QH_STATUS=$?; echo QH_LAYER_${QH_LAYER}_EXIT=$QH_STATUS; if [ $QH_STATUS -ne 0 ]; then break; fi; QH_APPLIED=$((QH_APPLIED+1)); done
            echo QH_APPLIED=$QH_APPLIED
            if [ $QH_APPLIED -eq 10 ]; then /bin/busybox mkdir -p /ownedroot/proc; /bin/busybox mount -t proc proc /ownedroot/proc; /bin/busybox chroot /ownedroot /_qh_probe_01/rosetta/rosetta /opt/miniconda3/envs/testbed/bin/python3.9 -I -B -c 'import sys,ssl,pytest,pluggy,platform,json,requests,hashlib; print("QH_ROOT_IMPORT_OK"); print(json.dumps(dict(version=sys.version,executable=sys.executable,prefix=sys.prefix,machine=platform.machine(),openssl=ssl.OPENSSL_VERSION,pytest=pytest.__version__,pluggy=pluggy.__version__,requests=requests.__version__,paths={m.__name__:m.__file__ for m in (ssl,pytest,pluggy,requests)},requests_file_sha256=hashlib.sha256(open(requests.__file__,"rb").read()).hexdigest()),sort_keys=True))'; echo QH_ROOT_PYTHON_EXIT=$?; fi
            /bin/busybox poweroff -f

            """
            input.fileHandleForWriting.write(Data(commands.utf8))
        }
    case .failure(let error):
        print("QH_VM_START_ERROR \(error)")
        exit(1)
    }
}
DispatchQueue.main.asyncAfter(deadline: .now() + 180) {
    print("QH_VM_DEADLINE")
    machine.stop { error in
        print("QH_VM_STOP_COMPLETION \(String(describing: error))")
        exit(124)
    }
}
dispatchMain()
