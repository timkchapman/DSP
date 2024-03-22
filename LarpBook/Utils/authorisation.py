from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from LarpBook import session

def organiser_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_organiser:
            flash('You need to be an organiser to access this page', 'danger')
            return redirect(url_for('auth.login'))  # Redirect to the login page
        return func(*args, **kwargs)
    return decorated_view

def is_user_logged_in():
    return current_user.is_authenticated