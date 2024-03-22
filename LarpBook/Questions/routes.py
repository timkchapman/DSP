from flask import render_template
from LarpBook.Questions import bp
from LarpBook.Utils import authorisation

@bp.route('/')
def index():
    
    logged_in = authorisation.is_user_logged_in()
    return render_template('questions/index.html', logged_in=logged_in)