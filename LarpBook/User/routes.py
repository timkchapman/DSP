from flask import render_template
from LarpBook.User import bp
from LarpBook import db

@bp.route('/')
def index():
    return render_template('user/index.html')