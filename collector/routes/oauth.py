# coding: utf-8

from flask import Blueprint, g
from flask import current_app, flash, redirect, url_for, session
from ..helpers.oauth import authorized_callback
from ..models import UserConnection

blueprint = Blueprint('oauth', __name__)

@blueprint.route('/connect/<provider>')
def connect(provider):
    providers = current_app.oauth.providers

    if provider in providers:
        return providers[provider].authorize(callback=url_for('oauth.authorized', provider=provider, _external=True))
    else:
        flash('Not found provider', 'error')
        return redirect(url_for('user.signin'))

@blueprint.route('/disconnect/<provider>')
def disconnect(provider):
    providers = current_app.oauth.providers

    if provider in providers:
        session.pop('{0}_token'.format(provider.lower()), None)

        if g.user:
            user_connection = UserConnection.query.filter_by(user_id=g.user.id, provider_name=provider).first()
            user_connection.access_token = ""
            user_connection.save()

            flash('Disconnect to {0} completed'.format(provider.capitalize()), 'success')

            return redirect(url_for('user.change_connection'))
        else:
            return redirect(url_for('index.index'))
    else:
        flash('Not found provider', 'error')
        return redirect(url_for('user.signin'))


    return redirect(url_for('index.index'))

@blueprint.route('/connect/authorized/<provider>')
def authorized(provider):
    providers = current_app.oauth.providers

    if provider in providers:
        return providers[provider].authorized_handler(authorized_callback)(provider)
    else:
        flash('Not found provider', 'error')
        return redirect(url_for('user.signin'))
