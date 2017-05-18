from . import auth
from flask import url_for, render_template, redirect, flash
from .forms import LoginForm, RegisterForm_email
from ..models import User
from sqlalchemy import or_
from .. import db
from flask_login import login_user, logout_user, login_required
from ..email import send_mail

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username_email = form.username_email.data
        password = form.password.data
        user = User.query.filter(or_(User.username==username_email,
                                        User.email==username_email)).first()

        if user is not None and user.checkpassword(password):
            login_user(user)
            flash('login success')
            return redirect(url_for('main.index'))
        else:
            flash('username or password error')
            return render_template('/auth/login.html', form=form)
    else:
        return render_template('/auth/login.html', form=form)
    return render_template('/auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm_email()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = User.query.filter(or_(username=='username', email=='email')).first()

        if user is None:
            u = User(username=username, email=email, password=password)
            send_mail(email, username, 'fuck')
            db.session.add(u)
            flash('register success')
            return redirect(url_for('auth.login'))
        else:
            flash('username or email is already existed')
            return render_template('/auth/register.html', form=form)
    else:
        return render_template('/auth/register.html', form=form)
    return render_template('/auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    flash('logout success')
    logout_user()
    return redirect(url_for('auth.login'))

