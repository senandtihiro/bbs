import os
import json
import time
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort
from functools import wraps
from models.user import User


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        # print('user', u)
        return u


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        print('login required')
        u = current_user()
        if u is None:
            return redirect('/user/login')
        return f(*args, **kwargs)
    return function



