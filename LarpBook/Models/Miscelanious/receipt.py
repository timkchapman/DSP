from LarpBook import db

class Receipt(db.Model):
    __tablename__ = 'receipt'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    purchase_time = db.Column(db.Time, nullable=False)
    purchase_amount = db.Column(db.Float, nullable=False)