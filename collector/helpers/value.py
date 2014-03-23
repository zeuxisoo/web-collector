# coding: utf-8

from ..models import User, Stream, Today

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

def fill_with_images(items):
    stream_target_ids = [item.target_id for item in items if item.category == 'stream']
    today_target_ids  = [item.target_id for item in items if item.category == 'today']

    streams = Stream.query.filter(Stream.result_id.in_(stream_target_ids)).all()
    todays  = Today.query.filter(Today.result_id.in_(today_target_ids)).all()

    stream_dict = { stream.result_id: stream for stream in streams }
    today_dict  = { today.result_id: today for today in todays }

    for item in items:
        if item.category == 'stream':
            item.image = stream_dict.get(item.target_id)
        else:
            item.image = today_dict.get(item.target_id)

    return items
