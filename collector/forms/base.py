# coding: utf-8

from flask.ext.wtf import Form

class BaseForm(Form):
    def __init__(self, *args, **kwargs):
        self._obj = kwargs.get('obj', None)
        super(BaseForm, self).__init__(*args, **kwargs)
