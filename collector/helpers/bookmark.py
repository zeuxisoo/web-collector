# coding: utf-8

from ..models import Bookmark

def is_bookmarked(type, target_id, user_id):
    return Bookmark.query.filter_by(type=type, target_id=target_id, user_id=user_id).first()
