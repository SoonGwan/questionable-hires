"""Owned experimental stdio MCP adapter to the frozen guest serial channel."""
import argparse
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import threading
import time

from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent, ToolAnnotations
from pydantic import Field


class Guest:
    def __init__(self, root, log, ready_timeout=20):
        self.process = None
        self.closed = False
        self.failed = False
        self.log = log.open('xb')
        self.selector = selectors.DefaultSelector()
        self.pending = bytearray()
        self.lock = threading.RLock()
        self.sequence = 0
        try:
            self.process = subprocess.Popen([str(root / 'probe'), str(root)], stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
            os.set_blocking(self.process.stdout.fileno(), False)
            self.selector.register(self.process.stdout, selectors.EVENT_READ)
            self.until(lambda line: True if line == 'QH_AGENT_READY' else None, ready_timeout)
        except BaseException:
            self.failed = True
            self.force_close()
            raise

    def until(self, predicate, timeout):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            while b'\n' in self.pending:
                line, _, remainder = self.pending.partition(b'\n')
                self.pending[:] = remainder
                result = predicate(line.decode(errors='replace').strip())
                if result is not None:
                    return result
            for key, _ in self.selector.select(0.1):
                data = os.read(key.fileobj.fileno(), 65536)
                if not data:
                    raise RuntimeError('Guest channel ended')
                self.log.write(data)
                self.log.flush()
                self.pending.extend(data)
        raise TimeoutError('Guest response deadline')

    def request(self, command, cwd, timeout):
        with self.lock:
            if self.failed or self.closed:
                raise RuntimeError('Guest channel is closed after failure')
            self.sequence += 1
            request = dict(id=self.sequence, command=command, cwd=cwd, timeout=timeout)
            try:
                self.process.stdin.write((json.dumps(request) + '\n').encode())
                self.process.stdin.flush()
                response = self.until(lambda line: json.loads(line[12:]) if line.startswith('QH_RESPONSE ') else None,
                                      timeout + 3)
                if response.get('id') != self.sequence:
                    raise RuntimeError('Guest response ID mismatch')
                return response
            except BaseException:
                self.failed = True
                self.force_close()
                raise

    def force_close(self):
        if self.closed:
            return
        self.closed = True
        try:
            if self.process is not None and self.process.poll() is None:
                try:
                    os.killpg(self.process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                self.process.wait(timeout=5)
        finally:
            self.selector.close()
            if self.process is not None:
                self.process.stdin.close()
                self.process.stdout.close()
            self.log.close()

    def close(self):
        with self.lock:
            if self.closed:
                return
            try:
                if self.process.poll() is None:
                    self.process.stdin.write(b'{"shutdown":true}\n')
                    self.process.stdin.flush()
                    self.until(lambda line: True if line == 'QH_VM_GUEST_STOPPED' else None, 5)
                    self.process.wait(timeout=2)
            finally:
                self.force_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--vm', type=Path, required=True)
    parser.add_argument('--log', type=Path, required=True)
    args = parser.parse_args()
    guest = Guest(args.vm.resolve(strict=True), args.log)
    server = FastMCP('qh-guest-command-prototype')

    @server.tool(structured_output=False, annotations=ToolAnnotations(
        readOnlyHint=False, destructiveHint=True, idempotentHint=False, openWorldHint=False))
    def guest_command(command: str = Field(min_length=1, max_length=8192, strict=True),
                      cwd: str = Field(default='/solver', max_length=1024, strict=True),
                      timeout: int = Field(default=5, ge=1, le=10, strict=True)) -> CallToolResult:
        """Execute an authorized shell command inside the disposable Linux guest only.

        Commands can mutate/delete guest files. No host shell fallback. Results
        preserve exit/timeout and binary output as base64; each stream retains its
        first4096 bytes with bytes-read/truncation flags. A returned exit1 is not
        success evidence; inspect the command outcome. No network or host data share.
        """
        response = guest.request(command, cwd, timeout)
        return CallToolResult(content=[TextContent(type='text', text=json.dumps(response))],
                              isError='error' in response)

    try:
        server.run(transport='stdio')
    finally:
        guest.close()
