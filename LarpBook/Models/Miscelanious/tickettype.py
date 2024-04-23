from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class TicketType(db.Model, SerializerMixin):
    __tablename__ = 'ticket_type'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    depositable = db.Column(db.Boolean, nullable=False)
    deposit_amount = db.Column(db.Float, nullable=True)
    available = db.Column(db.Boolean, default=False)
    max_tickets = db.Column(db.Integer, nullable=False)
    tickets_sold = db.Column(db.Integer, nullable=False)

    # Define relationships
    event = db.relationship('Event', backref='ticket_type')