import logging
import pymongo
import pymongo.database

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from db import get_database

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__file__)

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/add', methods=["POST"])
def add():
    name = request.form['ProductName']
    quantity = request.form['ProductQuantity']  # buc
    weight = request.form['ProductWeight']
    # TO DO: photo
    expirationDate = request.form['ProductExpDate']
    # TO DO: barcode
    category = request.form['ProductCategory']
    db = get_database()
    product = {
        "name": name,
        "quantity": quantity,
        "product_weight": weight,
        "expiration_date": expirationDate,
        "category": category
    }
    # TO DO: Treat Connection Failure Exception
    db.products.insert_one(product).inserted_id


@bp.route('/read', methods=["GET"])
def read():
    name = request.args.get("name")
    # /products/read     ?name=ceva
    db = get_database()
    if name is None:
        return jsonify(db.products.find())
    if db.products.find({"name": name}):
        return jsonify(db.products.find_one({"name": name}))
    else:
        logger.warning("Couldn't find any products by the given name")
        return jsonify({"error": "couldn't find product"})


@bp.route('/update', methods=["POST"])
def update():
    id = request.form["ProductId"]
    name = request.form['ProductName']
    quantity = request.form['ProductQuantity']  # buc
    weight = request.form['ProductWeight']
    # TO DO: photo
    expirationDate = request.form['ProductExpDate']
    # TO DO: barcode
    category = request.form['ProductCategory']
    db = get_database()
    product = db.products.find_one({"_id": id})
    if product is None:
        return jsonify({"error": "couldn't find the product to update"})
    db.products.update({"_id": id}, {"name": name,
                                     "quantity": quantity,
                                     "product_weight": weight,
                                     "expiration_date": expirationDate,
                                     "category": category})


@bp.route('/delete', methods=["POST"])
def delete():
    id = request.form["ProductId"]
    db = get_database()
    product = db.products.find_one({"_id": id})
    if product is None:
        return jsonify({"error": "couldn't find the product to delete"})
    db.products.remove({"_id":  id}, {justOne: True})
