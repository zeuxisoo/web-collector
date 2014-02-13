# coding: utf-8

from ..models import Bookmark

def is_bookmarked(category, target_id, user_id):
    return Bookmark.query.filter_by(category=category, target_id=target_id, user_id=user_id).first()
