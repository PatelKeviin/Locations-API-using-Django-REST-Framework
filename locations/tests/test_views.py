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


def test_get_all_locations(auth_paras):
    """
    Tests whether the locations API endpoint retrieves all locations in the SQLite database.
    """
    url = BASE_URL + 'locations/'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        "headers": headers
    }

    response = requests.get(url=url, **kwargs)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            assert True
            return

    assert False


def test_get_valid_single_location(auth_paras):
    """
    Tests whether the locations API endpoint retrieves geo-codes when a VALID location is given.
    """
    url = BASE_URL + 'locations/'
    params = {'location': 'California'}
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        'headers': headers
    }

    response = requests.get(url=url, **kwargs, params=params)

    if response.status_code == 200:
        data = response.json()[0]
        if data['loc'] == 'California' and data['lat'] != -1 and data['lon'] != -1:
            assert True
            return

    assert False


def test_get_invalid_single_location(auth_paras):
    """
    Tests whether the locations API endpoint retrieves -1 as geo-code values when an INVALID location is given.
    """
    url = BASE_URL + 'locations/'
    params = {'location': 'abc'}
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        'headers': headers
    }

    response = requests.get(url=url, **kwargs, params=params)

    if response.status_code == 200:
        data = response.json()[0]
        if data['loc'] == 'abc' and data['lat'] == -1 and data['lon'] == -1:
            assert True
            return

    assert False


def test_get_multiple_locations(auth_paras):
    """
    Tests whether the locations API endpoint retrieves latitudes and longitudes when multiple locations are given.
    """
    url = BASE_URL + 'locations/'
    params = {
        'location': ['NewYork', 'abc', 'Boise'],
    }
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        'headers': headers
    }

    response = requests.get(url=url, **kwargs, params=params)
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 3
        # checking geo-codes for 'NewYork' location
        data_ny = data[0]
        if data_ny['loc'] == 'NewYork' and round(data_ny['lat'], 2) == 40.71 and round(data_ny['lon'], 2) == -74.01:
            assert True
            return

    assert False
