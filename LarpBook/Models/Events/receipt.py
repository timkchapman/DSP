from LarpBook import db

class Receipt(db.Model):
    __tablename__ = 'receipt'
    receiptId = db.Column(db.Integer, primary_key=True)
    ticketId = db.Column(db.Integer, db.ForeignKey('ticket.ticketId'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    purchaseDate = db.Column(db.Date, nullable=False)
    purchaseTime = db.Column(db.Time, nullable=False)
    purchaseAmount = db.Column(db.Float, nullable=False)