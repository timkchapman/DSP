
"""
This module contains routes and functions related to managing events in LarpBook.

Routes and Functions:
    - /: Renders the index page displaying events and handles event-related functions.
    - /categories/: Renders the categories page.
    - /event/<int:event_id>/: Renders the page for a specific event.
    - /create/: Allows creation of a new event.
    - /check_venue: Checks venue availability.
    - /event_dashboard/<int:event_id>: Renders the event dashboard 
                                        and handles event-related functions.
    - /edit_event/<int:event_id>: Allows editing of an event.
    - /event_dashboard/<int:event_id>/delete: Deletes an event.
    - /edit_venue/<int:venue_id>: Allows editing of a venue.
    - /event_dashboard/<int:event_id>/add_ticket: Adds tickets to an event.
    - /view_ticket/<int:ticket_id>: Views ticket details.
    - /event_dashboard/<int:ticket_id>/edit_ticket: Allows editing of a ticket.
    - /event_dashboard/<int:ticket_id>/delete_ticket: Deletes a ticket.
    - /toggle_ticket_active/<int:ticket_id>: Toggles ticket active status.
    - /checkout/<int:ticket_id>/: Processes ticket checkout.
    - /simulate_purchase/<int:ticket_id>/<result>: Simulates ticket purchase.

Functions:
    - index(): Renders the index page.
    - categories(): Renders the categories page.
    - event_page(event_id): Renders the event page.
    - create_event(): Creates a new event.
    - check_venue(): Checks venue availability.
    - event_dashboard(event_id): Renders the event dashboard.
    - edit_event(event_id): Edits an event.
    - delete_event(event_id): Deletes an event.
    - edit_venue(venue_id): Edits a venue.
    - add_tickets(event_id): Adds tickets to an event.
    - view_ticket(ticket_id): Views ticket details.
    - edit_ticket(ticket_id): Edits a ticket.
    - delete_ticket(ticket_id): Deletes a ticket.
    - toggle_ticket_active(ticket_id): Toggles ticket active status.
    - checkout(ticket_id): Processes ticket checkout.
    - simulate_purchase(ticket_id, result): Simulates ticket purchase.
    - generate_ticket_pdf(ticket, event_name): Generates a PDF ticket.
"""

import os
from datetime import datetime
from sqlalchemy import and_, or_
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_paginate import Pagination
from flask_login import current_user
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from LarpBook.Events import bp
from LarpBook.extensions import db
from LarpBook.Models.models import (Event, User, Venue, Album, Image, EventWall,
                                    VenueWall, TicketType, Transaction, Ticket, Tags)
from LarpBook.Utils import geocode, authorisation
from LarpBook.Static.Forms.forms import EventForm, EditEventForm, AddTicketForm, EditVenueForm
from LarpBook.Utils.authorisation import organiser_login_required



