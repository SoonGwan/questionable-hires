#!/bin/sh
set -eu
cd /solver-input
/bin/busybox sha256sum -c checksums
/bin/busybox mkdir -p /solver
/bin/busybox mkdir -p /solver/psf__requests-3362
/bin/busybox tar -xf psf__requests-3362.tar -C /solver/psf__requests-3362
/bin/busybox test ! -e /solver/psf__requests-3362/.git
/bin/busybox echo QH_SOURCE_READY_psf__requests-3362
/bin/busybox mkdir -p /solver/psf__requests-863
/bin/busybox tar -xf psf__requests-863.tar -C /solver/psf__requests-863
/bin/busybox test ! -e /solver/psf__requests-863/.git
/bin/busybox echo QH_SOURCE_READY_psf__requests-863
/bin/busybox mkdir -p /solver/psf__requests-1963
/bin/busybox tar -xf psf__requests-1963.tar -C /solver/psf__requests-1963
/bin/busybox test ! -e /solver/psf__requests-1963/.git
/bin/busybox echo QH_SOURCE_READY_psf__requests-1963
/bin/busybox mkdir -p /solver/psf__requests-2674
/bin/busybox tar -xf psf__requests-2674.tar -C /solver/psf__requests-2674
/bin/busybox test ! -e /solver/psf__requests-2674/.git
/bin/busybox echo QH_SOURCE_READY_psf__requests-2674
/bin/busybox mkdir -p /solver/pytest-dev__pytest-5221
/bin/busybox tar -xf pytest-dev__pytest-5221.tar -C /solver/pytest-dev__pytest-5221
/bin/busybox test ! -e /solver/pytest-dev__pytest-5221/.git
/bin/busybox echo QH_SOURCE_READY_pytest-dev__pytest-5221
/bin/busybox mkdir -p /solver/pytest-dev__pytest-5103
/bin/busybox tar -xf pytest-dev__pytest-5103.tar -C /solver/pytest-dev__pytest-5103
/bin/busybox test ! -e /solver/pytest-dev__pytest-5103/.git
/bin/busybox echo QH_SOURCE_READY_pytest-dev__pytest-5103
/bin/busybox mkdir -p /solver/pytest-dev__pytest-6116
/bin/busybox tar -xf pytest-dev__pytest-6116.tar -C /solver/pytest-dev__pytest-6116
/bin/busybox test ! -e /solver/pytest-dev__pytest-6116/.git
/bin/busybox echo QH_SOURCE_READY_pytest-dev__pytest-6116
/bin/busybox mkdir -p /solver/pytest-dev__pytest-11143
/bin/busybox tar -xf pytest-dev__pytest-11143.tar -C /solver/pytest-dev__pytest-11143
/bin/busybox test ! -e /solver/pytest-dev__pytest-11143/.git
/bin/busybox echo QH_SOURCE_READY_pytest-dev__pytest-11143
/bin/busybox test ! -e /private/tmp/qh-external-bundle-02-private-grading
/bin/busybox test ! -e /Users
/bin/busybox echo QH_NO_HOST_GRADER_PATH
/bin/busybox echo QH_SOLVER_RAM_PROOF
