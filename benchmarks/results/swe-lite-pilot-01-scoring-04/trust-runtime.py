from pathlib import Path
import certifi

bundle = Path(certifi.where())
assert not str(bundle).startswith('/testbed/')
with bundle.open('ab') as output:
    output.write(b'\n' + Path('/tmp/ca.pem').read_bytes())
print('QH_SCOPED_CA_CONFIGURED', flush=True)
