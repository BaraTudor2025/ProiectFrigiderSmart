from datetime import date
from urllib.request import Request
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import logging
import pymongo
import pymongo.database
import auth
from db import get_database, get_products
from util import handle_exception

bp = Blueprint('products', __name__, url_prefix='/products')
log = logging.getLogger()


@bp.route('/add', methods=['POST'])
@auth.login_required
@handle_exception
def add():
    try:
        # validate object
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
        return jsonify({'status': f'bad schema: {e.args}'}), 400

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
@handle_exception
def read():
    name = request.args.get('name')
    db = get_database()
    user = db.users.find_one({'_id': g.user_id})
    if name is None:
        return jsonify(user['products']), 200
    # else
    for p in user['products']:
        if p['name'] == name:
            return jsonify(p), 200
    # else
    log.warning("Couldn't find any products by the given name")
    return jsonify({"status": "couldn't find product"}), 404


def remove_from_db(name: str):
    db = get_database()
    return db.users.update_one({'_id': g.user_id}, {'$pull': {'products': {'name': name}}})


def add_to_shopping_list(name: str, force=False):
    db = get_database()
    sl = db.users.find_one({'_id': g.user_id})['shopping_list']
    add = lambda: db.users.update_one({'_id': g.user_id}, {'$push': {'shopping_list': name}})
    if not force:
        for p in get_products():
            if p['quantity'] == 0 and p['name'] == name and (name not in sl):
                add()
                return
    elif name not in sl:
        add()


def _modify(request: Request, inc: bool):
    name = request.form['name']
    if not name:
        return jsonify({'status': 'name cannot be empty'}), 400

    q = 1
    if not inc:
        q = -1

    db = get_database()
    res = db.users.update_one(
        {'_id': g.user_id}, 
        {'$inc': {'products.$[elem].quantity': q}},
        array_filters=[{'elem.name': name, 'elem.quantity': {'$gt': 0}}]
    )

    if not inc and res.modified_count == 1:
        add_to_shopping_list(name, force=False)

    if res.modified_count == 1:
        return jsonify({'status': 'quantity modified'}), 200
    else:
        return jsonify({'status': 'could not modify quantity'}), 200


@bp.route('/shopping_list', methods=['GET'])
@auth.login_required
@handle_exception
def shopping_list():
    pass


@bp.route('/inc', methods=['POST'])
@auth.login_required
@handle_exception
def inc():
    return _modify(request, inc=True)


@bp.route('/dec', methods=['POST'])
@auth.login_required
@handle_exception
def dec():
    return _modify(request, inc=False)


@bp.route('/delete', methods=['POST'])
@auth.login_required
@handle_exception
def delete():
    name = request.form['name']
    if remove_from_db(name):
        add_to_shopping_list(name, force=True)
        return jsonify({'status': 'deleted product'}), 200
    else:
        return jsonify({'status': "couldn't find the product to delete"}), 404
