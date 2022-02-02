import pytest
from flask.testing import FlaskClient
from main import create_app
import json

@pytest.fixture(scope="package", autouse=True)
def client(request) -> FlaskClient:
    local_app = create_app()
    local_app.testing = True
    client = local_app.test_client()
    yield client
    def teardown():
        pass
        # return to home
    request.addfinalizer(teardown)


def get_status_str(rv):
    return json.loads(rv.data.decode())['status']


def login(client):
    return client.post('/auth/login', data={'username': 'admin', 'password': 'admin'}, follow_redirects=True)
