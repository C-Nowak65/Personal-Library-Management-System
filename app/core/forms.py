from .models import BookStatus
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    '''A Class to handle the login form.'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    '''A class to handle the registration form.'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Sign Up')

class ProfileUpdateForm(FlaskForm):
    '''A class to handle the profile update form.'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Update Profile')

class BookForm(FlaskForm):
    '''A class to handle the book form.'''
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()]) 
    start_date = DateTimeField('Start Date xx-xx-xxxx', format='%m-%d-%Y')
    end_date = DateTimeField('End Date (ex. xx-xx-xxxx)', format='%m-%d-%Y')
    status = SelectField('Book Status', choices=[(status.name, status.value) for status in BookStatus])
    rating = FloatField('Rating out of 5')
    submit = SubmitField('Submit')


