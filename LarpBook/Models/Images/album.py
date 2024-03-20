from LarpBook import db
from sqlalchemy.ext.declarative import declared_attr

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    cover_image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    images = db.relationship('Image', backref='album', lazy=True, primaryjoin="and_(Album.id == Image.album_id, Image.image_type == 'album_image')")

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
