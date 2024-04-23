from LarpBook.Models.models import Event, Ticket

def user_has_events(user_id):
    user_tickets = Ticket.query.filter_by(user_id=user_id).all()

    if user_tickets:
        event_ids = [ticket.event_id for ticket in user_tickets]
        user_events_query = Event.query.filter(Event.id.in_(event_ids))
        return user_events_query
    else:
        return Event.query.filter_by(id=None)  # Return an empty query to avoid errors
