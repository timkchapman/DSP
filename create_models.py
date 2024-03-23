from LarpBook import create_app,db
from config import Config
from LarpBook.Models import models

models = [models.User, 
          models.UserWall, 
          models.UserContact,
          models.UserPreferences, 
          models.WallPost, 
          models.Notification,
          models.Message, 
          models.Conversation, 
          models.ConversationParticipant,
          models.Venue, 
          models.VenueWall, 
          models.Event, 
          models.EventWall,
          models.Receipt, 
          models.Ticket, 
          models.TicketType, 
          models.Transaction,
          models.PaymentMethod, 
          models.Album, 
          models.Image
          ]

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