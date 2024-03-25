from flask import render_template
from LarpBook.User import bp
from LarpBook import db
from LarpBook.Models.models import User, Album, Image, Event, UserContact
from LarpBook.Utils import authorisation

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
    if album:
        cover_image = Image.query.filter_by(album_id=album.id).first()
        if cover_image:
            print(cover_image.location)
    else:  
        cover_image = None
        print("Cover Image Not Found")
    
    return render_template('users/user.html', user = user, logged_in=logged_in)