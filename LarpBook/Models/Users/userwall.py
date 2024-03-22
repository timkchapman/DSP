from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class UserWall(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posts = db.relationship('UserWallPost', backref='user_wall_post', lazy=True,
                            primaryjoin="and_(UserWall.id == UserWallPost.user_wall_id, UserWallPost.wall_type == 'user_wall')")

