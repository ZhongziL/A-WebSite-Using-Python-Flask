from . import auth
from flask import url_for, render_template, redirect, flash
from .forms import LoginForm_username, RegisterForm_email

@auth.route('/login')
def login():
    form = LoginForm_username()
    if form.validate_on_submit():
        return redirect(url_for('main.index'))
    return render_template('/auth/login.html', form=form)

@auth.route('/register')
def register():
    form = RegisterForm_email()
    if form.validate_on_submit():
        return redirect(url_for('auth.login'))
    return render_template('/auth/register.html', form=form)

