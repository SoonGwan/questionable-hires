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
config.memorySize = 512 * 1024 * 1024
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
let runtime = VZVirtioFileSystemDeviceConfiguration(tag: "runtime")
runtime.share = VZSingleDirectoryShare(directory: VZSharedDirectory(url: directory.appendingPathComponent("case-sensitive-mount/runtime"), readOnly: true))
config.directorySharingDevices = [translation, runtime]
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
            /bin/busybox mkdir -p /rosetta /runtime /lib64
            /bin/busybox mount -t virtiofs rosetta /rosetta
            /bin/busybox mount -t virtiofs runtime /runtime
            /bin/busybox ln -s /runtime/glibc/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
            /bin/busybox uname -m
            LD_LIBRARY_PATH=/runtime/env/lib:/runtime/glibc /rosetta/rosetta /runtime/env/bin/python3.9 -I -B -c 'import sys,ssl,pytest,pluggy,platform,json; print("QH_PYTHON_IMPORT_OK"); print(json.dumps(dict(version=sys.version,executable=sys.executable,prefix=sys.prefix,machine=platform.machine(),openssl=ssl.OPENSSL_VERSION,pytest=pytest.__version__,pluggy=pluggy.__version__,paths={m.__name__:m.__file__ for m in (ssl,pytest,pluggy)}),sort_keys=True))'
            echo QH_PYTHON_EXIT=$?
            /bin/busybox poweroff -f

            """
            input.fileHandleForWriting.write(Data(commands.utf8))
        }
    case .failure(let error):
        print("QH_VM_START_ERROR \(error)")
        exit(1)
    }
}
DispatchQueue.main.asyncAfter(deadline: .now() + 25) {
    print("QH_VM_DEADLINE")
    machine.stop { error in
        print("QH_VM_STOP_COMPLETION \(String(describing: error))")
        exit(124)
    }
}
dispatchMain()
