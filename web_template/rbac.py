from functools import wraps

from flask import request, session, redirect, url_for, jsonify


def login_required():
    def mid(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if session.get('login_user'):
                resp = func(*args, **kwargs)
                return resp
            else:
                return redirect(url_for('user_role_permiss.login'))

        return inner

    return mid


def check_permission():
    def mid(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if request.method not in session.get('user_permissions'):
                return redirect(url_for('user_role_permiss.index')), 403
            else:
                resp = func(*args, **kwargs)
                return resp

        return inner

    return mid
