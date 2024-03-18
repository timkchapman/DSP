from flask import render_template
from LarpBook.Events import bp
from LarpBook.extensions import db
from LarpBook.Models.Events.event import Event

@bp.route('/')
def index():
    events = Event.query.all()
    return render_template('events/index.html', events=events)

@bp.route('/categories/')
def categories():
    return render_template('events/categories.html')

@bp.route('/event/<int:event_id>/')
def event_page(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('events/event.html', event=event)