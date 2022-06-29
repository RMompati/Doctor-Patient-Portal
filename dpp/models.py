from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import session, current_app

from . import db, login_manager

# Set up the Patient table and tables it has relationships with.
class Patient(UserMixin, db.Model):

    __tablename__ = 'patients'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user = db.Column(# User type
        db.String(10),
        index=False,
        nullable=False
    )
    title = db.Column(
        db.String(10),
        nullable=False
    )
    first_name = db.Column(
        db.String(30),
        nullable=False
    )
    last_name = db.Column(
        db.String(30),
        nullable=False
    )
    gender = db.Column(
        db.String(5),
        nullable=False
    )
    dob = db.Column(
        db.DateTime,
        nullable=False
    )
    education = db.Column(
        db.String(50),
        nullable=False
    )
    marital_status = db.Column(
        db.String(15),
        nullable=False
    )
    address = db.Column(
        db.String(100),
        nullable=False
    )
    phone = db.Column(
        db.String(15),
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    h_password = db.Column(
        db.String(80),
        nullable=False
    )
    """ Relationships """
    feedback = db.relationship('Feedback', backref='author', lazy=True)
    medical_survey = db.relationship('MedicalSurvey', backref='patient', lazy=True)
    appointments = db.relationship('Booking', backref='booker', lazy=True)

    @property
    def password(self):
        raise AttributeError('Password is not accessible.')

    @password.setter
    def password(self, password):
        self.h_password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.h_password, password)

    '''Password Reset '''
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return Patient.query.get(user_id)


class MedicalSurvey(db.Model):
    __tablename__ = 'medicalsurveys'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patients.id')
    )
    completed = db.Column(
        db.DateTime,
        nullable=False
    )
    qas = db.relationship('QA', backref='survey', lazy=True)

class QA(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    survey_id = db.Column(
        db.Integer,
        db.ForeignKey('medicalsurveys.id')
    )
    questions_list = db.Column(
        db.Text,
        nullable=False
    )
    answers_list = db.Column(
        db.Text,
        nullable=False
    )
    answers_desc_list = db.Column(
        db.Text,
        nullable=False
    )
    
# Set up the Admin table
class Admin(UserMixin, db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True 
    )
    user = db.Column(# User type
        db.String(10),
        index=False,
        nullable=False
    )
    first_name = db.Column(
        db.String(30),
        nullable=False
    )
    last_name = db.Column(
        db.String(30),
        nullable=False
    )
    email = db.Column(
        db.String(50),
       nullable=False,
       unique=True
    )
    h_password = db.Column(
        db.String(80),
        nullable=False
    )

    @property
    def password(self):
        raise AttributeError('Password is not accessible.')

    @password.setter
    def password(self, password):
        self.h_password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.h_password, password)
    
    
    '''Password Reset '''
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return Admin.query.get(user_id)

# Set up the Doctor Table and Tables it has relationships with.

class Doctor(UserMixin, db.Model):

    __tablename__ = 'doctors'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user = db.Column(# User type
        db.String(10),
        index=False,
        nullable=False
    )
    title = db.Column(
        db.String(10),
        nullable=False
    )
    speciality = db.Column(
        db.String(30),
        nullable=False
    )
    first_name = db.Column(
        db.String(30),
        nullable=False
    )
    last_name = db.Column(
        db.String(30),
        nullable=False
    )
    gender = db.Column(
        db.String(5),
        nullable=False
    )
    address = db.Column(
        db.String(100),
        nullable=False
    )
    bio = db.Column(
        db.Text,
        nullable=False
    )
    phone = db.Column(
        db.String(15),
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    h_password = db.Column(
        db.String(80),
        nullable=False
    )
    """ Relationships """
    schedule = db.relationship('Schedule', backref='doctor', lazy=True)
    appointments = db.relationship('Booking', backref='doctor', lazy=True)

    @property
    def password(self):
        raise AttributeError('Password is not accessible.')

    @password.setter
    def password(self, password):
        self.h_password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.h_password, password)
    
    '''Password Reset '''
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return Doctor.query.get(user_id)
    

@login_manager.user_loader
def load_user(user_id):
    if session['user'] == '_pt_':
        return Patient.query.get(int(user_id))
    elif session['user'] == '_dr_':
        return Doctor.query.get(int(user_id))
    elif session['user'] == '_ad_':
        return Admin.query.get(int(user_id))
    else:
        return None

class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey('doctors.id'),
        nullable=False
    )
    title = db.Column(
        db.String(50),
        nullable=False
    )
    start = db.Column(
        db.DateTime,
        unique=True,
        nullable=False
    )
    end = db.Column(
        db.DateTime,
        unique=True,
        nullable=False
    )
    allDay = db.Column(
        db.Boolean,
        nullable=False
    )

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patients.id'),
        nullable=False
    )
    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey('doctors.id'),
        nullable=False
    )
    title = db.Column(
        db.String(50),
        nullable=False
    )
    start = db.Column(
        db.DateTime,
        nullable=False
    )
    end = db.Column(
        db.DateTime,
        nullable=False
    )

class Feedback(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patients.id'),
        nullable=False
    )
    subject = db.Column(
        db.String(100),
        nullable=False
    )
    post = db.Column(
        db.Text,
        nullable=False
    )
    posted = db.Column(
        db.Date,
        nullable=False
    )