from LarpBook import db
from datetime import datetime
from LarpBook.Utils.serialise_models import SerializerMixin

class Message(db.Model, SerializerMixin):
    __tablename__ = 'message'
    messageId = db.Column(db.Integer, primary_key=True)
    conversationId = db.Column(db.Integer, db.ForeignKey('conversation.conversationId'), nullable=False)
    senderId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timeStamp = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    read = db.Column(db.Boolean, nullable=False, default = False) 