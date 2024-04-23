from LarpBook.Models import models
from LarpBook import db

from LarpBook import create_app

app = create_app()

def set_authentication():
    users_to_authenticate = models.User.query.filter_by(is_authenticated=False).all()

    for user in users_to_authenticate:
        user.is_authenticated = True

    db.session.commit()

    print('All users have been authenticated')

if __name__ == '__main__':
    with app.app_context():
        set_authentication()