@bp.route('/')
def index():
    """
    Renders the index page.

    Returns:
        str: Rendered HTML template.
    """
    logged_in = authorisation.is_user_logged_in()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    events_query = Event.query
    events_query = events_query.outerjoin(TicketType)

    # Filter events by tag
    tag_filter = request.args.get('tag')
    if tag_filter:
        tag_filter = tag_filter.lower()
        events_query = events_query.filter(Event.tags.any(tag=tag_filter))

    # Filter events by ticket availability
    tickets_filter = request.args.get('tickets')
    if tickets_filter:
        if tickets_filter == 'lt20':
            events_query = events_query.filter(TicketType.max_tickets <= 20)
        elif tickets_filter == 'lt50':
            events_query = events_query.filter(TicketType.max_tickets <= 50)
        elif tickets_filter == 'lt100':
            events_query = events_query.filter(TicketType.max_tickets <= 100)
        elif tickets_filter == 'lt500':
            events_query = events_query.filter(TicketType.max_tickets <= 500)
        elif tickets_filter == 'gt500':
            events_query = events_query.filter(TicketType.max_tickets > 500)

    # Filter events by date range
    start_date_filter = request.args.get('start_date')
    end_date_filter = request.args.get('end_date')
    if start_date_filter and end_date_filter:
        start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
        events_query = events_query.filter(and_(Event.start_date >= start_date,
                                                Event.end_date <= end_date))
    elif start_date_filter:
        start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
        events_query = events_query.filter(Event.start_date >= start_date)
    elif end_date_filter:
        end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
        events_query = events_query.filter(Event.end_date <= end_date)

    # Filter events by price range
    min_price_filter = request.args.get('min_price')
    max_price_filter = request.args.get('max_price')
    if min_price_filter and max_price_filter:
        events_query = events_query.filter(and_(TicketType.price >= float(min_price_filter),
                                                TicketType.price <= float(max_price_filter)))

    # General search query
    search_query = request.args.get('q')
    if search_query:
        search_query = search_query.lower()
        events_query = events_query.filter(or_(
            Event.name.ilike(f'%{search_query}%'),
            Event.description.ilike(f'%{search_query}%'),
            User.username.ilike(f'%{search_query}%')  # Include organizer's username in the search
        ))

    events = events_query.all()

    organisers = User.query.filter(User.id.in_([event.organiser_id for event in events])).all()
    organiser_names = {organiser.id: organiser.username for organiser in organisers}

    combined_data = []
    for event in events:
        organiser_name = organiser_names.get(event.organiser_id)
        combined_data.append((event, organiser_name))

    # Sort combined_data by the date of the event
    combined_data.sort(key=lambda x: x[0].start_date)

    # Filter out past events before formatting the start date
    today = datetime.now().date()
    combined_data = [(event, organiser_name) for event,
                     organiser_name in combined_data if event.start_date >= today]

    # Format start date to display month name and day
    combined_data = [(event,
                      organiser_name,
                      event.start_date.strftime("%b %d")) for event,
                      organiser_name in combined_data]

    # Implement pagination
    pagination = Pagination(page=page,
                            per_page=per_page,
                            total=len(combined_data),
                            css_framework='bootstrap4')

    start_index = (pagination.page - 1) * pagination.per_page
    end_index = pagination.page * pagination.per_page
    combined_data = combined_data[start_index:end_index]

    return render_template('events/index.html',
                           events=combined_data,
                           pagination=pagination,
                           logged_in=logged_in)


@bp.route('/categories/')
def categories():
    """
    Renders the categories page.

    Returns:
        str: Rendered HTML template.
    """
    logged_in = authorisation.is_user_logged_in()
    return render_template('events/categories.html',
                           logged_in=logged_in)

@bp.route('/event/<int:event_id>/')
def event_page(event_id):
    """
    Renders the event page.

    Args:
        event_id (int): The ID of the event.

    Returns:
        str: Rendered HTML template.
    """
    logged_in = authorisation.is_user_logged_in()
    event = Event.query.get_or_404(event_id)
    album = Album.query.filter(Album.event.has(id=event_id)).first()
    if album:
        print("Album Found")
        cover_image = Image.query.filter_by(album_id=album.id).first()
        if cover_image:
            print("Cover Image Found")
            print(cover_image.location)
    else:
        cover_image = None
        print("Cover Image Not Found")
    organiser = User.query.get(event.organiser_id)

    venue = event.venue_id
    venue = Venue.query.get(venue)
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

    geocode_address = address.replace(",", " ")
    latlng = geocode.geocode(geocode_address)
    if latlng and len(latlng) == 2:
        lat, lng = latlng[0], latlng[1]
    else:
        lat, lng = None, None

    tickets = TicketType.query.filter_by(event_id=event_id).all()
    for ticket in tickets:
        print(ticket, ticket.available)
    return render_template('events/eventwall.html',
                           event=event,
                           image = cover_image,
                           organiser = organiser,
                           address = address,
                           venue = venue,
                           lat = lat,
                           lng = lng,
                           logged_in=logged_in,
                           tickets = tickets)

