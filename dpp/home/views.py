from flask import (
    render_template, g, flash, redirect, url_for, session
    )
from flask_login import login_required, current_user
from .. import db
from . import home
from .forms import (
    CreateSchedule, CreateAppointment, Survey, ConfirmSchedule, FeedbackForm
    )

from ..models import (
    Schedule, Doctor, Patient, Booking, MedicalSurvey, QA, Feedback
    )
from ..auth.views import (
    usernames, target
    )

from ..admin.views import (
    usernames as un, target as tg
)

from ..utils import (
    SendMail, Format, Choices
)
from datetime import date
import time

choices = Choices()

@home.route('/', methods=('GET', 'POST'))
@home.route('/home', methods=('GET', 'POST'))
def home_dpp():
    if '_rs_'  in g:
        g.pop('_rs__', None)
    
    doctors = Doctor.query.all()
    data = []
    
    if doctors is not None:
        for doctor in doctors:
            data.append(
                {'names': '{} {}'.format(doctor.first_name, doctor.last_name),
                'speciality': doctor.speciality,
                'bio': doctor.bio,
                'gender': doctor.gender
                }
            )

    form = FeedbackForm()
    
    if form.validate_on_submit():
    
        patient = Patient.query.filter_by(email=form.email.data).first()
        print(f'Patient : {patient}')
    
        if patient is not None:
            print("[INFO] in not NONE")
            feedback = Feedback(
                subject=form.subject.data,
                post=form.message.data,
                posted=date.today(),
                author=patient
            )
    
            db.session.add(feedback)
            db.session.commit()
    
            flash('Feedback sent.')
            time.sleep(5.0)
    
            print("[INFO] Moving on.")
    
            target.set_target('home.home_dpp')
            return redirect(url_for("auth.flashing"))
            
            
    return render_template('dpp/index.html', data=data, form=form)

@home.route('/dpp')
@login_required
def dash_dpp():
    
    usernames.set_username('{} {} {}'.format(current_user.title, current_user.first_name, current_user.last_name))
    username = usernames.get_username()
    data = None
    notifications = []
    
    if current_user.user == '_dr_':
        data = Booking.query.filter_by(doctor_id=current_user.id).all()
        schedules = Schedule.query.filter_by(doctor_id=current_user.get_id()).all()
        appointments = Booking.query.filter_by(doctor_id=current_user.get_id()).all()
        
        ids = [schedule.id for schedule in schedules if schedule.end.strftime('%Y-%m-%d %H:%M:%S') < date.today().strftime('%Y-%m-%d %H:%M:%S')]
        for i in ids:
            Schedule.query.filter_by(id=i).delete()
        db.session.commit()

        ids = [appointment.id for appointment in appointments if appointment.end.strftime('%Y-%m-%d %H:%M:%S') < date.today().strftime('%Y-%m-%d %H:%M:%S')]
        for i in ids:
            Booking.query.filter_by(id=i).delete()

        db.session.commit()

    if current_user.user == '_pt_':
        
        appointments = Booking.query.filter_by(patient_id=current_user.get_id()).all()
        ids = [appointment.id for appointment in appointments if appointment.end.strftime('%Y-%m-%d %H:%M:%S') < date.today().strftime('%Y-%m-%d %H:%M:%S')]

        for i in ids:
            Booking.query.filter_by(id=i).delete()
        
        db.session.commit()
            
    
    if data:
        for d in data:
            patient = Patient.query.filter_by(id=d.patient_id).first()
            notifications.append(['{} {}'.format(patient.title, patient.last_name), d.start.strftime('%Y-%m-%d %H:%M:%S')])
    
    session['notifications'] = notifications
    
    return render_template('dpp/welcome.html', notifications=notifications, username=username)

@home.route('/dpp/admin')
@login_required
def admin():
    un.set_username('Admin : {} {}'.format(current_user.first_name, current_user.last_name))
    username = un.get_username()
    return render_template('dpp/admin_dash.html', username=username)

