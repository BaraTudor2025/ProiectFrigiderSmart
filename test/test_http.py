from pydoc import cli
import pytest
import json
from main import create_app
from flask.testing import FlaskClient
from db import get_database, close_db_connection
import logging

log = logging.getLogger()


@pytest.fixture(scope="function", autouse=True)
def client(request) -> FlaskClient:
    local_app = create_app()
    local_app.testing = True
    client = local_app.test_client()
    yield client
    def teardown():
        pass
        # return to home
    request.addfinalizer(teardown)

def test_db_connection():
    db = get_database()
    assert db is not None
    # close_db_connection()


def get_status_str(rv):
    return json.loads(rv.data.decode())['status']


def login(client):
    return client.post('/auth/login', data={'username': 'admin', 'password': 'admin'}, follow_redirects=True)


def test_register(client: FlaskClient):
    res = client.post('/auth/register', data={'username': 'admin', 'password': 'admin'}, follow_redirects=True)
    assert res.status_code == 403
    assert get_status_str(res) == 'user already exists'

    res = client.post('/auth/register', data={'password': 'admin'}, follow_redirects=True)
    assert res.status_code == 400  # bad request

    res = client.post('/auth/register', data={'username': '', 'password': ''}, follow_redirects=True)
    assert res.status_code == 403
    assert get_status_str(res) == 'username is required'


def test_login(client: FlaskClient):
    res = client.post('/auth/login', data={'username': 'admin-care-nu-exita', 'password': 'admin'},
                      follow_redirects=True)
    assert res.status_code == 403
    assert get_status_str(res) == 'username not found'

    res = client.post('/auth/login', data={'username': 'admin', 'password': 'parola-gresita'}, follow_redirects=True)
    assert res.status_code == 403
    assert get_status_str(res) == 'password is incorrect'

    res = login(client)
    assert res.status_code == 200
    assert get_status_str(res) == 'user logged in succesfully'

    res = client.get('/auth/logout')
    assert res.status_code == 200
    assert get_status_str(res) == 'user logged out succesfully'


def test_products_crud(client: FlaskClient):
    data = dict(
        name='lapte',
        quantity=2,
        weight=0,  # 0 inseamna ca este irelevant
        expiration_date='2022-02-10',
        category='lactate'
    )

    client.get('/auth/logout')
    res = client.post('/products/add', data=data, follow_redirects=True)
    log.debug(res.status)
    assert res.status_code == 403
    assert get_status_str(res) == 'user is not authenticated'

    login(client)

    res = client.post('/products/delete', data={'name': data['name']})
    assert res.status_code == 200

    res = client.post('/products/add', data=data)
    log.debug(get_status_str(res))
    assert res.status_code == 200
