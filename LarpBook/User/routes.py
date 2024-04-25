from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from LarpBook.User import bp
from LarpBook import db
from LarpBook.Models.models import User, Tags, Album, Image, Ticket, Event, UserContact, userevents, TicketType
from LarpBook.Utils.user_events import user_has_events
from LarpBook.Utils.authorisation import organiser_login_required, is_user_logged_in
from flask_login import login_required, current_user
from LarpBook.Static.Forms.forms import EditEmailForm, EditWebsiteForm, EditAboutForm, EditPasswordForm, EditTagsForm
from LarpBook.extensions import bcrypt
from LarpBook.Auth.routes import logout_user


@bp.route('/')
def index():
    logged_in = is_user_logged_in()
    return render_template('users/index.html', logged_in=logged_in)

@bp.route('/organiser/<int:id>/')
def organiser_page(id):
    logged_in = is_user_logged_in()
    user = User.query.get_or_404(id)
    album = Album.query.filter_by(name='Default', user_id=user.id).first()
    if album:
        cover_image = Image.query.filter_by(album_id=album.id).first()
        if cover_image:
            print(cover_image.location)
    else:  
        cover_image = None
        print("Cover Image Not Found")

    contacts = UserContact.query.filter_by(user=user.id).all()
    for contact in contacts:
        print(contact.contact_value)

    events = Event.query.filter_by(organiser_id=user.id).all()
    return render_template('users/organiserwall.html', 
                           logged_in = logged_in,
                           user = user, 
                           album=album, 
                           events = events, 
                           image = cover_image, 
                           contacts = contacts)

@bp.route('/organiser_dashboard/<int:id>', methods=['GET', 'POST'])
@login_required
def organiser_dashboard(id):
    logged_in = is_user_logged_in()
    user = User.query.get_or_404(id)

    user_contact = UserContact.query.filter_by(user=user.id).all()

    edit_password_form = EditPasswordForm()
    edit_email_form = EditEmailForm()
    edit_about_form = EditAboutForm()
    edit_website_form = EditWebsiteForm()

    if user.id != id:
        abort(404)

    about = user.about
    website = user.website

    return render_template('users/organiser_dashboard.html',
                        logged_in=logged_in,
                        user=user, 
                        contacts=user_contact,
                        edit_password_form=edit_password_form,
                        edit_email_form=edit_email_form,
                        edit_about_form=edit_about_form,
                        edit_website_form=edit_website_form,
                        website = website,
                        about = about)


@bp.route('/user/<int:id>/')
def user_page(id):
    logged_in = is_user_logged_in()
    user = User.query.get_or_404(id)
    if user.is_organiser:
        return redirect(url_for('user.organiser_page', id=user.id))

    album = Album.query.filter_by(name='Default', user_id=user.id).first()
    cover_image = Image.query.filter_by(album_id=album.id).first() if album else None

    events = user_has_events(user.id)
    soonest_events = sorted(events, key=lambda x: x.start_date)[:5]

    tickets = Ticket.query.filter_by(user_id=user.id).all()

    # Fetch name and price from TicketType for each ticket
    ticket_details = []
    for ticket in tickets:
        ticket_type = TicketType.query.get(ticket.ticket_type_id)
        event_name_cleaned = ticket_type.event.name.replace(' ', '_')
        
        ticket_location = url_for('static', filename=f'Tickets/{event_name_cleaned}/ticket_{ticket.id}.pdf')
        print(ticket_location)
        ticket_details.append({
            'event_name': ticket_type.event.name,
            'ticket_type_name': ticket_type.name,
            'ticket_price': ticket_type.price,
            'ticket_code': ticket.ticket_code,
            'ticket_location': ticket_location
        })

    return render_template('users/userwall.html', 
                            logged_in=logged_in,
                            user=user, 
                            album=album,
                            image=cover_image, 
                            events=soonest_events, 
                            tickets=tickets, 
                            ticket_details=ticket_details)

# Route for the user dashboard
@bp.route('/user_dashboard/<int:id>', methods=['GET', 'POST'])
@login_required
def user_dashboard(id):
    logged_in = is_user_logged_in()
    user = User.query.get_or_404(id)
    if user.is_organiser:
        return redirect(url_for('user.organiser_dashboard', id=user.id))

    user_contact = UserContact.query.filter_by(user=user.id).all()

    if user.id != id:
        abort(404)

    edit_password_form = EditPasswordForm()
    edit_email_form = EditEmailForm()
    edit_tags_form = EditTagsForm()
    edit_about_form = EditAboutForm()

    existing_tags = [tag.tag for tag in user.tags]
    existing_tag_string = ', '.join(existing_tags)

    about = user.about

    return render_template('users/user_dashboard.html',
                        logged_in=logged_in,
                        user=user, 
                        contacts=user_contact,
                        edit_password_form=edit_password_form,
                        edit_email_form=edit_email_form,
                        edit_tags_form=edit_tags_form,
                        edit_about_form=edit_about_form,
                        tags = existing_tag_string,
                        about = about)