@bp.route('/create/', methods=['GET', 'POST'])
@organiser_login_required
def create_event():
    """
    Creates a new event.

    Returns:
        str: Rendered HTML template for the create event page.
    """
    logged_in = authorisation.is_user_logged_in()
    form = EventForm()

    if form.validate_on_submit():
        venue = Venue.query.filter_by(
            name = form.venue.data
        ).first()

        if venue:
            venue_id = venue.id
        else:
            new_venue = Venue(
                name = form.venue.data,
                address1 = form.address1.data,
                address2 = form.address2.data,
                city = form.city.data,
                county = form.county.data,
                postcode = form.postcode.data
            )
            db.session.add(new_venue)
            db.session.commit()
            venue_id = new_venue.id

            new_venue_wall = VenueWall(
                venue=new_venue.id
            )
            db.session.add(new_venue_wall)

        event_tags = []
        tag_names = [tag.strip().lower for tag in form.tags.data.split(',')]
        unique_tags = set(tag_names)

        for tag_name in unique_tags:
            existing_tag = Tags.query.filter_by(tag = tag_name).first()

            if not existing_tag:
                new_tag = Tags(tag = tag_name)
                db.session.add(new_tag)
                db.session.commit()
                event_tags.append(new_tag)
            else:
                event_tags.append(existing_tag)

        new_event = Event(
            organiser_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            venue_id=venue_id,
            tags = event_tags
        )
        db.session.add(new_event)
        db.session.commit()

        new_wall = EventWall(
            event=new_event.id
        )
        db.session.add(new_wall)

        new_album = Album(
            name= 'Default',
            description= 'album for : ' + new_event.name,
            event_id=new_event.id
        )
        db.session.add(new_album)
        db.session.commit()

        new_image = Image(
            name = 'Default',
            location = 'Images/default.jpg',
            album_id = new_album.id,
            image_type = 'banner_image'
        )
        db.session.add(new_image)
        db.session.commit()

        flash('Event created successfully', 'success')
        return redirect(url_for('events.event_dashboard',
                                event_id=new_event.id))

    return render_template('events/create.html',
                           form=form,
                           logged_in=logged_in)

@bp.route('/check_venue')
def check_venue():
    """
    Checks venue availability.

    Returns:
        str: JSON response containing matching venue names.
    """
    name = request.args.get('name')
    if name:
        matching_venues = Venue.query.filter(Venue.name.ilike(f'%{name}%')).all()
        venue_names = [{'name': venue.name} for venue in matching_venues]
        return jsonify(venue_names)
    return jsonify([])

# Route for the events dashboard
@bp.route('/event_dashboard/<int:event_id>', methods=['GET', 'POST'])
@organiser_login_required
def event_dashboard(event_id):
    """
    Renders the event dashboard.

    Args:
        event_id (int): The ID of the event.

    Returns:
        str: Rendered HTML template for the event dashboard.
    """
    logged_in = authorisation.is_user_logged_in()
    event = Event.query.get_or_404(event_id)

    if event.organiser_id != current_user.id:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('auth.login'))

    organiser = User.query.get(event.organiser_id)
    tickets = TicketType.query.filter_by(event_id=event_id).all()
    venue = Venue.query.get(event.venue_id)

    edit_venue_form = EditVenueForm()
    edit_event_form = EditEventForm()
    edit_tickets_form = AddTicketForm()
    existing_tags = [tag.tag for tag in event.tags]
    existing_tag_string = ', '.join(existing_tags)

    return render_template('events/event_dashboard.html',
                            logged_in = logged_in,
                            organiser = organiser,
                            event=event,
                            venue = venue,
                            tickets = tickets,
                            tags = existing_tag_string,
                            edit_event_form=edit_event_form,
                            edit_tickets_form=edit_tickets_form,
                            edit_venue_form=edit_venue_form)

@bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@organiser_login_required
def edit_event(event_id):
    """
    Edits an event.

    Args:
        event_id (int): The ID of the event.

    Returns:
        str: Rendered HTML template for the edit event page.
    """
    logged_in = authorisation.is_user_logged_in()
    event = Event.query.get_or_404(event_id)

    if event.organiser_id != current_user.id:
        flash('You do not have permission to edit this event.', 'error')
        return redirect(url_for('auth.login'))

    form = EditEventForm(obj=event)

    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data

        # Split the tag string into individual tag names
        tag_names = [tag.strip().lower() for tag in form.tags.data.split(',')]

        unique_tags = set(tag_names)

       # Create or fetch existing tags and associate them with the event
        event.tags.clear()  # Clear existing tags
        for tag_name in unique_tags:
            # Check if the tag already exists
            existing_tag = Tags.query.filter_by(tag=tag_name).first()

            if not existing_tag:
                # If tag does not exist, create a new one
                new_tag = Tags(tag=tag_name)
                db.session.add(new_tag)
                event.tags.append(new_tag)
            else:
                # If tag exists, use the existing one
                event.tags.append(existing_tag)
        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('events.event_dashboard', event_id=event.id))

    return render_template('edit_event.html', logged_in=logged_in, form=form, event=event)

# Route for deleting an event
@bp.route('/event_dashboard/<int:event_id>/delete', methods=['POST'])
@organiser_login_required
def delete_event(event_id):
    """
    Deletes an event.

    Args:
        event_id (int): The ID of the event.

    Returns:
        str: Redirects to the index page.
    """
    event = Event.query.get_or_404(event_id)

    if event.organiser_id != current_user.id:
        flash('You do not have permission to delete this event.', 'error')
        return redirect(url_for('auth.login'))

    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully', 'success')
    return redirect(url_for('events.index'))

# Define route for editing venue
@bp.route('/edit_venue/<int:venue_id>', methods=['GET', 'POST'])
@organiser_login_required
def edit_venue(venue_id):
    """
    Edits a venue.

    Args:
        venue_id (int): The ID of the venue.

    Returns:
        str: Rendered HTML template for the edit venue page.
    """
    # Fetch venue from database
    venue = Venue.query.get_or_404(venue_id)

    # Create form and populate it with existing venue data
    form = EditVenueForm(obj=venue)

    # Handle form submission
    if form.validate_on_submit():
        # Update venue details with data from the form
        venue.name = form.venue.data
        venue.address1 = form.address1.data
        venue.address2 = form.address2.data
        venue.city = form.city.data
        venue.county = form.county.data
        venue.postcode = form.postcode.data

        # Commit changes to the database
        db.session.commit()

        # Flash success message and redirect to venue page
        flash('Venue details updated successfully', 'success')
        return redirect(url_for('events.event_page',
                                event_id=venue.id))

    # Render template with form
    return render_template('venues/edit_venue.html', form=form, venue=venue)


@bp.route('/event_dashboard/<int:event_id>/add_ticket', methods=['GET','POST'])
@organiser_login_required
def add_tickets(event_id):
    """
    Adds tickets to an event.

    Args:
        event_id (int): The ID of the event.

    Returns:
        str: Rendered HTML template for adding tickets to an event.
    """
    logged_in = authorisation.is_user_logged_in()
    event = Event.query.get_or_404(event_id)
    if not event.organiser_id == current_user.id:
        flash('You do not have permission to add tickets to this event.', 'error')
        return redirect(url_for('events.event', event_id=event.id))

    form = AddTicketForm()
    if form.validate_on_submit():
        deposit_amount = form.deposit_amount.data if form.depositable.data else 0
        new_ticket = TicketType(
            event_id=event_id,
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            depositable=form.depositable.data,
            deposit_amount=deposit_amount,
            max_tickets=form.max_tickets.data,
            tickets_sold=0
        )
        db.session.add(new_ticket)
        db.session.commit()
        flash('Ticket added successfully', 'success')
        return redirect(url_for('events.event_dashboard', event_id=event.id))
    return render_template('tickets/add_ticket.html', logged_in = logged_in, form=form, event=event)

