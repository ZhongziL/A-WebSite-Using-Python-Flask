from . import main
from flask import render_template, abort
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
        abort(404)
    return render_template('profile.html', user=user)