from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, Label, TextAreaField, DateField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired

from .. import models as m

class RegisterAdmin(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[DataRequired()],
        render_kw={'placeholder' : 'First Name'}
        )
    last_name = StringField(
        'Last Name',
        validators=[DataRequired()],
        render_kw={'placeholder' : 'Last Name'}
        )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email('Invalid email')],
        render_kw={'placeholder' : 'Email'}
        )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={'placeholder' : 'Password'}
        )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(),
        EqualTo('password', message='Password mismatch.')],
        render_kw={'placeholder' : 'Confirm Password'}
        )
    register = SubmitField('Register')

    def email_validation(self, email_):
        if m.Admin.query.filter_by(email=email_.data).first():
            raise ValidationError(message='Email already taken.')

class LoginAdmin(FlaskForm):
    emial = StringField(
        'Email',
        validators=[DataRequired(),
        Email(message='Invalid email.')],
        render_kw={'placeholder' : 'admin@dpp.com'}
        )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={'placeholder' : 'Password'}
        )
    submit = SubmitField('Log In')
    register = SubmitField(
        'Register',
        render_kw={'formnovalidate' : True}
        )
