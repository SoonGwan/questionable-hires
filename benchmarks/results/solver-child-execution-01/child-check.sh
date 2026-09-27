#!/bin/sh
set -eu
/bin/busybox echo "da142869626ec9d4543ab46482af10b5ff2c8c1c2e01068ddf32360316a06218  /modloop-virt" | /bin/busybox sha256sum -c -
/bin/busybox modprobe loop
/bin/busybox modprobe squashfs
/bin/busybox mkdir -p /modloop /tmp
/bin/busybox mount -t squashfs -o loop,ro /modloop-virt /modloop
/bin/busybox cp /modloop/modules/6.12.110-0-virt/kernel/fs/binfmt_misc.ko /tmp/binfmt_misc.ko
/bin/busybox insmod /tmp/binfmt_misc.ko
/bin/busybox mount -t binfmt_misc binfmt_misc /proc/sys/fs/binfmt_misc
LD_LIBRARY_PATH=/runtime/env/lib:/runtime/glibc /rosetta/rosetta /runtime/env/bin/python3.9 -I -B /register.py
LD_LIBRARY_PATH=/runtime/env/lib:/runtime/glibc /rosetta/rosetta /runtime/env/bin/python3.9 -I -B /child-control.py
/bin/busybox umount /modloop
