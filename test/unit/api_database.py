import pymongo.errors
from db import get_database, close_db_connection
import logging

log = logging.getLogger()


def test_db_connection():
    db = get_database()
    assert db is not None
    # close_db_connection()

def check_database_connection():
    db = get_database()
    if db is None:
        log.error("Couldn't establish database connection")
        return False
    else:
        return True


def close_database_connection():
    try:
        close_db_connection()
        return True
    except pymongo.errors as e:
        log.error(e)
        return False