@bp.route('/view_ticket/<int:ticket_id>', methods=['GET'])
@organiser_login_required
def view_ticket(ticket_id):
    """
    Views ticket details.

    Args:
        ticket_id (int): The ID of the ticket.

    Returns:
        str: JSON response containing ticket information.
    """
    ticket = TicketType.query.get_or_404(ticket_id)
    event = Event.query.get_or_404(ticket.event_id)

    # Convert boolean depositable value to string "Yes" or "No"
    depositable_text = "Yes" if ticket.depositable else "No"

    deposit_text = ticket.deposit_amount if ticket.depositable else "N/A"


    # Return ticket information as JSON
    return jsonify({
        'event_name': event.name,
        'ticket_name': ticket.name,
        'description': ticket.description,
        'price': ticket.price,
        'depositable': depositable_text,
        'deposit_amount': deposit_text,
        'max_tickets': ticket.max_tickets,
        'tickets_sold': ticket.tickets_sold
    })

@bp.route('/event_dashboard/<int:ticket_id>/edit_ticket', methods=['GET', 'POST'])
@organiser_login_required
def edit_ticket(ticket_id):
    """
    Edits a ticket.

    Args:
        ticket_id (int): The ID of the ticket.

    Returns:
        str: Rendered HTML template for editing a ticket.
    """
    logged_in = authorisation.is_user_logged_in()
    ticket = TicketType.query.get_or_404(ticket_id)
    event = Event.query.get_or_404(ticket.event_id)  # Use ticket.event_id instead of ticket.event

    if event.organiser_id != current_user.id:
        flash('You do not have permission to edit this ticket.', 'error')
        return redirect(url_for('auth.login'))

    form = AddTicketForm(obj=ticket)
    if form.validate_on_submit():
        ticket.name = form.name.data
        ticket.price = form.price.data
        ticket.description = form.description.data
        ticket.depositable = form.depositable.data
        ticket.deposit_amount = form.deposit_amount.data
        ticket.max_tickets = form.max_tickets.data
        db.session.commit()  # No need to add ticket again
        flash('Ticket updated successfully', 'success')
        return redirect(url_for('events.event_dashboard', event_id=event.id))
    return render_template('events/edit_ticket.html',
                           logged_in=logged_in,
                           form=form,
                           ticket=ticket,
                           event=event)

@bp.route('/event_dashboard/<int:ticket_id>/delete_ticket', methods=['POST'])
@organiser_login_required
def delete_ticket(ticket_id):
    """
    Deletes a ticket.

    Args:
        ticket_id (int): The ID of the ticket.

    Returns:
        str: Redirects to the event dashboard page.
    """
    logged_in = authorisation.is_user_logged_in()
    ticket = TicketType.query.get_or_404(ticket_id)
    event = Event.query.get_or_404(ticket.event_id)

    if event.organiser_id != current_user.id:
        flash('You do not have permission to delete this ticket.', 'error')
        return redirect(url_for('auth.login'))

    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully', 'success')
    return redirect(url_for('events.event_dashboard', 
                            logged_in = logged_in, 
                            event_id=event.id))

@bp.route('/toggle_ticket_active/<int:ticket_id>',  methods=['POST'])
@organiser_login_required
def toggle_ticket_active(ticket_id):
    """
    Toggles ticket active status.

    Args:
        ticket_id (int): The ID of the ticket.

    Returns:
        str: Redirects to the event dashboard page.
    """
    logged_in = authorisation.is_user_logged_in()
    ticket = TicketType.query.get_or_404(ticket_id)

    if ticket.event.organiser_id != current_user.id:
        return redirect(url_for('auth.login'))

    # Toggle the available status of the ticket
    ticket.available = not ticket.available
    db.session.commit()
    flash('Ticket active status updated successfully', 'success')

    return redirect(url_for('events.event_dashboard',
                            logged_in = logged_in,
                            event_id=ticket.event.id))

