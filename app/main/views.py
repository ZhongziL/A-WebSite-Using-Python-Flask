from . import main
from flask import render_template, redirect, url_for
from flask_login import login_required
from ..models import User

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<name>')
@login_required
def user(name):
    user = User.query.filter_by(username=name).first()
    if user is None:
        return redirect(url_for('auth.login'))
    return render_template('profile.html', user=user)