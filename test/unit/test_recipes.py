import json
from flask.testing import FlaskClient
from test_utils import get_status_str, login


def test_recipes(client: FlaskClient):
    #login(client)
    res = client.get('/recipes?number=4&ingredients=milk,honey')
    data = json.loads(res.data.decode())
    json.dump(data, indent=2, fp=open('./recipes-response.json', mode='w'))
    assert res.status_code == 200

