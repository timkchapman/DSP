from LarpBook import db

class EventWall(db.Model):
    __tablename__ = 'eventwall'
    eventWallId = db.Column(db.Integer, primary_key=True)
    eventId = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
