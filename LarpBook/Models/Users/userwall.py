from LarpBook import db

class UserWall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posts = db.relationship('WallPost', backref='user_wall', lazy=True, primaryjoin = 'UserWall.id == WallPost.wall_id')