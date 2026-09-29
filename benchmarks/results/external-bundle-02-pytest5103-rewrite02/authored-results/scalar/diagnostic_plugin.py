import json,sys
from pathlib import Path
def pytest_collection_modifyitems(config,items):
 from _pytest.assertion import rewrite
 record=dict(assertmode=config.getoption('assertmode'),special_all=hasattr(rewrite.AssertionRewriter,'_visit_all'),rewrite_path=rewrite.__file__,hooks=[type(h).__name__ for h in sys.meta_path],collected=len(items),rewritten=[any(n.startswith('@pytest') for n in i.obj.__code__.co_names) for i in items])
 Path('native-observation.json').write_text(json.dumps(record))
