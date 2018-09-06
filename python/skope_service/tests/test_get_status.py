import pytest

from skope_service.app import app

@pytest.fixture(scope='module')
def client(request):
    return app.test_client()

@pytest.fixture(scope='module')
def response(client):
    return client.get('/')

@pytest.fixture(scope='module')
def response_json(response):
    return response.get_json()

def test_response_status_is_success(response):
    assert response.status == '200 OK'
    assert response.status_code == 200