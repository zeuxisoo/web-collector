# coding: utf-8

from flask import session
from ..models import User

def login_user(user, permanent=False):
    if not user:
        return None
    else:
        session['id']    = user.id
        session['token'] = user.token

        if permanent:
            session.permanent = True

    return user

def logout_user():
    if 'id' not in session:
        return

    session.pop('id')
    session.pop('token')

def get_current_user():
    if 'id' in session and 'token' in session:
        user = User.query.get(int(session['id']))

        if not user:
            return None
        elif user.token != session['token']:
            return None
        else:
            return user

    return None
