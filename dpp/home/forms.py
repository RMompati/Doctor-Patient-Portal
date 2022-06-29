from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, InputRequired, Email

from ..utils import GreaterThan

from ..utils import questions
from ..auth.views import g

class CreateSchedule(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=30)], render_kw={'placeholder': 'Title'})
    start = DateTimeField('Start', validators=[DataRequired()], render_kw={'placeholder' : 'yyyy-mm-dd hh:ii:ss'})
    end = DateTimeField('End', validators=[DataRequired(), GreaterThan('start')], render_kw={'placeholder' : 'yyyy-mm-dd hh:ii:ss'})
    allDay = BooleanField('AllDay', default=False)
    submit = SubmitField('Submit')
    


class CreateAppointment(FlaskForm):
    speciality = SelectField('Speciality')
    doctor = SelectField('Doctor', validate_choice=False)
    title = StringField('Title',validators=[DataRequired()], render_kw={'placeholder' : 'Title'})
    start = DateTimeField('Start', validators=[DataRequired()], render_kw={'placeholder' : 'yyyy-mm-dd hh:ii:ss', 'id': 'datetimepicker'} )
    end = DateTimeField('End', validators=[DataRequired(), GreaterThan('start')], render_kw={'placeholder' : 'yyyy-mm-dd hh:ii:ss', 'id':'datetimepicker'})
    create = SubmitField('Create')
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

class ConfirmSchedule(FlaskForm):
    speciality = SelectField('Speciality')
    doctor = SelectField('Doctor')
    update = SubmitField('01. Update Doctor Field', render_kw={'formnovalidate': True,'class':"btn btn-primary btn-lg btn-block"})
    update_schedule = SubmitField('02. Update Doctor\' Schedule', render_kw={'formnovalidate': True,'class':"btn btn-primary btn-lg btn-block"})

class UpdateAppointment(FlaskForm):
    pass

class DeleteAppointment(FlaskForm):
    pass

class Survey(FlaskForm):
    q_1 = StringField(questions[0], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_1 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : 'He/she said it eas due to ... and as a result my bp was too ....'})

    q_2 = StringField(questions[1], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_2 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : 'I had a heart attack a few years ago, and ..'})
    
    q_3 = StringField(questions[2], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_3 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : 'I have a good diet.'})
    
    q_4 = StringField(questions[3], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_4 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : 'My aunt recieved suh news.'})

    q_5 = StringField(questions[4], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_5 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : 'My back hurts sometimes.'})
    
    q_6 = StringField(questions[5], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_6 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : '.....'})
    
    q_7 = StringField(questions[6], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_7 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : '.....'})

    q_8 = StringField(questions[7], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_8 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : 'I am taking high blood pressure medication, and also medication for ...'})
    
    q_9 = StringField(questions[8], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_9 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : '.....'})
    
    q_10 = StringField(questions[9], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_10 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : 'I am 5 weeks pregnant | I am a male.'})

    q_11 = StringField(questions[10], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_11 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : 'I was advised to refrain from intense physical exercies..'})
    
    q_12 = StringField(questions[11], validators=[DataRequired()], render_kw={'placeholder' : 'Yes | No'})
    answer_desc_12 = TextAreaField('Please provide details', validators=[DataRequired()], render_kw={'placeholder' : 'I\'ve been diagnosed with .... I have a groin problem...'})
    submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired(), Email()])
    subject = StringField(validators=[InputRequired()])
    message = TextAreaField(validators=[InputRequired()])
    send = SubmitField("Send Message")