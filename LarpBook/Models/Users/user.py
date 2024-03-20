from LarpBook import db
from .friendslist import friendslist
from .blocklist import blocklist
from .userwall import UserWall
from ..Miscelanious.wallpost import WallPost

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_joined = db.Column(db.Date, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    is_organiser = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_authenticated = db.Column(db.Boolean, nullable=False, default=False)
    friends = db.relationship('User', secondary = friendslist,
                              primaryjoin = id == friendslist.c.user_id,
                              secondaryjoin = id == friendslist.c.friend_id,
                              backref = db.backref('friend_of', lazy = 'dynamic'),
                              lazy = 'dynamic')
    
    blocked = db.relationship('User', secondary = blocklist,
                              primaryjoin = id == blocklist.c.user_id,
                              secondaryjoin = id == blocklist.c.blocked_id,
                              backref = db.backref('blocked_by', lazy = 'dynamic'),
                                lazy = 'dynamic')
    
    wall_posts = db.relationship('WallPost', backref = 'user', lazy = True)
    
    def get_id(self):
        return str(self.id)
