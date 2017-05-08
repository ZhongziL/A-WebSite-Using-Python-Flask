from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length, Regexp
from wtforms import ValidationError
from ..models import User

class LoginForm_username(FlaskForm):
    username = StringField('username')
    password = StringField('password')
    submit = SubmitField('Log In')

class LoginForm_email(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email()])
    password = StringField('password', validators=[InputRequired()])
    submit = SubmitField('Log In')

class LoginForm_telnumber(FlaskForm):
    telnumber = StringField('telnumber', validators=[InputRequired(), Length(11), Regexp('^[1-9][0-9]*&')])
    password = StringField('password', validators=[InputRequired()])
    submit = SubmitField('Log In')

class RegisterForm_email(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email()])
    password = StringField('password', validators=[InputRequired()])
    password_confirm = StringField('confirm_password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username is already exist')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email address has already been registered')

class RegisterForm_telnumber(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    telnumber = StringField('telnumber', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username is already exist')

    def validate_telnumber(self, field):
        if User.query.filter_by(telnumber=field.data).first():
            raise ValidationError('telnumber has already been registered')