@bp.route('/checkout/<int:ticket_id>/', methods=['GET', 'POST'])
def checkout(ticket_id):
    """
    Processes ticket checkout.

    Args:
        ticket_id (int): The ID of the ticket.

    Returns:
        str: Rendered HTML template for the ticket checkout page.
    """
    logged_in = authorisation.is_user_logged_in()

    if not logged_in:
        flash('You must be logged in to purchase a ticket.', 'error')
        return redirect(url_for('auth.login'))

    ticket = TicketType.query.get_or_404(ticket_id)
    if not ticket.available:
        flash('This ticket is not available for purchase.', 'error')
        return redirect(url_for('events.event_page', event_id=ticket.event))

    event = Event.query.get(ticket.event_id)
    organiser = User.query.get(event.organiser_id)

    return render_template('tickets/checkout.html',
                           logged_in = logged_in,
                           ticket=ticket,
                           event=event,
                           organiser=organiser)

@bp.route('/simulate_purchase/<int:ticket_id>/<result>', methods=['POST'])
def simulate_purchase(ticket_id, result):
    """
    Simulates ticket purchase.

    Args:
        ticket_id (int): The ID of the ticket.
        result (str): The result of the purchase simulation.

    Returns:
        str: Redirects to the checkout page.
    """
    logged_in = authorisation.is_user_logged_in()
    ticket = TicketType.query.get_or_404(ticket_id)
    if result == 'success':

        # Create the ticket for the user
        new_ticket = Ticket(
            event_id=ticket.event_id,
            user_id=current_user.id,
            ticket_type_id=ticket.id,
            ticket_code=f'{current_user.id}-{ticket.event_id}-{ticket.id}-{ticket.tickets_sold + 1}'
        )
        db.session.add(new_ticket)
        db.session.commit()
        # Increment tickets_sold
        ticket.tickets_sold += 1
        db.session.commit()
        flash('Ticket purchased successfully.', 'success')
        event_name = ticket.event.name

        # Generate a PDF ticket
        generate_ticket_pdf(new_ticket, event_name)

        transaction = Transaction(
            user_id = current_user.id,
            event_id = ticket.event_id,
            ticket_id = new_ticket.id,
            total = ticket.price,
            payment_status = True,
            timestamp = datetime.now()
        )
        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for('events.event_page',
                                logged_in = logged_in,
                                event_id=ticket.event_id))
    elif result == 'failure':
        flash('Ticket purchase failed.', 'error')

        # Log the failed transaction
        transaction = Transaction(
            user_id = current_user.id,
            event_id = ticket.event_id,
            ticket_id = ticket.id,
            total = ticket.price,
            payment_status = False,
            timestamp = datetime.now()
        )
        db.session.add(transaction)
        db.session.commit()

    return redirect(url_for('events.checkout', logged_in = logged_in, ticket_id=ticket_id))

def generate_ticket_pdf(ticket, event_name):
    """
    Generates a PDF ticket.

    Args:
        ticket (Ticket): The ticket object.
        event_name (str): The name of the event.
    """
    event_name_cleaned = event_name.replace(' ', '_')  # Replace spaces with underscores
    event_dir = os.path.join('LarpBook', 'Static', 'Tickets', event_name_cleaned)
    os.makedirs(event_dir, exist_ok=True)


    file_name = f'ticket_{ticket.id}.pdf'
    save_path = os.path.join(event_dir, file_name)

    c = canvas.Canvas(save_path, pagesize=A5)
    c.rect(20, 20, 160, 210)
    c.line(20, 20, 180, 230)
    c.drawString(100, 500, f'Ticket for {ticket.event.name}')
    c.save()
    