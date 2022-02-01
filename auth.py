from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_database
from bson.objectid import ObjectId
import functools
import logging
from util import handle_exception

bp = Blueprint('auth', __name__, url_prefix='/auth')
log = logging.getLogger()


@bp.route('/register', methods=["POST"])
@handle_exception
def register():
    username = request.form['username']
    password = request.form['password']
    db = get_database()

    if not username:
        return jsonify({'status': 'username is required'}), 403
    elif not password:
        return jsonify({'status': 'password is required'}), 403

    # verifica daca user-ul deja exita
    if None != db.users.find_one({'username': username}):
        return jsonify({'status': 'user already exists'}), 403
    else:
        db.users.insert_one({'username': username, 'password': generate_password_hash(password), 'products': []})
    log.debug(f'user registered {username}')
    return jsonify({'status': 'user registered succesfully'}), 200


@bp.route('/login', methods=["POST"])
@handle_exception
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_database()
    user = db.users.find_one({'username': username})

    if user is None:
        return jsonify({'status': 'username not found'}), 403
    elif not check_password_hash(user['password'], password):
        return jsonify({'status': 'password is incorrect'}), 403

    session.clear()
    session['user_id_bin'] = user['_id'].binary
    return jsonify({'status': 'user logged in succesfully'}), 200


@bp.route('/logout')
@handle_exception
def logout():
    session.clear()
    g.user_id = None
    return jsonify({'status': 'user logged out succesfully'}), 200


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id_bin') is None:
            return jsonify({'status': 'user is not authenticated'}), 403

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id_bin = session.get('user_id_bin')

    if user_id_bin is None:
        g.user_id = None
    else:
        g.user_id = ObjectId(user_id_bin)
