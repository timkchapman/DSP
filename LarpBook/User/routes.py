from flask import render_template
from LarpBook.User import bp
from LarpBook import db
from LarpBook.Models.Users.user import User

@bp.route('/')
def index():
    return render_template('users/index.html')

@bp.route('/organiser/<int:organiser_id>/')
def organiser_page(organiser_id):
    organiser = User.query.get_or_404(organiser_id)
    return render_template('users/organiser.html', organiser = organiser)