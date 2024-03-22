from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class Image(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    image_type = db.Column(db.String(50), nullable=False)