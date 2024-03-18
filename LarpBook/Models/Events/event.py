from LarpBook import db
from LarpBook.Models.Users.user import User

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organiser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    organiser = db.relationship('User', backref='events')