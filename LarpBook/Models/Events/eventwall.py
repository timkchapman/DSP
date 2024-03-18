from LarpBook import db

class EventWall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    posts = db.relationship('EventWallPost', backref='event_wall_post', lazy=True,
                            primaryjoin="and_(EventWall.id == EventWallPost.event_wall_id, EventWallPost.wall_type == 'event_wall')")