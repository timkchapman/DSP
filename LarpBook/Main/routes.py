"""
This module contains routes and functions related to the index page of LarpBook.

Routes:
    - /: Renders the index page.

Functions:
    - index(): Renders the index page, fetching data for the carousel, 
        latest events, and soonest events.
"""

from flask import render_template
from LarpBook.Main import bp
from LarpBook.Models import models
from LarpBook.Utils import carousel_populator, authorisation


@bp.route('/')
def index():
    """
    Renders the index page of LarpBook.

    Retrieves necessary data for rendering the page including carousel events,
    latest events, and soonest events. Combines the data and renders the template 'index.html'.

    Returns:
        str: Rendered HTML template for the index page.
    """
    logged_in = authorisation.is_user_logged_in()
    # Fetch events for carousel
    carousel_events = 'LarpBook/Static/JSON/carousel.json'
    carousel = carousel_populator.fetch_events_from_file(carousel_events)
    events = list(enumerate(carousel))

    # Fetch all necessary data in one query
    latest_events = models.Event.query.order_by(models.Event.id.desc()).limit(5).all()
    soonest_events = models.Event.query.order_by(models.Event.start_date).limit(5).all()

    # Retrieve organiser names
    organiser_ids = set(event.organiser_id for event in latest_events + soonest_events)
    organisers = models.User.query.filter(models.User.id.in_(organiser_ids)).all()
    organiser_names = {organiser.id: organiser.username for organiser in organisers}

    # Retrieve venue addresses
    venue_ids = set(event.venue_id for event in latest_events + soonest_events)
    venues = models.Venue.query.filter(models.Venue.id.in_(venue_ids)).all()
    venue_dict = {venue.id: venue for venue in venues}


    # Combine data for rendering
    # Combine data for rendering
    combined_latest = []
    for event in latest_events:
        # Use event ID as the key
        organiser_name = organiser_names.get(event.organiser_id)
        venue = venue_dict.get(event.venue_id)
        if venue is not None:
            address_parts = [venue.name,
                             venue.address1,
                             venue.address2,
                             venue.city,
                             venue.county,
                             venue.postcode]
            address = ", ".join(filter(None, address_parts))
        else:
            address = "Unknown"

        combined_latest.append((event, organiser_name, address))

    combined_soonest = []
    for event in soonest_events:
        # Use event ID as the key
        organiser_name = organiser_names.get(event.organiser_id)
        address = ", ".join(filter(None,
                                   [venue.name,
                                    venue.address1,
                                    venue.address2,
                                    venue.city,
                                    venue.county,
                                    venue.postcode]))
        combined_soonest.append((event, organiser_name, address))

    return render_template('index.html',
                           events=events,
                           combined_data_latest=combined_latest,
                           combined_data_soonest=combined_soonest,
                           logged_in=logged_in)
