from LarpBook import db

class Conversation(db.Model):
    __tablename__ = 'conversation'
    conversationId = db.Column(db.Integer, primary_key=True)
    participants = db.relationship('User', secondary='conversationParticipant', backref=db.backref('conversations'))