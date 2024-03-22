from sqlalchemy import Index
from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class Event(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    organiser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    
    organiser = db.relationship('User', backref='events')
    venue = db.relationship('Venue', back_populates='events')

    # Define indexes within the class definition
    idx_event_organiser_id = Index('idx_event_organiser_id', organiser_id)
    idx_event_name = Index('idx_event_name', name)
    idx_event_start_date = Index('idx_event_start_date', start_date)
