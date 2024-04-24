from LarpBook import db
from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint

eventtags = Table('eventtags', db.Model.metadata,
                   Column('event_id', Integer, ForeignKey('event.id')),
                     Column('tag_id', Integer, ForeignKey('tags.id')),
                     UniqueConstraint('event_id', 'tag_id', name='event_tag')
                     )