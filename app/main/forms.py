from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class PostForm(FlaskForm):
    post = StringField('post')
    submit = SubmitField('submit')