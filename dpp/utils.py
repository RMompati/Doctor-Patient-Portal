from wtforms.validators import ValidationError
from flask_mail import Message
from . import mail
from flask import url_for

class Target(object):
    def __init__(self, target=None):
        self.set_target(target)
    
    def set_target(self, target):
        self.target= target
    
    def get_target(self):
        return self.target

class Username(object):
    def __init__(self, username='Unknown User'):
        self.set_username(username)
    
    def set_username(self, username):
        self.username = username
    
    def get_username(self):
        return self.username

class GreaterThan(object):
    """
    Compares values of two fields.

    :param fieldname:
        The name of the other field to aid the comparison
    :param message:
        Error message to raise in case of validation error.
    """

    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message
    
    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name \'%s\'.")%(self.fieldname))

        if field.data < other.data or field.data == other.data:
            d = {
                'other_label' : hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name' : self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('End date/time must be greater than %(other_name)s date/time.')
            
            raise ValidationError(message % d)

class SendMail(object):

    def __init__(self):
        ''' Initialized '''
    
    def __call__(self, subject, message, recipients):
        msg = Message(
            subject=subject,
            sender='dpp.system.admi@gmail.com',
            recipients=recipients
        )
        msg.body = message

        mail.send(msg)

class Format(object):
    '''
    A class to format the schedules in a proper format before, the
    data is passed on the the javascrip code.
    '''
    def __init__(self):
        ''' Initialized '''
    
    def __call__(self, schedules):
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
        
        return data

class Choices(object):

    def __init__(self, choices=[]):
        self.set_choices(choices)
    
    def set_choices(self, choices):
        self.choices = choices
    
    def get_choices(self):
        return self.choices
    
    def __call__(self):
        return self.choices

class UserType(object):
    def __init__(self, user_type=None):
        ''' Initialized '''
        self.set_usertype(user_type)
    
    def set_usertype(self, user_type):
        self.user_type = user_type
    
    def get_usertype(self):
         return self.user_type

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request', 
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = \
        f'''Doctor Patient Portal
    
        To reset your password, visit the following link: {url_for('auth.reset_token', token=token, _external=True)}
    


        If you did not make this request then simply ignore this email no changes will be made.
        '''
    mail.send(msg)



questions = [
    'Has your doctor ever said your blood pressure was too hign or too low ?',
    'Do you have any know cardiovascular problems (abnormal ECG, previous heart attack, etc) ?',
    'Has your doctor ever told you that your cholestrol was too high ?',
    'Have you (or family member) ever been told that you have diabetes ?',
    'Do you have any injuries or orthopedic problems (back, knees, etc) ?',
    'Do your have stiff or sollwen joints ?',
    'Do you have tension or sorness in any area ?',
    'Are you taking any prescribed medication or dietary suplementation ?',
    'Do you have problems sleeping ?',
    'Are you pregnant or post-partum(< 6 weeks) ?',
    'Have you ever been advised by a doctor, physician or speciaist not to perform any type of exercise/activity ?',
    'Do you have any other mdeical condition, injury or anything else we should be aware of we have not mentioned ?'
]
