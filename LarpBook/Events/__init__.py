from flask import Blueprint

bp = Blueprint('events', __name__)

from LarpBook.Events import routes