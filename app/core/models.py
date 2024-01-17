from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from enum import Enum

db = SQLAlchemy()
cache = Cache()
bcrypt = Bcrypt()

class User(db.Model):
    '''A class to handle the user Model.'''
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Unicode(64))
    user_password = db.Column(db.Unicode(128))
    books = db.relationship('Books', backref='user', lazy='dynamic')

    def __init__(self, user_name, user_password):
        '''A method to initialize the user Class.'''
        self.user_name = user_name
        self.user_password = user_password

    def is_authenticated(self):
        '''A method to authenticate a user.'''
        return True
    
    def is_active(self):
        '''A method to make the user active.'''
        return True
  
    def get_id(self):
        '''A method to return the unique identifier for the user to manage user sessions.'''
        return self.user_id
    
    def __unicode__(self):
        '''A method to return the username in unicode format.'''
        return self.user_name
    
    def set_password(self, password):
        '''A method to hash the given password and store it as the users password.'''
        self.user_password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        '''A method to check a given password versus the stored hashed password.'''
        return bcrypt.check_password_hash(self.user_password, password)
    
class BookStatus(Enum):
    '''A class to handle the overall status of books.'''
    WANT_TO_READ = "Want to read"
    CURRENTLY_READING = "Currently reading"
    DONE = "Done"
    
class Books(db.Model):
    '''A class uses to handle the book model.'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    genre = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.Enum(BookStatus))
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def update_status(self, new_status):
        '''A method to update the status of the book.'''
        self.status = new_status

    def format_book_details(self):
        '''A method to return a formatted representation of the book.'''
        return f"Title: {self.title}. Author: {self.author}, Genre: {self.genre}"
    

    def is_reading(self):
        '''A method to check if the book is currently being read.'''
        return self.status == BookStatus.CURRENTLY_READING
    
    def is_want_to_read(self):
        '''A method to check if the book is currently want to be read.'''
        return self.status == BookStatus.WANT_TO_READ
    
    def is_done(self):
        '''A Method to check if a book is done.'''
        return self.status == BookStatus.DONE
    
    def set_rating(self, rating):
        '''A mthod to set or update the rating of the book.'''
        self.rating = rating

