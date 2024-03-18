from flask import session,render_template, redirect, url_for, flash, request
from LarpBook.Auth import bp
from flask_login import current_user, login_user
from LarpBook.Models.Users.user import User
from LarpBook.extensions import bcrypt, login_manager

@bp.route('/')
def index():
    return render_template('auth/index.html')

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('auth/login.html')

@bp.route('/logout/')
def logout():
    # Clear the session data
    session.clear()
    # redirect the user to the index page
    return redirect(url_for('main.index'))

@bp.route('/categories/')
def categories():
    return render_template('auth/registration.html')



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))