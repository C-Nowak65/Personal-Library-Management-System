from flask import render_template, redirect, url_for, flash
from sqlalchemy import desc
from .models import db, Books, User
from .forms import BookForm, RegistrationForm, LoginForm, ProfileUpdateForm
from . import app
from flask_login import login_user, login_required, current_user, logout_user
from flask_bcrypt import Bcrypt

bcrypt =  Bcrypt(app)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    '''A Method to add books.'''
    form = BookForm()
    if form.validate_on_submit():
        app.logger.info(f"user_id: {current_user.user_id} adding book. ")
        try:
            new_book = Books(title=form.title.data, author=form.author.data, genre=form.genre.data, start_date=form.start_date.data, end_date=form.end_date.data, status=form.status.data, rating=form.rating.data)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!')
            app.logger.info(f"Book added successfully.")
        except Exception as e:
            flash(f"Error fetching books: {e}")
            app.logger.error(f"Error fetching books: {e}")
        return redirect(url_for('index'))
    return render_template('add_book.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''A Method to register a user.'''
    form = RegistrationForm()
    if form.validate_on_submit():
        app.logger.info("New user attempting to register.")
        try:
            new_user = User(user_name=form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered.')
            app.logger.info("New user registered.")
        except Exception as e:
            flash(f"Error registering user: {e}")
            app.logger.error(f"Error registering user: {e}")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''A method to login a user.'''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            app.logger.info(f"User {user.user_name} successfully logged in.")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.")
            app.logger.info(f"Failed login attempt for username: {form.username.data}")
    return render_template('login.html', form=form)

@app.route('/my_books')
@login_required
def my_books():
    '''A Method to show all of a users books.'''
    user_books = Books.query.filter_by(user_id=current_user.user_id).all()
    return render_template('my_books.html', books=user_books)

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    '''A method to allow users to edit their own books.'''
    book = Books.query.get_or_404(book_id)
    if book.user_id != current_user.user_id:
        flash('Book does not exist.')
        return redirect(url_for('index'))
    
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.genre = form.genre.data
        book.start_date = form.start_date.data
        book.end_date = form.end_date.data
        book.status = form.status.data
        book.rating = form.rating.data
        db.session.commit()
        flash('Book updated successfully!')
        return redirect(url_for('my_books'))
    
    return render_template('edit_book.html', form=form)

@app.route('/all_books')
def all_books():
    '''A method to show all books and which user added the book.'''
    books = Books.query.all()
    return render_template('all_books.html', books=books)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.')
    return redirect(url_for('index'))

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = User.query.get(current_user.user_id)

    form = ProfileUpdateForm(obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.set_password(form.password.data)
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('index'))
    
    return render_template('update_profile.html', form=form)
    

