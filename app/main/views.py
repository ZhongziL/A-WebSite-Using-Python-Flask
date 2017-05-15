from . import main
from flask import render_template

@main.route('/')
def index(username=None):
    return render_template('index.html', username=username)