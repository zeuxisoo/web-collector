# coding: utf-8

from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length
from .base import BaseForm
from ..models import User

class SignupForm(BaseForm):
    email = TextField(
        'Email',
        validators=[
            Required(message='Please enter email'),
            Email(message='Invalid email format')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            Required(message='Please enter password'),
            Length(message="Password must more than 8 length", min=8),
            EqualTo('confirm_password', message='Passwords must match'),
        ]
    )

    confirm_password = PasswordField('Confirm Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).count():
            raise ValueError('This email has been registered.')

    def save(self):
        data = self.data
        data.pop('confirm_password', None)

        user = User(**data)
        user.save()

        return user

class SigninForm(BaseForm):
    email = TextField(
        'Email',
        validators=[
            Required(message='Please enter email'),
            Email(message='Invalid email format')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            Required(message='Please enter password'),
        ]
    )

    permanent = BooleanField('Remember me')

    def validate_password(self, field):
        account = self.email.data

        user = User.query.filter_by(email=account).first()

        if not user:
            raise ValueError('Account not found')
        elif user.password_verify(field.data, user.password) is False:
            raise ValueError('Password incorrect')
        else:
            self.user = user
            return user
