from LarpBook import db

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticketId = db.Column(db.Integer, primary_key=True)
    eventId = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticketType = db.Column(db.String(50), nullable=False)
    ticketPrice = db.Column(db.Float, nullable=False)
    ticketcode =  db.Column(db.String, unique=True, nullable=False)