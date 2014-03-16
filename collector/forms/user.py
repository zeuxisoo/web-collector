# coding: utf-8

from flask import g
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length, Regexp
from .base import BaseForm
from ..models import User

class SignupForm(BaseForm):
    username = TextField(
        'Username',
        validators=[
            Required(message='Please enter username'),
            Length(min=3, max=20),
            Regexp(r'^[a-z0-9A-Z]+$', message='Username must english characters only.')
        ]
    )

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

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.lower()).count():
            raise ValueError('This username has been registered.')

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

class ChangeProfileForm(BaseForm):
    email = TextField(
        'Email',
        validators=[
            Required(message='Please enter email'),
            Email(message='Invalid email format')
        ]
    )

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).count():
            raise ValueError('Email already registered')

class ChangePasswordForm(BaseForm):

    old_password = PasswordField(
        'Old Password',
        validators=[
            Required(message="Please enter old password")
        ]
    )

    new_password = PasswordField(
        'New Password',
        validators=[
            Required(message='Please enter new password'),
            Length(message="New password must more than 8 length", min=8),
            EqualTo('confirm_new_password', message='New password must match'),
        ]
    )

    confirm_new_password = PasswordField('Confirm New Password')

    def validate_old_password(self, field):
        user = User.query.filter_by(email=g.user.email).first()

        if User.password_verify(field.data.lower(), user.password) is False:
            raise ValueError("Password incorrect")
