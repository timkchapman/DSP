from flask import render_template
from LarpBook.Main import bp
from LarpBook import db
from LarpBook.Models.Events.event import Event
from LarpBook.Models.Events.eventdetails import EventDetails
from LarpBook.Models.Users.user import User

@bp.route('/')
def index():
	latest_events = Event.query.order_by(Event.id.desc()).limit(5).all()
	latest_event_details = EventDetails.query.order_by(EventDetails.id.desc()).limit(5).all()

	organiser_ids = [event.organiser_id for event in latest_events]
	organisers = User.query.filter(User.id.in_(organiser_ids)).all()

	organiser_names = {organiser.id: organiser.username for organiser in organisers}

	events_with_organisers = [(event, organiser_names.get(event.organiser_id)) for event in latest_events]

	combined_data = zip(events_with_organisers, latest_event_details)
	return render_template('index.html', combined_data=combined_data)