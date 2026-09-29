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
try config.validate()
let lifecycle = Lifecycle()
let machine = VZVirtualMachine(configuration: config)
machine.delegate = lifecycle
machine.start { result in
    switch result {
    case .success:
        print("QH_VM_STARTED")
        DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
            input.fileHandleForWriting.write(Data("/bin/busybox uname -a\n/bin/busybox echo QH_LINUX_GUEST_PROOF\n/bin/busybox poweroff -f\n".utf8))
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
