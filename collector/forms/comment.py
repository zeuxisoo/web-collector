# coding: utf-8

from .base import BaseForm
from wtforms import TextAreaField
from wtforms.validators import Required
from ..models import Comment

class CommentForm(BaseForm):
    content = TextAreaField(
        'Content',
        validators=[
            Required(message='Please enter content')
        ]
    )

    def save(self, category, result_id, user):
        comment = Comment(**self.data)
        comment.category  = category
        comment.result_id = result_id
        comment.user_id   = user.id
        comment.save()

        return comment
