from flask import session,render_template, redirect, url_for, flash, request, get_flashed_messages
from LarpBook.Auth import bp
from flask_login import current_user, login_user, logout_user
from LarpBook.Models.models import User, Tags, Image, Album, UserWall, UserContact
from LarpBook.extensions import bcrypt, login_manager
from LarpBook.Static.Forms.forms import LoginForm, RegistrationForm
from LarpBook.Utils import authorisation
from datetime import datetime
from LarpBook import db

@bp.route('/')
def index():

    return render_template('auth/index.html')

def is_user_logged_in():
    return current_user.is_authenticated

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('Login failed. Please check your username and password.', 'error')
    return render_template('auth/login.html', form=form)

@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register/', methods=['GET', 'POST'])
def register():
    logged_in = authorisation.is_user_logged_in()
    form = RegistrationForm()
    if form.validate_on_submit():
        try:

            # Check if the interest tags already exist
            user_tags = []
            tag_names = [tag.strip().lower for tag in form.tags.data.split(',')]
            unique_tags = set(tag_names)
            for tag_name in unique_tags:
                existing_tag = Tags.query.filter_by(tag = tag_name).first()
                
                # If the tag does not exist, create a new tag object
                if not existing_tag:
                    new_tag = Tags(tag = tag_name)
                    db.session.add(new_tag)
                    db.session.commit()
                    user_tags.append(new_tag)
                # If the tag already exists, add the existing tag object to the user's tags
                else:
                    user_tags.append(existing_tag)

            # Create a new user object from the form
            new_user = User(
                username=form.username.data,
                password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                birth_date=form.birth_date.data,
                date_joined=datetime.now(),
                is_organiser=form.is_organiser.data,
                tags = user_tags
            )

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Create auxiliary user objects
            user_id = new_user.id

            new_user_contact = UserContact(
                user = user_id,
                contact_type = 'Email',
                contact_value = form.email.data,
                description = 'Primary email address'
            )

            new_user_album = Album(
                name = 'Default',
                description = 'Default album for {new_user.username}',
                user_id = user_id,
                event_id = None
            )
            print(f"New user album created: {new_user_album}")
            db.session.add(new_user_contact)
            db.session.add(new_user_album)
            db.session.commit()

            new_image = Image(
            name = 'Default',
            location = 'Images/default.jpg',
            album_id = new_user_album.id,
            image_type = 'banner_image'
            )
            print(f"New image created: {new_image}")
            db.session.add(new_image)
            db.session.commit()
            image = Image.query.filter_by(album_id=new_user_album.id).first()

            new_user_wall = UserWall(
                user = user_id,
            )
            db.session.add(new_user_wall)
            db.session.commit()
            
            return redirect(url_for('auth.registration_success'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.')
            print(f"Error during registration: {str(e)}")

    return render_template('auth/register.html', form = form, logged_in=logged_in)

@bp.route('/registration_success/')
def registration_success():
    return render_template('auth/registration_success.html')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