@home.route('/dpp/view/schedule')
@login_required
def view_schedule():

    usernames.set_username('{} {} {}'.format(current_user.title, current_user.first_name, current_user.last_name))
    username = usernames.get_username()
    
    schedules = Schedule.query.filter_by(doctor_id=current_user.get_id()).all()

    if len(schedules) == 0:
        target.set_target('home.create_schedule')
        flash('Your schedule is clear... you will be redirected to a schedule creation page..')
        return redirect(url_for('auth.flashing'))
    
    data = []
    for schedule in schedules:
        data.append({
            'title' : schedule.title,
            'start' : {
                'y' : schedule.start.strftime('%Y'),
                'm' : schedule.start.strftime('%m'),
                'd' : schedule.start.strftime('%d'),
                'h' : schedule.start.strftime('%H'),
                'M' : schedule.start.strftime('%M'),
                's' : schedule.start.strftime('%S')
            },
            'end' : { # schedule.end.strftime('%Y-%m-%d %H:%M:%S')
                'y' : schedule.end.strftime('%Y'),
                'm' : schedule.end.strftime('%m'),
                'd' : schedule.start.strftime('%d'),
                'h' : schedule.end.strftime('%H'),
                'M' : schedule.end.strftime('%M'),
                's' : schedule.end.strftime('%S')
            },
            'allDay' : schedule.allDay,
        })

    return render_template('dpp/schedule.html', notifications=session.get('notifications'), username= username, data=data)

@home.route('/dpp/create/schedule', methods=('GET', 'POST'))
@login_required
def create_schedule():

    usernames.set_username('{} {} {}'.format(current_user.title, current_user.first_name, current_user.last_name))
    username = usernames.get_username()

    form = CreateSchedule()

    if form.validate_on_submit():
        schedule = Schedule(
            title=form.title.data,
            start=form.start.data,
            end=form.end.data,
            allDay=form.allDay.data,
            doctor=current_user
        )
        db.session.add(schedule)
        db.session.commit()
        flash('Your schedule creation was successful.')
        target.set_target('home.dash_dpp')
        return redirect(url_for('auth.flashing'))

    return render_template('dpp/update.html', username = username, form=form)

@home.route('/dpp/create/appointment', methods=('GET', 'POST'))
@login_required
def create_appointment():

    usernames.set_username('{} {} {}'.format(current_user.title, current_user.first_name, current_user.last_name))
    username = usernames.get_username()

    form = CreateAppointment()
    confirm = ConfirmSchedule()
    """Get all the doctors from the database and populate the choices with their specialities"""
    doctors = Doctor.query.all()
    specialities = [s.speciality for s in set(doctors)]
    form.speciality.choices = list(set(specialities))
    confirm.speciality.choices = list(set(specialities))

    if confirm.update.data:
        
        doctors = Doctor.query.filter_by(speciality=f'{form.speciality.data}').all()
        confirm.doctor.choices = ['{} {}'.format(d.first_name, d.last_name) for d in doctors]
        form.doctor.choices = ['{} {}'.format(d.first_name, d.last_name) for d in doctors]
        choices.set_choices(['{} {}'.format(d.first_name, d.last_name) for d in doctors])

        return render_template('dpp/appointment.html', username=username, form=form, confirm=confirm, data=[],dr=None)

    if confirm.update_schedule.data:
        names = str(form.doctor.data).split(' ')
        if len(names) > 1:
                
            doc = Doctor.query.filter_by(first_name=names[0], last_name=names[1]).first()
            schedules = Schedule.query.filter_by(doctor_id=doc.id).all()

            data_format = Format()
            data = data_format(schedules)
            confirm.doctor.choices = choices.get_choices()
            form.doctor.choices = choices.get_choices()

            return render_template('dpp/appointment.html', username=username, form=form, confirm=confirm, data=data, dr=names[1])
        else:
            return render_template('dpp/appointment.html', username=username,  form=form, confirm=confirm, data=[],dr=None)

        return render_template('dpp/appointment.html', username=username, form=form, confirm=confirm, data=[],dr=None)
    
    
    if form.cancel.data:
        return redirect(url_for('home.dash_dpp'))
    
    if len(form.speciality.choices) == 0:
        flash('There are currently no doctors registerd on the system..')
        target.set_target('home.dash_dpp')
        return redirect(url_for('auth.flashing'))
    

    if form.validate_on_submit():
        names = str(form.doctor.data).split(' ')
        doctor = Doctor.query.filter_by(first_name=names[0], last_name=names[1]).first()
    
        booking = Booking(
            title=form.title.data,
            start=form.start.data,
            end=form.end.data,
            booker=current_user,
            doctor=doctor
        )
    
        schedule = Schedule(
            title='Appointment with {} {}'.format(current_user.title, current_user.last_name),
            start=form.start.data,
            end=form.end.data,
            allDay=False,
            doctor=doctor
        )
    
        db.session.add(schedule)
        db.session.add(booking)
        db.session.commit()
        ''' Set up the email notification for the doctor..'''
        #booking = Booking.query.filter_by(start=form.start.data)
        subject = '{}'.format(form.title.data)
        message = f'''Hello Dr {doctor.last_name} you have an appointment with {current_user.title} {current_user.last_name} on {form.start.data.strftime('%Y-%m-%d')} at {form.start.data.strftime('%H:%M:%S')}.
        
        Please ignore if this message is not for you.
        '''
        recipients = [doctor.email]

        sendMail = SendMail()
        sendMail(subject, message, recipients)

        ''' Email notification set up done ..'''

        flash('Appointment booked successfully.')

        target.set_target('home.dash_dpp')
        return redirect(url_for('auth.flashing'))
    
    return render_template('dpp/appointment.html', username=username, form=form, confirm=confirm, data=[],dr=None)

