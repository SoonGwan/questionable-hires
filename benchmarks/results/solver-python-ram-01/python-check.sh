#!/bin/sh
set -eu
/bin/busybox mkdir -p /proc /sys /rosetta /lib64
/bin/busybox mount -t proc proc /proc
/bin/busybox mount -t sysfs sysfs /sys
/bin/busybox modprobe virtiofs
/bin/busybox mount -t virtiofs rosetta /rosetta
/bin/busybox echo "359a09cb4b543ab8f73440b14f2ee8a4b690583c26afb7c8e53a5055cd28ff6e  /runtime.tar" | /bin/busybox sha256sum -c -
/bin/busybox tar -xf /runtime.tar -C /
/bin/busybox rm /runtime.tar
/bin/busybox ln -s /runtime/glibc/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
LD_LIBRARY_PATH=/runtime/env/lib:/runtime/glibc /rosetta/rosetta /runtime/env/bin/python3.9 -I -B -c 'import sys,ssl,sqlite3,pytest,pluggy,json; c=sqlite3.connect(":memory:"); c.execute("create table control(value)"); c.execute("insert into control values(7)"); assert c.execute("select value from control").fetchall()==[(7,)]; c.close(); print(json.dumps(dict(python=sys.version,pytest=pytest.__version__,ssl=ssl.OPENSSL_VERSION,sqlite=sqlite3.sqlite_version,prefix=sys.prefix))); print("QH_SOLVER_PYTHON_RAM_PROOF")'
/bin/busybox test ! -e /private/tmp/qh-external-bundle-02-private-grading
/bin/busybox test ! -e /Users
/bin/busybox echo QH_PYTHON_NO_HOST_GRADER
