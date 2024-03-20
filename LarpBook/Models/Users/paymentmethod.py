from LarpBook import db

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_method = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.String(100), nullable=False)
    cvv = db.Column(db.String(100), nullable=False)
    billing_address = db.Column(db.String(100), nullable=False)
    billing_postcode = db.Column(db.String(100), nullable=False)
    billing_city = db.Column(db.String(100), nullable=False)
    billing_country = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)