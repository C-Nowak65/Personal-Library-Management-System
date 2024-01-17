from flask import Blueprint, render_template, url_for, flash, redirect, current_app
from .models import Books, User, db
from app.core.forms import BookForm, RegistrationForm, LoginForm, ProfileUpdateForm
from flask_login import login_user, login_required, current_user, logout_user


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@login_required
@main.route('/add_book', methods=['GET', 'POST'])
def add_book():
    '''A Method to add a book.'''
    form = BookForm()
    if form.validate_on_submit():
        current_app.logger.info(f'{current_user.user_id} is registering a book.')
        try:
            new_book = Books(title=form.title.data, author=form.author.data, genre=form.genre.data, start_date=form.start_date.data, end_date=form.end_date.data, status=form.status.data, rating=form.rating.data, user_id=current_user.user_id)
            db.session.add(new_book)
            db.session.commit()
            flash('Book Registered Successfully!')
            current_app.logger.info(f'{current_user.user_id} has registered a book successfully!')
        except Exception as e:
            flash('Error registering Books!')
            current_app.logger.error(f'Error registering: {e}')
        return redirect(url_for('main.my_books'))
    return render_template('add_book.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    '''A Method to register a user.'''
    form = RegistrationForm()
    if form.validate_on_submit():
        current_app.logger.info("New user attempting to register.")
        try:
            new_user = User(user_name=form.username.data, user_password=form.password.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered.')
            current_app.logger.info("New user registered.")
        except Exception as e:
            flash(f"Error registering user: {e}")
            current_app.logger.error(f"Error registering user: {e}")
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    '''A method to login a user.'''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            current_app.logger.info(f"User {user.user_name} successfully logged in.")
            return redirect(url_for('main.home'))
        else:
            flash("Invalid username or password.")
            current_app.logger.info(f"Failed login attempt for username: {form.username.data}")
    return render_template('login.html', form=form)

@main.route('/my_books')
@login_required
def my_books():
    '''A Method to show all of a users books.'''
    user_books = Books.query.filter_by(user_id=current_user.user_id).all()
    return render_template('my_books.html', user_books=user_books)

@main.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    '''A method to allow users to edit their own books.'''
    book = Books.query.get_or_404(book_id)
    if book.user_id != current_user.user_id:
        flash('Book does not exist.')
        return redirect(url_for('main.home'))
    
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
        return redirect(url_for('main.my_books'))
    
    return render_template('edit_book.html', form=form)

@main.route('/all_books')
def all_books():
    '''A method to show all books and which user added the book.'''
    books = Books.query.all()
    return render_template('all_books.html', books=books)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.')
    return redirect(url_for('main.home'))

@main.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = User.query.get(current_user.user_id)

    form = ProfileUpdateForm(obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.set_password(form.password.data)
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('main.home'))
    
    return render_template('update_profile.html', form=form)
    

