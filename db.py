from itertools import product
from pymongo import MongoClient
from pymongo.database import Database, Collection
import logging
import atexit
from flask import g

log = logging.getLogger('mongo-db')

# object is a singleton
g_frigider_db: Database = None
g_mongo_client: MongoClient = None

def get_database() -> Database:
    global g_frigider_db, g_mongo_client
    if g_frigider_db == None:
        client = MongoClient("mongodb+srv://florian:florian@smartfridgecluster.yle9m.mongodb.net")
        log.debug('client connection made')
        atexit.register(lambda: client.close())
        g_frigider_db = client['frigider-db']
        g_mongo_client = client
    return g_frigider_db


def get_products() -> list[dict]:
    """
    trebuie ca user-ul sa fie logat
    """
    db = get_database()
    return db.users.find_one({'_id': g.user_id})['products']

def close_db_connection():
    global g_mongo_client, g_frigider_db
    g_mongo_client.close()
    g_frigider_db = None

