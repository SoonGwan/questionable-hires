import pathlib,sys,importlib,json
root=pathlib.Path(sys.argv[1]).resolve()
source=root/'src' if (root/'src').is_dir() else root
if root.name in {"pytest-dev__pytest-5221", "pytest-dev__pytest-5103", "pytest-dev__pytest-6116"}:
    sys.path.insert(0,"/runtime-compat")
sys.path.insert(0,str(source))
module=importlib.import_module(sys.argv[2])
assert pathlib.Path(module.__file__).resolve().is_relative_to(root),module.__file__
print(json.dumps(dict(issue=root.name,module=module.__name__,version=module.__version__,path=module.__file__),sort_keys=True))
