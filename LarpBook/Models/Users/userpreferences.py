from LarpBook import db
from .user import User
from LarpBook.Utils.serialise_models import SerializerMixin

class UserPreferences(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(255), unique = True, nullable = False)

    def __repr__(self):
        return f'<UserPreferences user id = {self.user}, json file path = {self.file_path}>'.format(self.user, self.file_path)