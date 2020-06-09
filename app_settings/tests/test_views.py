import pytest
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/'
USERNAME = 'tlk'
PASSWORD = 'tlk12345'


@pytest.fixture(scope="module", name="auth_paras")
def get_auth_paras():
    class AuthParas:
        def __init__(self):
            url = BASE_URL + 'login'
            data = {
                'username': USERNAME,
                'password': PASSWORD
            }
            kwargs = {
                "data": data
            }
            response = requests.post(url=url, **kwargs)
            _dict = json.loads(response.text)
            self.token = _dict['token']

    return AuthParas()


def test_get_all_settings(auth_paras):
    """
    Tests whether the settings API endpoint retrieves all settings in the SQLite database.
    """
    url = BASE_URL + 'settings/'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        "headers": headers
    }

    response = requests.get(url=url, **kwargs)
    if response.status_code == 200:
        data = response.json()
        if len(data) >= 0:
            assert True
            return

    assert False


def test_get_settings_by_name(auth_paras):
    """
    Tests whether the settings API endpoint retrieves all settings that matches the name parameter.
    """
    url = BASE_URL + 'settings/'
    params = {'name': 'dummy1_Name'}
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        'headers': headers
    }

    response = requests.get(url=url, **kwargs, params=params)
    if response.status_code == 200:
        data = response.json()['results']
        assert len(data) == 2
        if data[0]['name'] == 'dummy1_Name' and data[1]['name'] == 'dummy1_Name':
            assert True
            return

    assert False


def test_get_settings_by_type(auth_paras):
    """
    Tests whether the settings API endpoint retrieves all settings that matches the type parameter.
    """
    url = BASE_URL + 'settings/'
    params = {'type': 'xyz'}
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        'headers': headers
    }

    response = requests.get(url=url, **kwargs, params=params)
    if response.status_code == 200:
        data = response.json()['results']
        assert len(data) == 0
        return

    assert False


def test_get_settings_by_name_and_type(auth_paras):
    """
    Tests whether the settings API endpoint retrieves settings when name and type are given.
    """
    url = BASE_URL + 'settings/'
    params = {
        'name': 'dummy1_Name',
        'type': 'dummy1_Type'
    }
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        'headers': headers
    }

    response = requests.get(url=url, **kwargs, params=params)
    if response.status_code == 200:
        data = response.json()['results']
        assert len(data) == 1
        if data[0]['name'] == 'dummy1_Name' and data[0]['type'] == 'dummy1_Type':
            assert True
            return

    assert False


def test_create_new_setting(auth_paras):
    """
    Tests settings API endpoint by adding a new setting, given a name, type and value.
    """
    url = BASE_URL + 'settings/'
    data = {
        'name': 'dummy_name',
        'type': 'dummy_type',
        'value': 'dummy_value'
    }
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        'headers': headers
    }

    response = requests.post(url=url, **kwargs, data=data)
    if response.status_code == 201:
        r = response.json()
        if r['name'] == 'dummy_name' and r['type'] == 'dummy_type' and r['value'] == 'dummy_value':
            assert True
            return

    assert False


def test_create_invalid_setting(auth_paras):
    """
    Tests settings API endpoint by trying to add an invalid setting into the SQLite database.
    """
    url = BASE_URL + 'settings/'
    data = {
        'name': 'dummy_name',
        # 'type' argument is missing
        'value': 'dummy_value'
    }
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        'headers': headers
    }

    response = requests.post(url=url, **kwargs, data=data)
    if response.status_code == 400:
        if response.json()['error']:
            assert True
            return

    assert False
