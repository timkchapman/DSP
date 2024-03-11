from flask import render_template
from LarpBook.Main import bp

@bp.route('/')
def index():
	return render_template('index.html')
