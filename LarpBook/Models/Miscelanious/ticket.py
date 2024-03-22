from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class Ticket(db.Model, SerializerMixin):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_type = db.Column(db.String(50), nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    ticket_code =  db.Column(db.String, unique=True, nullable=False)