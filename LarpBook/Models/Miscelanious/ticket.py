from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class Ticket(db.Model, SerializerMixin):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticket_type.id'), nullable=False)
    ticket_code =  db.Column(db.String, unique=True, nullable=False)

    event = db.relationship('Event', back_populates='event_tickets')
