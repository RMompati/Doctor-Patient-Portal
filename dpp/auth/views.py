from is_safe_url import is_safe_url
from flask import (
    render_template, request, flash, g, redirect, url_for, session
)
from flask_login import (
    login_user, login_required, logout_user, current_user
    )
from . import auth
from .forms import (
    RegisterPatient, LoginPatient, RegisterDoctor, LoginDoctor, RequestResetForm, ResetPasswordForm
    )
from .. import db
from ..models import (
    Patient,
    Doctor
    )
from werkzeug.exceptions import abort

from ..utils import (
    Target, 
    Username,
    SendMail,
    UserType,
    send_reset_email
    )

target = Target()
usernames = Username()
usertype = UserType()

@auth.route('/register/patient', methods=('GET', 'POST'))
@auth.route('/signup/patient',  methods=('GET', 'POST'))
def patient_register():
    if '_rs_' not  in g:
        g._rs_ = '_rs__'
        
    form = RegisterPatient()
    if form.validate_on_submit():
        patient = Patient(
            user='_pt_',
            title=form.title.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            dob=form.dob.data,
            education=form.education.data,
            marital_status=form.marital_status.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(patient)
        db.session.commit()

        ''' Set up the email notification for the doctor..'''
        subject = 'Registration Successful.'
        message = f'''Welcome {form.title.data} {form.last_name.data}.\n

        Thank you for joining our ever growing family at Doctor Patient Portal.
        '''
        recipients = [form.email.data]

        sendMail = SendMail()
        sendMail(subject, message, recipients)
        
        ''' Email notification set up done ..'''

        flash('Your registration was successful.')
        target.set_target('auth.patient_signin')
        return redirect(url_for('auth.flashing'))

    return render_template('auth/patient/register.html', form=form)


@auth.route('/signup/doctor', methods=('GET', 'POST'))
@auth.route('/register/doctor', methods=('GET', 'POST'))
def doctor_register():
    if '_rs_' not  in g:
        g._rs_ = '_rs__'
    
    form = RegisterDoctor()

    if form.validate_on_submit():
        doctor = Doctor(
            user='_dr_',
            title=form.title.data,
            speciality=form.speciality.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            address=form.address.data,
            bio=form.bio.data,
            phone=form.phone.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(doctor)
        db.session.commit()

        ''' Set up the email notification for the doctor..'''
        subject = 'Registration Successful.'
        message = f'''Welcome {form.title.data} {form.last_name.data}.\n

        Thank you for joining our ever growing family at Doctor Patient Portal.
        '''
        recipients = [form.email.data]

        sendMail = SendMail()
        sendMail(subject, message, recipients)
        
        ''' Email notification set up done ..'''

        flash('Doctor registration, successful.')
        target.set_target('auth.doctor_signin')

        return redirect(url_for('auth.flashing'))

    return render_template('auth/doctor/register.html', form=form)



@auth.route('/login/patient', methods=('GET', 'POST'))
@auth.route('/signin/patient', methods=('GET', 'POST'))
def patient_signin():
    if '_rs_' not  in g:
        g._rs_ = '_rs__'
    
    usertype.set_usertype('_pt_')
    
    form = LoginPatient()
    if form.register.data:
        return redirect(url_for('auth.patient_register'))
    
    if form.validate_on_submit():
                        
        patient = \
            Patient.query.filter_by(email=form.email.data).first()
        if patient is not None and patient.verify_password(form.password.data):

            if 'user' in g:
                g.pop('user', None)

            g.user = patient
            if 'user' in session:
                session.pop("user", None)

            session['user'] = g.user.user
            session['id'] = g.user.id

            usernames.set_username("{} {} {}".format(g.user.title, g.user.first_name, g.user.last_name))

            login_user(patient)         
            return redirect(url_for('auth.login'))

        else:
            flash(u'Invalid email or password', 'error')

    return render_template('auth/patient/login.html', form=form)

@auth.route('/login/doctor', methods=('GET', 'POST'))
@auth.route('/signin/doctor', methods=('GET', 'POST'))
def doctor_signin():
    if '_rs_' not  in g:
        g._rs_ = '_rs_'
    
    usertype.set_usertype('_dr_')
    
    form = LoginDoctor()
    
    if form.register.data:
        return redirect(url_for('auth.doctor_register'))
    
    if form.validate_on_submit():
                        
        doctor = \
            Doctor.query.filter_by(email=form.email.data).first()
        if doctor is not None and doctor.verify_password(form.password.data):

            if 'user' in g:
                g.pop('user', None)

            g.user = doctor
            if 'user' in session:
                session.pop("user", None)
            
            session['user'] = g.user.user
            session['id'] = g.user.id
            
            usernames.set_username("{} {} {}".format(g.user.title, g.user.first_name, g.user.last_name))

            login_user(doctor)
            return redirect(url_for('auth.login'))
        else:
            flash(u'Invalid email or password', 'error')
        
        

    return render_template('auth/doctor/login.html', form=form)

@auth.route('/login', methods=('GET', 'POST'))
def login():
    return redirect(url_for('home.dash_dpp'))

@auth.route('/logout')
@login_required
def logout():
    user = current_user.user
    logout_user()
    session.clear()
    flash('You have been logged out succesfully.')
    target.set_target('home.home_dpp')
    return redirect(url_for('auth.flashing'))


@auth.route('/flashing')
def flashing():
    return render_template('auth/flashing.html', target = target.get_target()) # display the flashes, then


@auth.route('/reset_password', methods=('GET', 'POST'))
def reset_request():
    if '_rs_' not  in g:
        g._rs_ = '_rs_'
    print(usertype.get_usertype())
    if current_user.is_authenticated:
        return redirect(url_for('home.home_dpp'))
    
    form = RequestResetForm()

    if form.validate_on_submit():
        if usertype.get_usertype() == '_pt_':
            user = Patient.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.')
            '''Redirect to emails'''
            target.set_target('auth.patient_signin')
            return redirect(url_for('auth.flashing'))
        
        if usertype.get_usertype() == '_dr_':
            user = Doctor.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.')
            '''Redirect to emails'''
            target.set_target('auth.doctor_signin')
            return redirect(url_for('auth.flashing'))
    
    return render_template('auth/reset_request.html', form=form)


@auth.route('/reset_password/<token>', methods=('GET', 'POST'))
def reset_token(token):
    if '_rs_' not  in g:
        g._rs_ = '_rs_'
    print(usertype.get_usertype())

    if current_user.is_authenticated:
        return redirect(url_for('home.home_dpp'))
    
    if usertype.get_usertype():
        if usertype.get_usertype() == '_pt_':
            user = Patient.verify_reset_token(token)
        
        if usertype.get_usertype() == '_dr_':
            user = Doctor.verify_reset_token(token)
    else:
        return redirect(url_for('home.home_dpp'))
    if user is None:
        flash('That is an invalid or expired token.')
        target.set_target('auth.reset_request')
        return redirect(url_for('auth.flashing'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated!')
        if usertype.get_usertype() == '_dr_':
            target.set_target('auth.doctor_signin')

        if usertype.get_usertype() == '_pt_':
            target.set_target('auth.patient_signin')

        return redirect(url_for('auth.flashing'))
    
    return render_template('auth/reset_password.html', form=form)

        
    
    
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('id')

    if user_id is None:
        g.user = None
    else:
        if  session.get('user') == '_dr_': # For Doctor
            g.user = Doctor.query.filter_by(id=user_id).first()
        if session.get('user') == '_pt_': #For Patient
            g.user = Patient.query.filter_by(id=user_id).first()