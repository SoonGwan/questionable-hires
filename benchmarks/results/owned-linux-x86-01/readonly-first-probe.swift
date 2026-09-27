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
let fixture = VZVirtioFileSystemDeviceConfiguration(tag: "fixture")
fixture.share = VZSingleDirectoryShare(directory: VZSharedDirectory(url: directory.appendingPathComponent("fixture"), readOnly: true))
config.directorySharingDevices = [translation, fixture]
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
            /bin/busybox mkdir -p /rosetta /fixture
            /bin/busybox mount -t virtiofs rosetta /rosetta
            /bin/busybox mount -t virtiofs fixture /fixture
            /bin/busybox uname -a
            /bin/busybox uname -m
            /rosetta/rosetta /fixture/busybox.static uname -m
            echo QH_X86_UNAME_EXIT=$?
            /rosetta/rosetta /fixture/busybox.static sh -c 'echo QH_X86_WORKLOAD_OK; echo $((6 * 7))'
            echo QH_X86_WORKLOAD_EXIT=$?
            /bin/busybox sh -c 'echo forbidden > /fixture/should-not-write'
            echo QH_READONLY_WRITE_EXIT=$?
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
