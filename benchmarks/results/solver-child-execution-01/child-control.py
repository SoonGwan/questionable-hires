import subprocess,sys,json,base64
normal=subprocess.run([sys.executable,'-I','-B','-c','print(42)'],capture_output=True,timeout=5,cwd='/solver')
assert normal.returncode==0 and normal.stdout==b'42\n' and normal.stderr==b''
code='import sys;sys.stdout.buffer.write(bytes([0,255]));sys.stderr.write("expected failure");sys.exit(7)'
failure=subprocess.run([sys.executable,'-I','-B','-c',code],capture_output=True,timeout=5,cwd='/solver')
assert failure.returncode==7 and failure.stdout==bytes([0,255]) and failure.stderr==b'expected failure'
arm=subprocess.run(['/bin/busybox','printf','arm-child'],capture_output=True,timeout=5)
assert arm.returncode==0 and arm.stdout==b'arm-child'
absent=subprocess.run(['/bin/busybox','test','-e','/private/tmp/qh-external-bundle-02-private-grading'],capture_output=True,timeout=5)
assert absent.returncode==1
print(json.dumps(dict(executable=sys.executable,normal_exit=normal.returncode,normal_stdout=normal.stdout.decode(),failure_exit=failure.returncode,failure_stdout_base64=base64.b64encode(failure.stdout).decode(),failure_stderr=failure.stderr.decode(),arm_exit=arm.returncode,host_grader_absent=True),sort_keys=True))
print('QH_SOLVER_CHILD_EXECUTION_PROOF')
