# coding: utf-8

from ..models import User

def force_integer(value, default=1):
    try:
        return int(value)
    except:
        return default

def fill_with_users(items):
    user_ids  = [item.user_id for item in items]
    users     = User.query.filter(User.id.in_(user_ids)).all()
    user_dict = {user.id: user for user in users}

    for item in items:
        item.user = user_dict.get(item.user_id)

    return items
