from itertools import product
from pymongo import MongoClient
import pymongo
import pymongo.database
import logging
import atexit

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger('mongo-db')

# object is a singleton
g_frigider_db: pymongo.database.Database = None

def get_database() -> pymongo.database.Database:
    global g_frigider_db
    if g_frigider_db == None:
        client = MongoClient("mongodb+srv://florian:florian@smartfridgecluster.yle9m.mongodb.net")
        logger.debug('client connection made')
        atexit.register(lambda: client.close())
        g_frigider_db = client['frigider-db']
    return g_frigider_db