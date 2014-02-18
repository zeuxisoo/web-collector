# coding: utf-8

from flask import Blueprint, g
from flask import flash, redirect, url_for, render_template
from ..forms import SignupForm, SigninForm, ChangeProfileForm, ChangePasswordForm
from ..models import User, UserConnection
from ..helpers.user import login_user, logout_user, require_login

blueprint = Blueprint('user', __name__)

@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = form.save()
        flash('Thanks for your register. Your account has been created', 'success')
        return redirect(url_for('user.signup'))

    return render_template('user/signup.html', form=form)

@blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()

    if form.validate_on_submit():
        login_user(form.user, form.permanent.data)
        return redirect(url_for('index.index'))

    return render_template('user/signin.html', form=form)

@require_login
@blueprint.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index.index'))

@require_login
@blueprint.route('/change/profile', methods=['GET', 'POST'])
def change_profile():
    form = ChangeProfileForm(obj=g.user)

    if form.validate_on_submit():
        user = User.query.get(g.user.id)
        form.populate_obj(user)
        user.save()

        flash('Your profile was updated', 'success')

        return redirect(url_for('user.change_profile'))

    return render_template('user/change/profile.html', form=form)

@require_login
@blueprint.route('/change/password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm(obj=g.user)

    if form.validate_on_submit():
        user = User.query.get(g.user.id)
        user.change_password(form.new_password.data)
        form.populate_obj(user)
        user.save()

        flash('Your password was updated, Please sign in again', 'success')

        return redirect(url_for('user.signout'))

    return render_template('user/change/password.html', form=form)

@require_login
@blueprint.route('/change/connection', methods=['GET', 'POST'])
def change_connection():
    user_connections    = UserConnection.query.filter(
        UserConnection.user_id == g.user.id,
        UserConnection.access_token != ''
    ).all()

    connected_providers = [user_connection.provider_name for user_connection in user_connections]

    return render_template('user/change/connection.html', connected_providers=connected_providers)

