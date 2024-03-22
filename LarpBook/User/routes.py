from flask import render_template
from LarpBook.User import bp
from LarpBook import db
from LarpBook.Models.Users.user import User
from LarpBook.Utils import authorisation

@bp.route('/')
def index():
    logged_in = authorisation.is_user_logged_in()
    return render_template('users/index.html', logged_in=logged_in)

@bp.route('/organiser/<int:id>/')
def organiser_page(id):
    
    logged_in = authorisation.is_user_logged_in()
    organiser = User.query.get_or_404(id)
    return render_template('users/organiser.html', organiser = organiser, logged_in=logged_in)

@bp.route('/user/<int:id>/')
def user_page(id):
    logged_in = authorisation.is_user_logged_in()
    user = User.query.get_or_404(id)
    return render_template('users/user.html', user = user, logged_in=logged_in)