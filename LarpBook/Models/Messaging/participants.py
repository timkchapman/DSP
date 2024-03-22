from LarpBook import db
from LarpBook.Utils.serialise_models import SerializerMixin

class ConversationParticipant(db.Model, SerializerMixin):
    __tablename__ = 'conversationParticipant'
    conversationParticipantId = db.Column(db.Integer, primary_key=True)
    conversationId = db.Column(db.Integer, db.ForeignKey('conversation.conversationId'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)