from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_paginate import Pagination
from LarpBook.Events import bp
from LarpBook.extensions import db
from LarpBook.Models.models import Event, User, Venue, Album, Image, EventWall, VenueWall, TicketType
from LarpBook.Utils import geocode, authorisation
from datetime import datetime
from config import Config
from LarpBook.Static.Forms.forms import EventForm, AddTicketForm, PaymentMethodForm
from LarpBook.Utils.authorisation import organiser_login_required
from flask_login import current_user

@bp.route('/')
def index():
    logged_in = authorisation.is_user_logged_in()
    page = request.args.get('page', 1, type=int)
    per_page = 4
    
    events = Event.query.all()
    
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
    combined_data = [(event, organiser_name) for event, organiser_name in combined_data if event.start_date >= today]

    # Format start date to display month name and day
    combined_data = [(event, organiser_name, event.start_date.strftime("%b %d")) for event, organiser_name in combined_data]

    # Implement pagination
    pagination = Pagination(page=page, per_page=per_page, total=len(combined_data), css_framework='bootstrap4')
    combined_data = combined_data[pagination.page * pagination.per_page - pagination.per_page:pagination.page * pagination.per_page]

    return render_template('events/index.html', events=combined_data, pagination=pagination, logged_in=logged_in)


@bp.route('/categories/')
def categories():
    
    logged_in = authorisation.is_user_logged_in()
    return render_template('events/categories.html', logged_in=logged_in)

@bp.route('/event/<int:event_id>/')
def event_page(event_id):
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
    address = ", ".join(filter(None, [venue.name, venue.address1, venue.address2, venue.city, venue.county, venue.postcode]))
    geocode_address = address.replace(",", " ")
    latlng = geocode.geocode(geocode_address)
    if latlng and len(latlng) == 2:
        lat, lng = latlng[0], latlng[1]
    else:
        lat, lng = None, None

    tickets = TicketType.query.filter_by(event=event_id).all()
    for ticket in tickets:
        print(ticket, ticket.available)
    return render_template('events/event.html', event=event, image = cover_image, organiser = organiser, address = address, venue = venue, lat = lat, lng = lng, logged_in=logged_in, tickets = tickets)

@bp.route('/create/', methods=['GET', 'POST'])
@organiser_login_required
def create_event():
    logged_in = authorisation.is_user_logged_in()
    form = EventForm()

    if form.validate_on_submit():
        venue = Venue.query.filter_by(
            name = form.venue.data,
            address1 = form.address1.data,
            address2 = form.address2.data,
            city = form.city.data,
            county = form.county.data,
            postcode = form.postcode.data
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

            New_venue_wall = VenueWall(
                venue=new_venue.id
            )
            db.session.add(New_venue_wall)
        
        new_event = Event(
            organiser_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            venue_id=venue_id
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
        album = Album.query.filter_by(event_id=new_event.id).first()
        print(album.id)
        print("Album Added")

        new_image = Image(
            name = 'Default',
            location = 'Images/default.jpg',
            album_id = new_album.id,
            image_type = 'banner_image'
        )
        db.session.add(new_image)
        db.session.commit()
        image = Image.query.filter_by(album_id=new_album.id).first()
        print(image.id)
        print("Image Added")

        flash('Event created successfully', 'success')
        return redirect(url_for('events.index'))
    
    return render_template('events/create.html', form=form, logged_in=logged_in)

@bp.route('/check_venue')
def check_venue():
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
    logged_in = authorisation.is_user_logged_in()
    event = Event.query.get_or_404(event_id)

    if event.organiser_id != current_user.id:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('events.event_page', event_id=event.id))
    
    tickets = TicketType.query.filter_by(event=event_id).all()
    
    return render_template('events/event_dashboard.html', logged_in = logged_in, event=event, tickets = tickets)

# Route for editing event information
@bp.route('/event_dashboard/<int:event_id>/edit', methods=['GET', 'POST'])
@organiser_login_required
def edit_event(event_id):
    logged_in = authorisation.is_user_logged_in()
    event = Event.query.get_or_404(event_id)

    if event.organiser_id != current_user.id:
        flash('You do not have permission to edit this event.', 'error')
        return redirect(url_for('events.event_page', event_id=event.id))

    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('events.event_dashboard', logged_in = logged_in, event_id=event.id))
    
    return render_template('events/edit_event.html', form=form, event=event)

