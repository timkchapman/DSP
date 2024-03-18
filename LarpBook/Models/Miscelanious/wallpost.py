from LarpBook import db

class WallPost(db.Model):
    __tablename__ = 'wallpost'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_date = db.Column(db.Date, nullable=False)
    post_time = db.Column(db.Time, nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(50), nullable=False)
    post_visibility = db.Column(db.String(50), nullable=False)
    # Polymorphic relationship with UserWall and EventWall
    wall_type = db.Column(db.String(50), nullable=False)
    __mapper_args__ = {
        'polymorphic_on': wall_type
    }

class UserWallPost(WallPost):
    user_wall_id = db.Column(None, db.ForeignKey('user_wall.id'), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'user_wall'
    }

class EventWallPost(WallPost):
    event_wall_id = db.Column(None, db.ForeignKey('event_wall.id'), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'event_wall'
    }