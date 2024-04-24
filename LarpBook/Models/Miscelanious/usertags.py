from LarpBook import db
from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint

usertags = Table('usertags', db.Model.metadata,
                   Column('user_id', Integer, ForeignKey('user.id')),
                     Column('tag_id', Integer, ForeignKey('tags.id')),
                     UniqueConstraint('user_id', 'tag_id', name='user_tag')
                     )