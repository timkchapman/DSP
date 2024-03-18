from flask import Blueprint

bp = Blueprint('auth', __name__)

from LarpBook.Auth import routes
