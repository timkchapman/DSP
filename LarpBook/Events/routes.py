from flask import render_template
from LarpBook.Events import bp

@bp.route('/')
def index():
    return render_template('events/index.html')

@bp.route('/categories/')
def categories():
    return render_template('events/categories.html')