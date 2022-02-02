from flask.testing import FlaskClient
from test_utils import get_status_str, login

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
