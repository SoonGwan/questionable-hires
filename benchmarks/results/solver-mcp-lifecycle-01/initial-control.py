"""Exact Guest class controls with synthetic native processes, no models/VMs."""
import ast
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import tempfile
import threading
import time


def guest_class(source):
    tree = ast.parse(source.read_text())
    nodes = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'Guest']
    assert len(nodes) == 1
    scope = dict(subprocess=subprocess, selectors=selectors, os=os, threading=threading,
                 time=time, json=json, signal=signal)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec'), scope)
    cls = scope['Guest']
    original = cls.until
    cls.until = lambda self, predicate, timeout: original(self, predicate, min(timeout, 0.2))
    return cls


def measure(source):
    cls = guest_class(source)
    results = []
    for case in ['startup-timeout', 'wrong-id', 'response-timeout', 'graceful']:
        root = Path(tempfile.mkdtemp(prefix='qh-mcp-lifecycle-'))
        program = '#!' + sys.executable + '\nimport sys,json,time\n'
        if case == 'startup-timeout':
            program += 'time.sleep(10)\n'
        else:
            program += 'print("QH_AGENT_READY",flush=True)\n'
            program += 'for line in sys.stdin:\n r=json.loads(line)\n'
            program += ' if r.get("shutdown"): print("QH_VM_GUEST_STOPPED",flush=True);break\n'
            if case == 'wrong-id':
                program += ' print("QH_RESPONSE "+json.dumps({"id":999}),flush=True)\n'
            elif case == 'response-timeout':
                program += ' time.sleep(10)\n'
            else:
                program += ' print("QH_RESPONSE "+json.dumps({"id":r["id"],"result":{"exit_code":0}}),flush=True)\n'
        (root / 'probe').write_text(program)
        (root / 'probe').chmod(0o700)
        obj = cls.__new__(cls)
        error = None
        try:
            cls.__init__(obj, root, root / 'guest.log')
            obj.request('ignored synthetic command', '/solver', 1)
            obj.close()
            if case == 'graceful' and hasattr(obj, 'closed'):
                obj.close()
        except Exception as caught:
            error = type(caught).__name__
        stopped = obj.process.poll() is not None
        results.append(dict(case=case, error=error, process_stopped_before_author_cleanup=stopped))
        # Preserve observation first, then reclaim baseline's leaked owned process.
        if not stopped:
            os.killpg(obj.process.pid, signal.SIGKILL)
            obj.process.wait(timeout=5)
        obj.selector.close()
        obj.process.stdin.close()
        obj.process.stdout.close()
        obj.log.close()
    return results


if __name__ == '__main__':
    previous, candidate = Path(sys.argv[1]), Path(sys.argv[2])
    before, after = measure(previous), measure(candidate)
    for rows in [before, after]:
        assert [row['error'] for row in rows] == ['TimeoutError', 'RuntimeError', 'TimeoutError', None]
    assert all(not row['process_stopped_before_author_cleanup'] for row in before[:3])
    assert all(row['process_stopped_before_author_cleanup'] for row in after)
    print(json.dumps(dict(result='PASS', previous=before, candidate=after,
                         synthetic_process_controls=True, models=0, actual_vms=0), indent=2))
