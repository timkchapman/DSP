from flask import Blueprint

bp = Blueprint('main', __name__)

from LarpBook.Main import routes
