from flask import session,render_template, redirect, url_for, flash, request, get_flashed_messages
from LarpBook.Auth import bp
from flask_login import current_user, login_user
from LarpBook.Models import models
from LarpBook.extensions import bcrypt, login_manager
from LarpBook.Utils.Forms.forms import LoginForm, RegistrationForm
from datetime import datetime
from LarpBook import db

@bp.route('/')
def index():

    return render_template('auth/index.html')

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        print(f"Attempting to log in user {username}.")
        password = form.password.data
        print(f"Password entered: {password}")
        print(f"Hashed password: {bcrypt.generate_password_hash(password).decode('utf-8')}")

        user = models.User.query.filter_by(username = username).first()
        if user:
            print(f"User found: {user.username}")
            print(f"User password: {user.password}")
        else:
            print(f"User not found.")

        if username and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=form.remember.data)
            print(f"User {user} logged in successfully.")
            return redirect(url_for('main.index'))
        else:
            flash('Login failed. Please check your username and password.', 'error')
            messages = get_flashed_messages(with_categories=True)
            print(messages)
            print(f"Login failed, please try again.")
    return render_template('auth/login.html', form=form)

@bp.route('/logout/')
def logout():
    # Clear the session data
    session.clear()
    # redirect the user to the index page
    return redirect(url_for('main.index'))

@bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Create a new user object from the dorm
            new_user = models.User(
                username=form.username.data,
                password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                birth_date=form.birth_date.data,
                date_joined=datetime.now(),
                is_organiser=form.is_organiser.data
            )

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Create auxiliary user objects
            user_id = new_user.id

            new_user_contact = models.UserContact(
                user = user_id,
                contact_type = 'email',
                contact_value = form.email.data,
                description = 'Primary email address'
            )

            new_user_album = models.Album(
                name = 'default',
                description = 'Default album for {User.username}',
                cover_image_id = 1,
                user_id = user_id,
                event_id = None
            )

            new_user_wall = models.UserWall(
                user = user_id,
            )

            db.session.add(new_user_contact)
            db.session.add(new_user_album)
            db.session.commit()
            return redirect(url_for('auth.registration_success'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.')
            print(f"Error during registration: {str(e)}")

    return render_template('auth/register.html', form = form)

@bp.route('/registration_success/')
def registration_success():
    return render_template('auth/registration_success.html')

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))