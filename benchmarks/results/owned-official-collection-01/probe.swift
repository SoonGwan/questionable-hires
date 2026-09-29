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
let fixture = VZVirtioFileSystemDeviceConfiguration(tag: "probe")
fixture.share = VZSingleDirectoryShare(directory: VZSharedDirectory(url: directory.appendingPathComponent("fixture"), readOnly: true))
let root = VZVirtioFileSystemDeviceConfiguration(tag: "root")
root.share = VZSingleDirectoryShare(directory: VZSharedDirectory(url: URL(fileURLWithPath: CommandLine.arguments[2]), readOnly: true))
config.directorySharingDevices = [translation, fixture, root]
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
            /bin/busybox mount -t virtiofs probe /ownedroot/_qh_probe_01/layers
            /bin/busybox mount -t virtiofs rosetta /ownedroot/_qh_probe_01/rosetta
            /bin/busybox mount -t proc proc /ownedroot/proc
            /bin/busybox mount -t tmpfs tmpfs /ownedroot/tmp
            /bin/busybox mount -t devtmpfs devtmpfs /ownedroot/dev
            echo QH_DEVTMPFS_EXIT=$?
            /bin/busybox modprobe loop
            echo QH_LOOP_EXIT=$?
            /bin/busybox modprobe squashfs
            echo QH_SQUASHFS_EXIT=$?
            /bin/busybox mkdir -p /modloop /tmp
            /bin/busybox mount -t squashfs -o loop,ro /ownedroot/_qh_probe_01/layers/modloop-virt /modloop
            echo QH_MODLOOP_MOUNT_EXIT=$?
            /bin/busybox find /modloop/modules/6.12.110-0-virt -name binfmt_misc.ko -o -name binfmt_misc.ko.gz
            if [ -f /modloop/modules/6.12.110-0-virt/kernel/fs/binfmt_misc.ko ]; then /bin/busybox cp /modloop/modules/6.12.110-0-virt/kernel/fs/binfmt_misc.ko /tmp/binfmt_misc.ko; else /bin/busybox gzip -dc /modloop/modules/6.12.110-0-virt/kernel/fs/binfmt_misc.ko.gz > /tmp/binfmt_misc.ko; fi
            echo QH_MODULE_PREPARE_EXIT=$?
            /bin/busybox insmod /tmp/binfmt_misc.ko
            echo QH_MODULE_LOAD_EXIT=$?
            /bin/busybox mount -t binfmt_misc binfmt_misc /ownedroot/proc/sys/fs/binfmt_misc
            echo QH_BINFMT_MOUNT_EXIT=$?
            /bin/busybox chroot /ownedroot /_qh_probe_01/rosetta/rosetta /opt/miniconda3/envs/testbed/bin/python3.9 -I -B /_qh_probe_01/layers/register.py
            echo QH_REGISTER_EXIT=$?
            /bin/busybox chroot /ownedroot /_qh_probe_01/rosetta/rosetta /opt/miniconda3/envs/testbed/bin/python3.9 -B /_qh_probe_01/layers/probe.py
            echo QH_COLLECTION_DRIVER_EXIT=$?
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
