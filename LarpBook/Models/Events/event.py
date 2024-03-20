from sqlalchemy import Index
from LarpBook import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organiser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    cover_image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    organiser = db.relationship('User', backref='events')

    # Define indexes within the class definition
    idx_event_organiser_id = Index('idx_event_organiser_id', organiser_id)
    idx_event_name = Index('idx_event_name', name)
    idx_event_start_date = Index('idx_event_start_date', start_date)
