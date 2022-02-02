import logging
from math import prod
from re import T
import re

from flask import Blueprint
from api_database import check_database_connection
from db import get_products
from products import remove_from_db


log = logging.getLogger()


def check_product(productName):
    if check_database_connection():
        for product in get_products():
            if product['name'] == productName:
                return True
        log.warning("Couldn't find the given product")
        return False
    else:
        log.warning("Couldn't establish a connection with the database")


def remove_product(productName):
    if check_product(productName):
        if check_database_connection():
            try:
                remove_from_db()
                if not check_product(productName):
                    return True
                else:
                    log.warning("Couldn't remove product from database")
                    return False
            except:
                log.warning("Function db.remove_from_db raises exception")
                return False
        else:
            log.warning("Couldn't establish a connection with the database")
            return False
    else:
        log.warning(
            "The product you are trying to remove is not in the database")
