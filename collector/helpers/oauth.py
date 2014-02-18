# coding: utf-8

import importlib
from flask import g
from flask import request, flash, redirect, url_for
from flask_oauthlib.client import OAuthException
from ..models import UserConnection, User
from ..helpers.user import login_user

def authorized_callback(response, provider_name):
    if response is None:
        error = request.args.get('error'),
        error_description = request.args.get('error_description')

        flash('Access denied: reason={0}, error={1}'.format(''.join(error), error_description), 'error')

        return redirect(url_for('user.change_connection' if g.user else 'user.signin'))
    elif 'access_token' not in response:
        flash('Authentication failed, Can not get the access token, Please sign in again', 'error')
        return redirect(url_for('user.change_connection' if g.user else 'user.signin'))
    else:
        access_token = response['access_token']

        current_package  = __name__.split('.')[0]
        provider_modules = importlib.import_module(".providers", package=current_package)
        provider_class   = getattr(provider_modules, '{0}Provider'.format(provider_name.capitalize()))

        provider              = provider_class(access_token)
        provider_user_id      = provider.user_id()
        provider_display_name = provider.display_name()
        provider_email        = provider.email()

        # Make user login if the connection is already connected
        user_connection = UserConnection.query.filter_by(provider_name=provider_name, provider_user_id=provider_user_id).first()

        if user_connection:
            user_connection.provider_user_id = provider_user_id
            user_connection.access_token     = access_token
            user_connection.display_name     = provider_display_name
            user_connection.save()

            user = User.query.get(user_connection.user_id)

            login_user(user)

            return redirect(url_for('user.change_connection' if g.user else 'index.index'))

        # Redirect to sign in page if the provider.email() is registered in website
        if provider.email():
            user = User.query.filter_by(email=provider.email()).first()

            if user:
                flash('You already registered, Please sign in by email account', 'error')
                return redirect(url_for('user.change_connection' if g.user else 'user.signin'))

        # Create new user if not connected and email is not registered
        user = User(
            email    = provider_email,
            password = User.generate_token(20)
        ).save()

        UserConnection(
            user_id          = user.id,
            provider_name    = provider_name,
            provider_user_id = provider_user_id,
            access_token     = access_token,
            display_name     = provider_display_name
        ).save()

        login_user(user)

        return redirect(url_for('user.change_connection' if g.user else 'index.index'))
