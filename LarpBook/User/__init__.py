from flask import Blueprint

bp = Blueprint('user', __name__)

from LarpBook.User import routes
