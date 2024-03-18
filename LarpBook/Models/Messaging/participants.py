from LarpBook import db

class ConversationParticipant(db.Model):
    __tablename__ = 'conversationParticipant'
    conversationParticipantId = db.Column(db.Integer, primary_key=True)
    conversationId = db.Column(db.Integer, db.ForeignKey('conversation.conversationId'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)