from pydoc import cli
import pytest
import json
from main import create_app
from flask.testing import FlaskClient
from db import get_database, close_db_connection

@pytest.fixture()
def client() -> FlaskClient:
    local_app = create_app()
    local_app.testing = True
    client = local_app.test_client()
    yield client

def test_db_connection():
    db = get_database()
    assert db != None
    close_db_connection()

def test_register(client: FlaskClient):
    rv = client.post('/auth/register', data={'username': 'admin', 'password': 'admin'}, follow_redirects=True)
    assert rv.status_code == 403
    res = json.loads(rv.data.decode())
    assert res['status'] == 'User already exists'


