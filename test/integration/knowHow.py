from pydoc import cli
import pytest
import json
from main import create_app
from flask.testing import FlaskClient
from db import get_database, close_db_connection
import logging

"""
GLOBAL VARIABLES:
    Toate string-urile sau toate variablele de care aveti nevoie trebuie adaugate la inceput:
"""
PASSWORD_INCORECT_TEXT = "password is incorrect"
FAIL_STATUS_CODE = 403

"LOGGERE SAU ALTE CLASE CARE TREBUIESC INITAILIZATE"

log = logging.getLogger()


@pytest.fixture()
def client(request) -> FlaskClient:
    local_app = create_app()
    local_app.testing = True
    client = local_app.test_client()
    yield client


class Test_Ce_Trebuie_Testat:
    """
    Cateva informatii despre testele voastre
    Spre exemplu: Toate testele care se ocupa de crud-uri pe produse
    """

    def get_status_str(self, rv):
        """
        Compileaza dar nu face parte din teste
        Este o functie a clasei care ne returneaza date
        """
        return json.loads(rv.data.decode())['status']

    def test_case_1(self):
        """
        Toate testele care vor fi rulate trebuie sa inceapa cu 'test'.
        Scrieti ce trebuie sa faca testul vostru
        Spre exemplu: Verificam daca adaugam un produs in frigider care are data experirarii mai mica de 7 zile. Este adaugat in lista
        Pytest functioneaza cu assert-uri -> verificati daca exista vreo functie in api-ul de unit care sa faca ce va doriti
        Daca un assert va intoarce Fail testul vostru este picat
        """
        assert self.get_status_str(res) == PASSWORD_INCORECT_TEXT
        assert res.status_code == FAIL_STATUS_CODE
