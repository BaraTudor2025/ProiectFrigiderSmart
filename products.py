from datetime import date
from multiprocessing.sharedctypes import Value
from sqlite3 import Date
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import logging
import pymongo
import pymongo.database
import auth
from db import get_database, get_products

bp = Blueprint('products', __name__, url_prefix='/products')
log = logging.getLogger()


@bp.route('/add', methods=['POST'])
@auth.login_required
def add():
    try:
        name = request.form['name']
        if not name:
            raise ValueError('name cannot be empty')

        for p in get_products():
            if p['name'] == name:
                return jsonify({'status': 'product with name already exists'}), 403

        if (quantity := int(request.form['quantity'])) <= 0:
            raise ValueError('invalid quantity')

        if (weight := int(request.form['weight'])) < 0:
            raise ValueError('invalid weight')

        expirationDate = date.fromisoformat(request.form['expiration_date'])

        category = request.form['category']

        # TO DO: photo
        # TO DO: barcode

    except Exception as e:
        log.debug('invalid schema')
        return jsonify({'status': f'bad schema: {e.args}'}), 403

    product = {
        "name": name,
        "quantity": quantity,
        "weight": weight,
        "expiration_date": expirationDate.isoformat(),
        "category": category
    }
    db = get_database()
    db.users.update_one({'_id': g.user_id}, {'$push': {'products': product}})
    return jsonify({'status': 'product added'}), 200


@bp.route('/read', methods=['GET'])
@auth.login_required
def read():
    name = request.args.get("name")
    # /products/read     ?name=ceva
    db = get_database()
    if name is None:
        return jsonify(db.products.find())
    if db.products.find({"name": name}):
        return jsonify(db.products.find_one({"name": name}))
    else:
        log.warning("Couldn't find any products by the given name")
        return jsonify({"error": "couldn't find product"})


@bp.route('/update', methods=['POST'])
@auth.login_required
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
    db.products.update_one({"_id": id}, {"name": name,
                                     "quantity": quantity,
                                     "product_weight": weight,
                                     "expiration_date": expirationDate,
                                     "category": category})


@bp.route('/delete', methods=['POST'])
@auth.login_required
def delete():
    name = request.form['name']
    db = get_database()
    if db.users.update_one({'_id': g.user_id}, {'$pull': {'products': {'name': name}}}):
        return jsonify({'status': 'deleted product'}), 200
    else:
        return jsonify({"error": "couldn't find the product to delete"}), 403
