# coding: utf-8

from flask import Blueprint
from flask import flash, redirect, url_for, render_template
from ..forms import SignupForm, SigninForm
from ..helpers.user import login_user, logout_user

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

@blueprint.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index.index'))
