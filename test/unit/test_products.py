import logging
from flask.testing import FlaskClient
from test_utils import get_status_str, login


log = logging.getLogger()


def test_products_crud(client: FlaskClient):
    data = dict(
        name='lapte',
        quantity=2,
        weight=0,  # 0 inseamna ca este irelevant
        expiration_date='2022-01-10',
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


def test_read_prod(client: FlaskClient):
    login(client)
    res = client.get('/products/read?name=lapte')
    log.debug(res.data.decode())

    res = client.post('/products/inc', data={'name': 'lapte-nush'})
    assert res.status_code == 200
    
    res = client.post('/products/dec', data={'name': 'lapte-nush'})
    assert res.status_code == 200

    # res = client.post('/products/dec', data={'name': 'lapte-nush'})
    res = client.post('/products/dec', data={'name': 'lapte-nush'})
    assert res.status_code != 200

    log.debug(get_status_str(res))

    res = client.get('products/date')
    log.debug(res.data.decode()) 


def test_shopping_list(client: FlaskClient):
    login(client)
    res = client.get('/products/shopping_list')
    assert res.status_code == 200
    log.debug(res.data.decode())

    client.post('/products/delete_shopping_list')
    res = client.get('/products/shopping_list')
    assert res.status_code == 200
    assert res.data.decode() == '[]\n'

