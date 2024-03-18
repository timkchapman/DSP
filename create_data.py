from LarpBook import db, create_app
from LarpBook.Models import models
from LarpBook.extensions import bcrypt
from datetime import datetime

def main():
    app = create_app()
    with app.app_context():
        try:
            # Generate hashed passwords
            passwords = ['Password1', 'Password2', 'Password3', 'Password4', 'Password5']
            hashed_passwords = [bcrypt.generate_password_hash(password).decode('utf-8') for password in passwords]

            # Define user data
            user_data = [
                {'username': 'user1', 'first_name': 'User', 'last_name': 'One', 'is_organiser': True, 'is_active': True},
                {'username': 'user2', 'first_name': 'User', 'last_name': 'Two', 'is_organiser': True, 'is_active': True},
                {'username': 'user3', 'first_name': 'User', 'last_name': 'Three', 'is_organiser': False, 'is_active': True},
                {'username': 'user4', 'first_name': 'User', 'last_name': 'Four', 'is_organiser': False, 'is_active': True},
                {'username': 'user5', 'first_name': 'User', 'last_name': 'Five', 'is_organiser': False, 'is_active': True}
            ]

            # Add hashed passwords and dates to user data
            for i, user_info in enumerate(user_data):
                user_info['password_hash'] = hashed_passwords[i]
                user_info['date_joined'] = datetime.strptime('2024-01-01', '%Y-%m-%d').date()
                user_info['birth_date'] = datetime.strptime(f'199{i + 1}-0{i + 1}-0{i + 1}', '%Y-%m-%d').date()

                # Create user instance
                user = models.User(**user_info)

                # Add user to the session
                db.session.add(user)

                # Commit the user addition to get auto-generated user id
                db.session.commit()

                # Create UserWall instance for the user
                user_wall = models.UserWall(user=user.id)
                db.session.add(user_wall)

                # Create UserContact instances for the user
                email_contact = models.UserContact(
                    user=user.id,
                    contact_type='Email',
                    contact_value=f'email{i + 1}@email.com',
                    description=f"user {i + 1}'s email address"
                )
                db.session.add(email_contact)

                # Create 10 events for User1 and 2 each
                if i == 0:
                    for j in range(10):
                        event = models.Event(organiser_id=user.id, name=f'Event {j + 1}')
                        db.session.add(event)
                elif i == 1:
                    for j in range(10,20):
                        event = models.Event(organiser_id=user.id, name=f'Event {j + 1}')
                        db.session.add(event)

            # Commit the changes
            db.session.commit()
            print('Data added to database.')

        except Exception as e:
            print(f'An error occurred while adding users: {e}')
            db.session.rollback()

        '''try:
            # Creating event data
            user1 = models.User.query.filter_by(username='user1').first()
            if user1:
                event = models.Event(organiser_id=user1.id, name='Event 1')
                db.session.add(event)

        except Exception as e:
            print(f'An error occurred while adding events: {e}')
            db.session.rollback()'''
        

if __name__ == '__main__':
    main()
