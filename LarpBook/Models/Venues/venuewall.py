from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class VenueWall(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posts = db.relationship('VenueWallPost', backref='venue_wall_post', lazy=True,
                            primaryjoin="and_(VenueWall.id == VenueWallPost.venue_wall_id, VenueWallPost.wall_type == 'venue_wall')")