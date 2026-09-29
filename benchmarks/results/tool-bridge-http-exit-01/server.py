"""Scoped experimental MCP adapter; existing eight skills remain unchanged."""
import argparse
from functools import partial
import importlib.util
import json
from pathlib import Path
from typing import Literal
import anyio
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr

class WorkingTree(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    working_tree: Literal[True]

class Recipe(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    fixed: list[StrictStr] = Field(min_length=1)
    vary: list[StrictStr] = Field(min_length=1)
    before: StrictStr
    after: StrictStr | WorkingTree
    imports: list[StrictStr] = Field(min_length=1)
    tests: list[StrictStr] = Field(min_length=1)
    runner: Literal['unittest'] = 'unittest'
    invocation: Literal['bootstrap', 'module'] = 'bootstrap'
    additional_before: list[StrictStr] = Field(default_factory=list)
    observe_assertions: StrictBool = False
    guard_tree: StrictBool = False
    import_roots: list[StrictStr] = Field(default_factory=list)
    watch: list[StrictStr] = Field(default_factory=list)
    module_bindings: dict[StrictStr, StrictStr] = Field(default_factory=dict)

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--helper', type=Path, required=True)
parser.add_argument('--python', required=True)
parser.add_argument('--port', type=int, required=True)
args = parser.parse_args()
root = args.source.resolve(strict=True)
assert root.is_dir()
spec = importlib.util.spec_from_file_location('native_receipt', args.helper.resolve(strict=True))
helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
server = FastMCP('questionable-hires-receipt-prototype', host='127.0.0.1', port=args.port)
project_gate = anyio.Lock()

@server.tool(structured_output=False)
async def receipt_compare(recipe: Recipe, timeout: int = Field(default=30, ge=1, le=300, strict=True)) -> CallToolResult:
    """Compare selected historical implementations with identical current native unittest tests. Paths are relative to the launch-authorized project. Native exit1 is valid before-failure evidence; inspect assertions/imports/guards/cleanup. CLI-style incomplete observations are tool errors, not repair proof. Trusted tests only; not a sandbox."""
    # Default thread behavior waits for the native helper; never abandon its cleanup.
    async with project_gate:
        value = await anyio.to_thread.run_sync(partial(helper.compare, root,
            dict(recipe.model_dump(exclude_defaults=True), runner='unittest'), python=args.python, timeout=timeout))
        # Deliver pending cancellation after native cleanup, before any normal reply.
        await anyio.lowlevel.checkpoint()
    return CallToolResult(content=[TextContent(type='text', text=json.dumps(value, separators=(',', ':')))],
                          isError=value['status'] != 'observed')

if __name__ == '__main__':
    server.run(transport='streamable-http')
