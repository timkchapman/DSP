from flask import render_template
from LarpBook.Main import bp
from LarpBook import db
from LarpBook.Models import models
from LarpBook.Utils import carousel_populator, geocode
import time

@bp.route('/')
def index():
    # Fetch events for carousel
    carousel_events = 'LarpBook/Static/JSON/carousel.json'
    carousel = carousel_populator.fetch_events_from_file(carousel_events)
    events = list(enumerate(carousel))
    
    # Fetch all necessary data in one query
    latest_events = models.Event.query.order_by(models.Event.id.desc()).limit(5).all()
    soonest_events = models.Event.query.order_by(models.Event.start_date).limit(5).all()

    # Extract coordinates for latest events
    latest_event_coords = [(event.latitude, event.longitude) for event in latest_events if event.latitude and event.longitude]
    # Batch reverse geocode latest event coordinates
    latest_event_addresses = {}
    if latest_event_coords:
        latest_event_addresses = geocode.batch_reverse_geocode(latest_event_coords, [event.id for event in latest_events])

    # Extract coordinates for soonest events
    soonest_event_coords = [(event.latitude, event.longitude) for event in soonest_events if event.latitude and event.longitude]
    # Batch reverse geocode soonest event coordinates
    soonest_event_addresses = {}
    if soonest_event_coords:
        soonest_event_addresses = geocode.batch_reverse_geocode(soonest_event_coords, [event.id for event in soonest_events])

    # Retrieve organiser names
    organiser_ids = set(event.organiser_id for event in latest_events + soonest_events)
    organisers = models.User.query.filter(models.User.id.in_(organiser_ids)).all()
    organiser_names = {organiser.id: organiser.username for organiser in organisers}

    # Combine data for rendering
    # Combine data for rendering
    combined_latest = []
    for event in latest_events:
        # Use event ID as the key
        address = latest_event_addresses.get(event.id)
        organiser_name = organiser_names.get(event.organiser_id)
        combined_latest.append((event, organiser_name, address))

    combined_soonest = []
    for event in soonest_events:
        # Use event ID as the key
        address = soonest_event_addresses.get(event.id)
        organiser_name = organiser_names.get(event.organiser_id)
        combined_soonest.append((event, organiser_name, address))
    
    return render_template('index.html', events=events, combined_data_latest=combined_latest, combined_data_soonest=combined_soonest)
