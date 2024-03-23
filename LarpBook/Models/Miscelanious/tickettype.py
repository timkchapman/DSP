from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class TicketType(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    max_tickets = db.Column(db.Integer, nullable=False)
    tickets_sold = db.Column(db.Integer, nullable=False)

