import sqlalchemy as db
from sqlalchemy import create_engine, PrimaryKeyConstraint
from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///database.db')
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique = True, nullable = False)
    password = Column(String(50), nullable = False)
    email = Column(String(50), unique = True, nullable = False) 
    latitude = Column(Float)
    longitude = Column(Float)
    
    events = relationship('Event', back_populates='organizer')
    tickets = relationship('Tickets', back_populates='buyer')
    interests = relationship('UserInterests', back_populates='user')
    reviews = relationship('EventReview', back_populates='user')
    
class Event(Base):
    __tablename__ = 'Events'
    event_id = Column(Integer, primary_key=True)
    organizer_id = Column(Integer, ForeignKey('Users.user_id'))
    event_name = Column(String(50), nullable = False)
    description = Column(Text, nullable = False)
    location = Column(String(50), nullable = False)
    date = Column(DateTime, nullable = False)
    time = Column(DateTime, nullable = False)
    
    organizer = relationship('User', back_populates='events')
    tickets = relationship('Tickets', back_populates='event')
    reviews = relationship('EventReview', back_populates='event')
    
class EventCategories(Base):
    __tablename__ = 'EventCategories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(50), nullable = False)
    
class UserInterests(Base):
    __tablename__ = 'UserInterests'
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    category_id = Column(Integer, ForeignKey('EventCategories.category_id'))
    
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'category_id'),
    )
    
    user = relationship('User', back_populates='interests')
    category = relationship('EventCategories', back_populates='user_interests')
    
class Tickets(Base):
    __tablename__ = 'Tickets'
    ticket_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('Events.event_id'))
    buyer_id = Column(Integer, ForeignKey('Users.user_id'))
    
    event = relationship('Event', back_populates='tickets')
    buyer = relationship('User', back_populates='tickets')
    
class EventReview(Base):
    __tablename__ = 'EventReviews'
    feedback_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('Events.event_id'))
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    rating = Column(Integer, nullable = False)
    feedback_text = Column(Text, nullable = False)
    
    event = relationship('Event', back_populates='reviews')
    user = relationship('User', back_populates='reviews')
    
Base.metadata.create_all(engine)
session.close()
