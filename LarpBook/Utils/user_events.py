from LarpBook.Models.models import Event, Ticket

def user_has_events(user_id):
    user_tickets = Ticket.query.filter_by(user_id=user_id).all()

    if user_tickets:
        event_ids = [ticket.event_id for ticket in user_tickets]

        user_events = Event.query.filter(Event.id.in_(event_ids)).all()

        return user_events
    else:
        return None