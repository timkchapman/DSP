from flask import render_template
from LarpBook.Main import bp
from LarpBook import db
from LarpBook.Models.Events.event import Event
from LarpBook.Models.Events.eventdetails import EventDetails
from LarpBook.Models.Users.user import User
from LarpBook.Utils import carousel_populator
import json

@bp.route('/')
def index():
    carousel_events = 'LarpBook/Static/JSON/carousel.json'
    carousel = carousel_populator.fetch_events_from_file(carousel_events)
    events = list(enumerate(carousel))
    for event in events:
        print(event)

    latest_events = Event.query.order_by(Event.id.desc()).limit(5).all()
    latest_event_details = EventDetails.query.order_by(EventDetails.id.desc()).limit(5).all()

    soonest_events = Event.query.join(EventDetails).order_by(EventDetails.date.asc()).limit(5).all()
    soonest_event_details = EventDetails.query.order_by(EventDetails.date.asc()).limit(5).all()

    organiser_ids = [event.organiser_id for event in latest_events + soonest_events]
    organisers = User.query.filter(User.id.in_(organiser_ids)).all()

    organiser_names = {organiser.id: organiser.username for organiser in organisers}

    latest_events_with_organisers = [(event, organiser_names.get(event.organiser_id)) for event in latest_events]
    soonest_events_with_organisers = [(event, organiser_names.get(event.organiser_id)) for event in soonest_events]

    combined_data_latest = zip(latest_events_with_organisers, latest_event_details)
    combined_data_soonest = zip(soonest_events_with_organisers, soonest_event_details)

    return render_template('index.html', events = events, combined_data_latest=combined_data_latest, combined_data_soonest=combined_data_soonest)
