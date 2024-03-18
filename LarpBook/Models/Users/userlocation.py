from LarpBook import db
from .user import User

class UserLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Integer(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)