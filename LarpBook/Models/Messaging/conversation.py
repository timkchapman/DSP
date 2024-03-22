from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class Conversation(db.Model, SerializerMixin):
    __tablename__ = 'conversation'
    conversationId = db.Column(db.Integer, primary_key=True)
    participants = db.relationship('User', secondary='conversationParticipant', backref=db.backref('conversations'))