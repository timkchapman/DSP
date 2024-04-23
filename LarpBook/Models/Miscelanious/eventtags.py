from LarpBook import db
from sqlalchemy import Table, Column, Integer, ForeignKey

eventtags = Table('eventtags', db.Model.metadata,
                   Column('event_id', Integer, ForeignKey('event.id')),
                     Column('tag_id', Integer, ForeignKey('tags.id'))
                     )