@home.route('/dpp/appointment/view', methods=('GET', 'POST'))
@login_required
def view_appointments():

    usernames.set_username('{} {} {}'.format(current_user.title, current_user.first_name, current_user.last_name))
    username = usernames.get_username()

    appointments = Booking.query.filter_by(patient_id=current_user.get_id()).all()
    

    if len(appointments) == 0:
        target.set_target('home.create_appointment')
        flash('You do not have any appointments at the moment... let us help you book one..')
        return redirect(url_for('auth.flashing'))
    
    data = []
    for appointment in appointments:
        d = Doctor.query.filter_by(id=appointment.doctor_id).first()
        data.append({
            'title' : '{} with Dr. {}'.format(appointment.title, d.last_name ),
            'start' : {
                'y' : appointment.start.strftime('%Y'),
                'm' : appointment.start.strftime('%m'),
                'd' : appointment.start.strftime('%d'),
                'h' : appointment.start.strftime('%H'),
                'M' : appointment.start.strftime('%M'),
                's' : appointment.start.strftime('%S')
            },
            'end' : { # appointment.end.strftime('%Y-%m-%d %H:%M:%S')
                'y' : appointment.end.strftime('%Y'),
                'm' : appointment.end.strftime('%m'),
                'd' : appointment.start.strftime('%d'),
                'h' : appointment.end.strftime('%H'),
                'M' : appointment.end.strftime('%M'),
                's' : appointment.end.strftime('%S')
            },
            'allDay' : False,
        })

    return render_template('dpp/appointments.html', username= username, data=data)


@home.route('/dpp/survey/medical', methods=('GET', 'POST'))
@login_required
def medical_survey():
    usernames.set_username('{} {} {}'.format(current_user.title, current_user.first_name, current_user.last_name))
    username = usernames.get_username()

    form = Survey()

    if form.validate_on_submit():
    
        questions = [
            form.q_1.label.text, form.q_2.label.text, form.q_3.label.text,
            form.q_4.label.text, form.q_5.label.text, form.q_6.label.text,
            form.q_7.label.text, form.q_8.label.text, form.q_9.label.text,
            form.q_10.label.text, form.q_11.label.text, form.q_12.label.text
        ]
    
        answers = [
            form.q_1.data, form.q_2.data, form.q_3.data, form.q_4.data, form.q_5.data,
            form.q_6.data, form.q_7.data, form.q_8.data, form.q_9.data, form.q_10.data,
            form.q_11.data, form.q_12.data
        ]
    
        descriptions = [
            form.answer_desc_1.data, form.answer_desc_2.data,
            form.answer_desc_3.data, form.answer_desc_4.data,
            form.answer_desc_5.data, form.answer_desc_6.data,
            form.answer_desc_7.data, form.answer_desc_8.data,
            form.answer_desc_9.data, form.answer_desc_10.data,
            form.answer_desc_11.data, form.answer_desc_12.data
        ]

        questions = ', '.join(questions)
        answers = ', '.join(answers)
        descriptions = ', '.join(descriptions)
        
        survey = MedicalSurvey(patient=current_user, completed=date.today())
        qa = QA(
            questions_list=questions,
            answers_list=answers,
            answers_desc_list=descriptions,
            survey=survey
        )
        db.session.add(survey)
        db.session.add(qa)
        db.session.commit()
        
        flash('Medical Survey completed successfully.')
        target.set_target('home.dash_dpp')
        return redirect(url_for('auth.flashing'))

    return render_template('dpp/survey.html', username=username, form= form)

@home.route('/dpp/patient/feedback', methods=('GET', 'POST'))
def feedback():
    if '_rs_' not  in g:
        g._rs_ = '_rs_'
    feedback = Feedback.query.all()
    data = []
    if feedback is not None:
        for feed in feedback:
            data.append(
                {'names': '{} {}'.format(feed.author.first_name, feed.author.last_name),
                'posted': feed.posted,
                'subject': feed.subject,
                'post': feed.post
                }
            )
    return render_template('feedback/posts.html', data=data)
    