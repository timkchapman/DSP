from flask import render_template
from LarpBook.Questions import bp

@bp.route('/')
def index():
    return render_template('questions/index.html')