from LarpBook import db

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address1 = db.Column(db.String(100), nullable=False)
    address2 = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    county = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)

    events = db.relationship('Event', back_populates='venue')

    idx_venue_id = db.Index('idx_venue_id', id)