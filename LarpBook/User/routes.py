from flask import render_template
from LarpBook.User import bp
from LarpBook import db
from LarpBook.Models.models import User, Album, Image, Ticket, Event, UserContact, userevents, TicketType
from LarpBook.Utils import authorisation, user_events

@bp.route('/')
def index():
    logged_in = authorisation.is_user_logged_in()
    return render_template('users/index.html', logged_in=logged_in)

@bp.route('/organiser/<int:id>/')
def organiser_page(id):
    logged_in = authorisation.is_user_logged_in()
    organiser = User.query.get_or_404(id)
    album = Album.query.filter_by(name='Default', user_id=organiser.id).first()
    if album:
        cover_image = Image.query.filter_by(album_id=album.id).first()
        if cover_image:
            print(cover_image.location)
    else:  
        cover_image = None
        print("Cover Image Not Found")

    contacts = UserContact.query.filter_by(user=organiser.id).all()
    for contact in contacts:
        print(contact.contact_value)

    events = Event.query.filter_by(organiser_id=organiser.id).all()

    return render_template('users/organiser.html', organiser = organiser, logged_in=logged_in, album=album, events = events, image = cover_image, contacts = contacts)

@bp.route('/user/<int:id>/')
def user_page(id):
    logged_in = authorisation.is_user_logged_in()
    user = User.query.get_or_404(id)

    album = Album.query.filter_by(name='Default', user_id=user.id).first()
    cover_image = Image.query.filter_by(album_id=album.id).first() if album else None

    events = user_events.user_has_events(user.id)

    tickets = Ticket.query.filter_by(user_id=user.id).all()

    # Fetch name and price from TicketType for each ticket
    ticket_details = []
    for ticket in tickets:
        ticket_type = TicketType.query.get(ticket.ticket_type_id)
        ticket_details.append({
            'event_name': ticket_type.event.name,
            'ticket_type_name': ticket_type.name,
            'ticket_price': ticket_type.price,
            'ticket_code': ticket.ticket_code
        })

    return render_template('users/user.html', user=user, logged_in=logged_in, album=album,
                           image=cover_image, events=events, tickets=tickets, ticket_details=ticket_details)
