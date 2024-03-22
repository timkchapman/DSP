from LarpBook import db
from .user import User
from LarpBook.Utils.serialise_models import SerializerMixin

class UserContact(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_type = db.Column(db.String(50), nullable=False)
    contact_value = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=True)