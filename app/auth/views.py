from . import auth
from flask import url_for, render_template, redirect, flash, request
from .forms import LoginForm, RegisterForm_email, ChangePasswordForm, EditProfileForm
from ..models import User
from sqlalchemy import or_
from .. import db
from flask_login import login_user, logout_user, login_required, current_user
from ..email import send_mail

@auth.before_app_request
def before():
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint != 'main.index' \
                and request.endpoint != 'auth.unconfirmed' \
                and request.endpoint != 'auth.logout':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


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
            return redirect(request.args.get('next') or url_for('main.index'))
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


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.oldpassword.data
        if current_user.checkpassword(old_password):
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            flash('password changed')
            return redirect(url_for('main.index'))
        flash('password error')
        return render_template('/auth/changepassword.html', form=form)
    return render_template('/auth/changepassword.html', form=form)

@auth.route('/edit-password', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user_detail = form.user_detail.data
        current_user.user_detail = user_detail
        db.session.add(current_user)
        flash('profile edit success')
        return redirect(url_for('main.user', name=current_user.username))
    form.user_detail.data = current_user.user_detail
    return render_template('/auth/edit_profile.html', form=form)

