from flask import render_template
from LarpBook.Main import bp
from LarpBook import db
from LarpBook.Models import models
from LarpBook.Utils import carousel_populator
import json

@bp.route('/')
def index():
    carousel_events = 'LarpBook/Static/JSON/carousel.json'
    carousel = carousel_populator.fetch_events_from_file(carousel_events)
    events = list(enumerate(carousel))
    for event in events:
        print(event)

    latest_events = models.Event.query.order_by(models.Event.id.desc()).limit(5).all()
    latest_event_details = models.EventDetails.query.order_by(models.EventDetails.id.desc()).limit(5).all()

    soonest_events = models.Event.query.join(models.EventDetails).order_by(models.EventDetails.start_date.asc()).limit(5).all()
    soonest_event_details = models.EventDetails.query.order_by(models.EventDetails.start_date.asc()).limit(5).all()

    organiser_ids = [event.organiser_id for event in latest_events + soonest_events]
    organisers = models.User.query.filter(models.User.id.in_(organiser_ids)).all()

    organiser_names = {organiser.id: organiser.username for organiser in organisers}

    latest_events_with_organisers = [(event, organiser_names.get(event.organiser_id)) for event in latest_events]
    soonest_events_with_organisers = [(event, organiser_names.get(event.organiser_id)) for event in soonest_events]

    combined_data_latest = zip(latest_events_with_organisers, latest_event_details)
    combined_data_soonest = zip(soonest_events_with_organisers, soonest_event_details)

    return render_template('index.html', events = events, combined_data_latest=combined_data_latest, combined_data_soonest=combined_data_soonest)