@bp.route('/event_dashboard/<int:event_id>/add_ticket', methods=['GET','POST'])
@organiser_login_required
def add_tickets(event_id):
    logged_in = authorisation.is_user_logged_in()
    event = Event.query.get_or_404(event_id)
    if not event.organiser_id == current_user.id:
        flash('You do not have permission to add tickets to this event.', 'error')
        return redirect(url_for('events.event', event_id=event.id))  # Redirect to event detail page or somewhere else

    form = AddTicketForm()
    if form.validate_on_submit():
        deposit_amount = form.deposit_amount.data if form.depositable.data else 0
        new_ticket = TicketType(
            event=event_id,
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            depositable=form.depositable.data,
            deposit_amount=form.deposit_amount.data,
            max_tickets=form.max_tickets.data,
            tickets_sold=0
        )
        db.session.add(new_ticket)
        db.session.commit()
        flash('Ticket added successfully', 'success')
        return redirect(url_for('events.event_dashboard', event_id=event.id))
    return render_template('events/add_ticket.html', logged_in = logged_in, form=form, event=event)

@bp.route('/event_dashboard/<int:ticket_id>/edit_ticket', methods=['GET', 'POST'])
@organiser_login_required
def edit_ticket(ticket_id):
    logged_in = authorisation.is_user_logged_in()
    ticket = TicketType.query.get_or_404(ticket_id)
    event = Event.query.get_or_404(ticket.event)

    if event.organiser_id != current_user.id:
        flash('You do not have permission to edit this ticket.', 'error')
        return redirect(url_for('events.event_page', event_id=event.id))

    form = AddTicketForm(obj=ticket)
    if form.validate_on_submit():
        form.populate_obj(ticket)
        db.session.commit()
        flash('Ticket updated successfully', 'success')
        return redirect(url_for('events.event_dashboard', event_id=event.id))
    return render_template('events/edit_ticket.html', logged_in = logged_in, form=form, ticket=ticket, event=event)

@bp.route('/event_dashboard/<int:ticket_id>/delete_ticket', methods=['GET', 'POST'])
@organiser_login_required
def delete_ticket(ticket_id):
    ticket = TicketType.query.get_or_404(ticket_id)
    event = Event.query.get_or_404(ticket.event)

    if event.organiser_id != current_user.id:
        flash('You do not have permission to delete this ticket.', 'error')
        return redirect(url_for('events.event_page', event_id=event.id))

    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully', 'success')
    return redirect(url_for('events.event_page', event_id=event.id))

from flask import request

@bp.route('/toggle_ticket_active/<int:ticket_id>', methods=['POST'])
@organiser_login_required
def toggle_ticket_active(ticket_id):
    ticket = TicketType.query.get_or_404(ticket_id)

    if ticket.ticket_event.organiser_id != current_user.id:
        return jsonify({'error': 'You do not have permission to toggle this ticket'})

    # Toggle the available status of the ticket
    ticket.available = not ticket.available
    db.session.commit()
    flash('Ticket active status updated successfully', 'success')

    return redirect(url_for('events.event_dashboard', event_id=ticket.event))

@bp.route('/purchase_ticket/<int:ticket_id>', methods=['GET','POST'])
def purchase_ticket(ticket_id):
    logged_in = authorisation.is_user_logged_in()
    ticket = TicketType.query.get_or_404(ticket_id)

    form = PaymentMethodForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            ticket.tickets_sold += 1
            db.session.commit()
            flash('Ticket purchased successfully', 'success')
            return redirect(url_for('events.event_page', event_id=ticket.event))
        else:
            flash('There was an error processing your payment', 'error')
    
    return render_template('events/purchase_ticket.html', ticket=ticket, logged_in=logged_in)