from itertools import product
from pymongo import MongoClient
import pymongo
from pymongo.database import Database
import logging
import atexit

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger('mongo-db')

# object is a singleton
g_frigider_db: Database = None
g_mongo_client: MongoClient = None

def get_database() -> Database:
    global g_frigider_db
    global g_mongo_client
    if g_frigider_db == None:
        client = MongoClient("mongodb+srv://florian:florian@smartfridgecluster.yle9m.mongodb.net")
        logger.debug('client connection made')
        atexit.register(lambda: client.close())
        g_frigider_db = client['frigider-db']
        g_mongo_client = client
    return g_frigider_db

def close_db_connection():
    g_mongo_client.close()