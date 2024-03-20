from flask import render_template, request
from flask_paginate import Pagination
from LarpBook.Events import bp
from LarpBook.extensions import db
from LarpBook.Models import models
from datetime import datetime

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    
    events = models.Event.query.all()
    for event in events:
        print(event.name)
    
    details = models.EventDetails.query.filter(models.EventDetails.event_id.in_([event.id for event in events])).all()
    for event in details:
        print(event.start_date)

    organisers = models.User.query.filter(models.User.id.in_([event.organiser_id for event in events])).all()
    organiser_names = {organiser.id: organiser.username for organiser in organisers}

    combined_data = []
    for event in events:
        event_details = [detail for detail in details if detail.event_id == event.id]
        organiser_name = organiser_names.get(event.organiser_id)
        combined_data.append((event, event_details, organiser_name))

    # Sort combined_data by the date of the first event detail
    combined_data.sort(key=lambda x: x[1][0].start_date if x[1] else None)
    
    # Filter out past events before formatting the start date
    today = datetime.now().date()
    print(today)
    combined_data = [(event, details, organiser_name) for event, details, organiser_name in combined_data if details and details[0].start_date >= today]

    # Format start date to display month name and day
    combined_data = [(event, details, organiser_name, details[0].start_date.strftime("%b %d")) for event, details, organiser_name in combined_data]

    # Implement pagination
    pagination = Pagination(page=page, per_page=per_page, total=len(combined_data), css_framework='bootstrap4')
    combined_data = combined_data[pagination.page * pagination.per_page - pagination.per_page:pagination.page * pagination.per_page]

    return render_template('events/index.html', events=combined_data, pagination=pagination)


@bp.route('/categories/')
def categories():
    return render_template('events/categories.html')

@bp.route('/event/<int:event_id>/')
def event_page(event_id):
    event = models.Event.query.get_or_404(event_id)

    event_details = models.EventDetails.query.filter_by(event_id = event_id).first()
    cover_image = None
    if event_details:
        cover_image = event_details.cover_image_id
    return render_template('events/eventwall.html', event=event, image = cover_image)
