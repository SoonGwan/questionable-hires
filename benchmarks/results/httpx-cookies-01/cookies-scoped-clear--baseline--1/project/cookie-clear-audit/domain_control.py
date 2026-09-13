from pathlib import Path
import httpx
assert Path(httpx.__file__).resolve() == Path.cwd() / "httpx/__init__.py"
cookies = httpx.Cookies()
for domain, path, value in [
    ("example.com", "/subpath/1", "target-one"),
    ("example.com", "/subpath/2", "target-two"),
    ("example.org", "/subpath/1", "other-domain"),
]:
    cookies.set("name", value, domain=domain, path=path)
cookies.clear(domain="example.com")
remaining = {(c.domain, c.path, c.name, c.value) for c in cookies.jar}
assert remaining == {("example.org", "/subpath/1", "name", "other-domain")}, remaining
print("Imported:", httpx.__file__)
print("Domain-only control PASS:", remaining)
