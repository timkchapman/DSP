from LarpBook import db

albumimage = db.Table('albumimage',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'), primary_key=True)
)