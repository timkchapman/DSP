from flask import render_template
from LarpBook.User import bp
from LarpBook import db
from LarpBook.Models.Users.user import User

@bp.route('/')
def index():
    return render_template('users/index.html')

@bp.route('/organiser/<int:id>/')
def organiser_page(id):
    organiser = User.query.get_or_404(id)
    return render_template('users/organiser.html', organiser = organiser)

@bp.route('/user/<int:id>/')
def user_page(id):
    user = User.query.get_or_404(id)
    return render_template('users/user.html', user = user)