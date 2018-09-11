'''Tests the /status endpoint.'''
import pytest

from skope_service.app import app

# pylint: disable=redefined-outer-name

@pytest.fixture(scope='module')
def client():
    '''Return the Flask client instance to test against.'''
    return app.test_client()

@pytest.fixture(scope='module')
def response(client):
    '''Return the response from calling the service at the /status endpoint.'''
    return client.get('/status')

@pytest.fixture(scope='module')
def response_json(response):
    '''Return the JSON body of response.'''
    return response.get_json()

# pylint: disable=redefined-outer-name, missing-docstring

def test_response_status_is_success(response):
    assert response.status == '200 OK'
    assert response.status_code == 200

def test_response_body_is_json(response):
    assert response.is_json
    assert response.mimetype == 'application/json'

def test_response_header_has_two_keys(response):
    assert len(response.headers) == 2
    assert response.headers['Content-Type'] == 'application/json'
    assert int(response.headers['Content-Length']) > 0

def test_response_json_contains_just_name_key(response_json):
    assert len(response_json) == 1
    assert 'name' in response_json

def test_response_name_property_has_service_name_for_value(response_json):
    assert response_json['name'] == 'SKOPE Timeseries Service'
