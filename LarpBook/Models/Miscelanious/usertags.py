from LarpBook import db
from sqlalchemy import Table, Column, Integer, ForeignKey

usertags = Table('usertags', db.Model.metadata,
                   Column('user_id', Integer, ForeignKey('user.id')),
                     Column('tag_id', Integer, ForeignKey('tags.id'))
                     )