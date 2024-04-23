from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class Tags(db.Model, SerializerMixin):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key = True)
    tag = db.Column(db.String, nullable = False, unique = True)

    events = db.relationship('Event', secondary = 'eventtags', back_populates = 'tags')
    users = db.relationship('User', secondary = 'usertags', back_populates = 'tags')