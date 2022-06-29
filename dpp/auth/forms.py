from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, Label, TextAreaField, DateField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired

from .. import models as m
from . import (
    views as v
    )

class RegisterDoctor(FlaskForm):
    """
        Here we will create doctor registration form.
    """
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=10)], render_kw={'placeholder':'i.e Dr'})
    speciality = StringField('Speciality', validators=[DataRequired()], render_kw={'placeholder':'i.e Cardiologist'})
    first_name = StringField('First Name', validators=[DataRequired()], render_kw={'placeholder':'First Name'})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={'placeholder':'Last Name'})
    gender = StringField('Gender', validators=[DataRequired()], render_kw={'placeholder':'Male | Female, M | F'})
    address = StringField('Address', validators=[DataRequired()], render_kw={'placeholder':'129th Ave. Sandton'})
    bio = TextAreaField('A short biography', validators=[DataRequired()], render_kw={'placeholder':'About your career and where you are based.'})
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)], render_kw={'placeholder':'i.e +2711828160'})
    email = StringField('Email', validators=[DataRequired(), Email('Invalid email.')], render_kw={'placeholder':'i.e  doctor@gmail.com'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Password'})
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[DataRequired(), EqualTo('password')], 
        render_kw={'placeholder':'Confirm Password'}
    )

    submit = SubmitField('Register')

    def email_validation(self, email_):
        if m.Doctor.query.filter_by(email=email_.data).first():
            raise ValidationError(message='Email already taken.')


class RegisterPatient(FlaskForm):
    """
        Here we will create patient registration form.
    """
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=10)], render_kw={'placeholder':'i.e Mr, Mrs, Mss'})
    first_name = StringField('First Name', validators=[DataRequired()], render_kw={'placeholder':'First Name'})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={'placeholder':'Last Name'})
    gender = StringField('Gender', validators=[DataRequired()], render_kw={'placeholder':'Male or Female | M or F'})
    dob = DateField('Date Of Birth', validators=[DataRequired()], render_kw={'placeholder':'yyyy-mm-dd'})
    education = StringField('Education', validators=[DataRequired()], render_kw={'placeholder':'University student.'})
    marital_status = StringField('Marital Status', validators=[DataRequired()], render_kw={'placeholder':'Single | Married | Widowed'})
    address = StringField('Address', validators=[DataRequired()], render_kw={'placeholder':'E29 Blekkies section Morokweng'})
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)], render_kw={'placeholder':'+27711828160 | 0711828160'})
    email = StringField('Email', validators=[DataRequired(), Email('Invalid email.')], render_kw={'placeholder':'example@demo.com'})
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired()],
            render_kw={'placeholder':'Password'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder':'Confirm Password'})

    submit = SubmitField('Register')

    def email_validation(self, email_):
        if m.Doctor.query.filter_by(email=email_.data).first():
            raise ValidationError(message='Email already taken.')

class LoginPatient(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Invalid email.')], render_kw={'placeholder':'patient@example.com'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Password'})
    submit_ = SubmitField('Login')
    register = SubmitField('Register', render_kw={'formnovalidate': True})

class LoginDoctor(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Invalid email.')], render_kw={'placeholder':'doctor@example.com'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Password'})
    submit_ = SubmitField('Login')
    register = SubmitField('Register', render_kw={'formnovalidate': True})



class RequestResetForm(FlaskForm):
    email = StringField('Email',
                         validators=[DataRequired(), Email()], render_kw={'placeholder' : 'me@email.com'})
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        if v.usertype.get_usertype():

            if v.usertype.get_usertype() == '_pt_':
                user = m.Patient.query.filter_by(email=email.data).first()
            elif v.usertype.get_usertype() == '_dr_':
                user = m.Doctor.query.filter_by(email=email.data).first()
            
            if user is None:
                raise ValidationError('There is no account with that email. Your must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Password'})
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[DataRequired(), EqualTo('password')], 
        render_kw={'placeholder':'Confirm Password'}
    )

    submit = SubmitField('Reset Password')