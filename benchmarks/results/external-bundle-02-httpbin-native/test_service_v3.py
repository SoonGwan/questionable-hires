import requests
from pytest_httpbin import certs

def test_http_service(httpbin):
    response = requests.get(httpbin.url + '/get', timeout=2)
    assert response.status_code == 200
    assert response.json()['url'] == httpbin.url + '/get'

def test_https_service(httpbin_secure):
    response = requests.get(httpbin_secure.url + '/get', verify=certs.where(), timeout=2)
    assert response.status_code == 200

def test_https_rejects_untrusted_ca(httpbin_secure):
    try:
        requests.get(httpbin_secure.url + '/get', timeout=2)
    except requests.exceptions.SSLError as error:
        assert 'certificate verify failed' in str(error).lower()
    else:
        raise AssertionError('untrusted fixture CA was accepted')

def test_https_rejects_wrong_hostname(httpbin_secure):
    try:
        requests.get(httpbin_secure.url.replace('127.0.0.1', 'localhost') + '/get', verify=certs.where(), timeout=2)
    except requests.exceptions.SSLError as error:
        assert 'localhost' in str(error) and ('match' in str(error) or 'hostname' in str(error))
    else:
        raise AssertionError('wrong hostname was accepted')
