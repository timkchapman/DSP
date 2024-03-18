from LarpBook import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notification'
    notificationId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timeStamp = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    read = db.Column(db.Boolean, nullable=False, default = False)