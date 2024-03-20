import json
from LarpBook.Models import models

def fetch_events_from_file(filename):
    # Load event IDs from the JSON file
    with open(filename, 'r') as f:
        event_ids = json.load(f)

    # Fetch event details from the database for each event ID
    events = []
    for event_id in event_ids:
        event = models.Event.query.get(event_id)
        if event:
            # Fetch the Cover Image for the event
            cover_image = models.Image.query.get(event.cover_image_id)
            if cover_image:
                events.append({
                    'id': event.id,
                    'name': event.name,
                    'description': event.description,
                    'imageUrl': cover_image.location
                })
    return events
