from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, EqualTo, Length, Regexp, DataRequired
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    username_email = StringField('username_email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class LoginForm_telnumber(FlaskForm):
    telnumber = StringField('telnumber', validators=[DataRequired(), Length(11), Regexp('^[1-9][0-9]*&')])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterForm_email(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    password_confirm = StringField('confirm_password')
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username is already exist')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email address has already been registered')

class RegisterForm_telnumber(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    telnumber = StringField('telnumber', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username is already exist')

    def validate_telnumber(self, field):
        if User.query.filter_by(telnumber=field.data).first():
            raise ValidationError('telnumber has already been registered')