@bp.route('/delete_account/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    user = User.query.get_or_404(id)

    # Check if the current user has permission to delete the account
    if current_user.id != user.id:
        abort(404)

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    logout_user()

    return redirect(url_for('main.index'))


@bp.route('/edit_password/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_password(id):
    form = EditPasswordForm()

    if form.validate_on_submit():
        # Fetch the user
        user = User.query.get_or_404(id)

        # Check if the current password matches the user's password
        if not bcrypt.check_password_hash(user.password, form.current_password.data):
            flash('Incorrect current password.', 'error')
            if not user.is_organiser:
                return redirect(url_for('user.user_dashboard', id=user.id))
            return redirect(url_for('user.organiser_dashboard', id=user.id))

        # Hash the new password
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')

        # Update the user's password
        user.password = hashed_password
        db.session.commit()

        flash('Password updated successfully.', 'success')
        if not user.is_organiser:
            return redirect(url_for('user.user_dashboard', id=user.id))
        return redirect(url_for('user.organiser_dashboard', id=user.id))

    return render_template('edit_password.html', 
                           form=form)

@bp.route('/edit_email/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_email(id):
    logged_in = is_user_logged_in()
    user = User.query.get_or_404(id)

    if current_user.id != user.id:
        flash('You do not have permission to edit this user.', 'error')
        if not user.is_organiser:
            return redirect(url_for('users.user_page', id=user.id))
        return redirect(url_for('users.organiser_page', id=user.id))
    
    email_contact = UserContact.query.filter_by(user=user.id).first()

    form = EditEmailForm()

    if form.validate_on_submit():

        # Check if the password matches the user's password
        if not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Incorrect current password.', 'error')
            if not user.is_organiser:
                return redirect(url_for('user.user_dashboard', id=user.id))
            return redirect(url_for('user.organiser_dashboard', id=user.id))
        
        email_contact.contact_value = form.email.data
        db.session.commit()
        flash('Email updated successfully', 'success')
        if not user.is_organiser:
            return redirect(url_for('user.user_dashboard', id=user.id))
        return redirect(url_for('user.organiser_dashboard', id=user.id))

    return render_template('edit_email.html', 
                           logged_in=logged_in,
                           email = email_contact, 
                           form=form)

@bp.route('/edit_tags/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tags(id):
    logged_in = is_user_logged_in()
    user = User.query.get_or_404(id)

    if current_user.id != user.id:
        flash('You do not have permission to edit this user.', 'error')
        if not user.is_organiser:
            return redirect(url_for('user.user_page', id=user.id))
        return redirect(url_for('users.organiser_page', id=user.id))

    form = EditTagsForm()

    if form.validate_on_submit():

        # Split the tag string into individual tag names
        tag_names = [tag.strip().lower() for tag in form.tags.data.split(',')]
        
        unique_tags = set(tag_names)

       # Create or fetch existing tags and associate them with the event
        user.tags.clear()  # Clear existing tags
        for tag_name in unique_tags:
            # Check if the tag already exists
            existing_tag = Tags.query.filter_by(tag=tag_name).first()
            
            if not existing_tag:
                # If tag does not exist, create a new one
                new_tag = Tags(tag=tag_name)
                db.session.add(new_tag)
                user.tags.append(new_tag)
            else:
                # If tag exists, use the existing one
                user.tags.append(existing_tag)

        db.session.commit()

        flash('Tags updated successfully', 'success')
        if not user.is_organiser:
            return redirect(url_for('user.user_dashboard', id=user.id))
        return redirect(url_for('user.organiser_dashboard', id=user.id))

    return render_template('edit_tags.html', 
                           logged_in=logged_in,
                           form=form)

@bp.route('/edit_about/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_about(id):
    logged_in = is_user_logged_in()
    user = User.query.get_or_404(id)

    if current_user.id != user.id:
        flash('You do not have permission to edit this user.', 'error')
        if not user.is_organiser:
            return redirect(url_for('user.user_page', id=user.id))
        return redirect(url_for('users.organiser_page', id=user.id))

    form = EditAboutForm()

    if form.validate_on_submit():
        user.about = form.about.data
        db.session.commit()
        flash('About updated successfully', 'success')
        if not user.is_organiser:
            return redirect(url_for('user.user_dashboard', id=user.id))
        return redirect(url_for('user.organiser_dashboard', id=user.id))

    return render_template('edit_about.html', 
                           logged_in=logged_in,
                           form=form)

@bp.route('edit_website/<int:id>', methods=['GET', 'POST'])
@organiser_login_required
def edit_website(id):
    logged_in = is_user_logged_in()
    user = User.query.get_or_404(id)

    if current_user.id != user.id:
        flash('You do not have permission to edit this user.', 'error')
        return redirect(url_for('users.organiser_page', id=user.id))
    
    form = EditWebsiteForm()

    if form.validate_on_submit():
        user.website = form.website.data
        db.session.commit()
        flash('Website updated successfully', 'success')
        return redirect(url_for('user.organiser_dashboard', id=user.id))
    

