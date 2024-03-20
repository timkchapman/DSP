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
    
    organisers = models.User.query.filter(models.User.id.in_([event.organiser_id for event in events])).all()
    organiser_names = {organiser.id: organiser.username for organiser in organisers}

    combined_data = []
    for event in events:
        organiser_name = organiser_names.get(event.organiser_id)
        combined_data.append((event, organiser_name))

    # Sort combined_data by the date of the event
    combined_data.sort(key=lambda x: x[0].start_date)

    # Filter out past events before formatting the start date
    today = datetime.now().date()
    combined_data = [(event, organiser_name) for event, organiser_name in combined_data if event.start_date >= today]

    # Format start date to display month name and day
    combined_data = [(event, organiser_name, event.start_date.strftime("%b %d")) for event, organiser_name in combined_data]

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
    cover_image = event.cover_image_id
    return render_template('events/eventwall.html', event=event, image=cover_image)
