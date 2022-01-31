from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from werkzeug.security import check_password_hash, generate_password_hash
from db import get_database
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    db = get_database()

    if not username:
        return jsonify({'status': 'Username is required.'}), 403
    elif not password:
        return jsonify({'status': 'Password is required.'}), 403

    # verifica daca user-ul deja exita
    if None != db.users.find_one({'username': username}):
        return jsonify({'status': 'User already exists'}), 403
    else:
        db.users.insert_one({'username': username, 'password': generate_password_hash(password)})

    return jsonify({'status': 'user registered succesfully'}), 200


@bp.route('/login', methods=["POST"])
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
    session['user_id'] = user['id']
    return jsonify({'status': 'user logged in succesfully'}), 200


@bp.route('/logout')
def logout():
    session.clear()
    return jsonify({'status': 'user logged out succesfully'}), 200


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'status': 'User is not authenticated'}), 403

        return view(**kwargs)

    return wrapped_view


# @flaskbp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()
