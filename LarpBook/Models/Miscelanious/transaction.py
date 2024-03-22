from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class Transaction(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)