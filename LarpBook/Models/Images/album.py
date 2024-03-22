from LarpBook import db
from .albumimage import albumimage
from sqlalchemy.ext.declarative import declared_attr
from LarpBook.Utils.serialise_models import SerializerMixin

class Album(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    images = db.relationship('Image', secondary=albumimage, backref='albums')


    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    @declared_attr
    def event_id(cls):
        return db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', backref='albums')

    @declared_attr
    def event(cls):
        return db.relationship('Event', backref='albums')
    
    