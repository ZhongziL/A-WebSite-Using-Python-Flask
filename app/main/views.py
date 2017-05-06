from . import main

@main.route('/')
def index():
    return '<p>hello world<p>'