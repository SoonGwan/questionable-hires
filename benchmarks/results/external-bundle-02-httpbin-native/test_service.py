import requests
from pytest_httpbin import certs

def test_http_service(httpbin):
    response = requests.get(httpbin.url + '/get', timeout=2)
    assert response.status_code == 200
    assert response.json()['url'] == httpbin.url + '/get'

def test_https_service(httpbin_secure):
    response = requests.get(httpbin_secure.url + '/get', verify=certs.where(), timeout=2)
    assert response.status_code == 200
