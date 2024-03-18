from LarpBook import create_app,db
from config import Config


from LarpBook.Models.Users.user import User
from LarpBook.Models.Users.friendslist import friendslist
from LarpBook.Models.Users.blocklist import blocklist
from LarpBook.Models.Users.userwall import UserWall
from LarpBook.Models.Users.usercontact import UserContact
from LarpBook.Models.Users.userpreferences import UserPreferences
from LarpBook.Models.Miscelanious.wallpost import WallPost
from LarpBook.Models.Miscelanious.notifications import Notification
from LarpBook.Models.Messaging.message import Message
from LarpBook.Models.Messaging.conversation import Conversation
from LarpBook.Models.Messaging.participants import ConversationParticipant
from LarpBook.Models.Events.event import Event
from LarpBook.Models.Events.eventdetails import EventDetails
from LarpBook.Models.Events.eventwall import EventWall
from LarpBook.Models.Events.receipt import Receipt
from LarpBook.Models.Events.ticket import Ticket

models = [User, UserWall, UserContact, UserPreferences, WallPost, Notification, Message, Conversation, ConversationParticipant, Event, EventDetails, EventWall, Receipt, Ticket]

def main():
    app = create_app(Config)
    with app.app_context():
        print('Dropping tables...')
        db.drop_all()
        print('Creating tables...')
        for model in models:
            print(f'Creating table for {model}...')
            model.__table__.create(bind=db.engine)
        db.create_all()
        print('Tables created.')

if __name__ == '__main__':
    main()