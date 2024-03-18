import json
from LarpBook.Models import models

'''# Load event ID's from the JSON file
with open('carousel.json', 'r') as f:
    event_ids = json.load(f)'''
def fetch_events_from_file(filename):
    # Load event ID's from the JSON file
    with open(filename, 'r') as f:
        event_ids = json.load(f)

    # Fetch event details from the database for each event ID
    events = []
    for event_id in event_ids:
        event = models.Event.query.get(event_id)
        if event:
            # Fetch the event description from EventDetails
            description = models.EventDetails.query.filter_by(event_id=event_id).first()
            if description:
                # Fetch the Cover Image for the event
                cover_image = models.Image.query.get(description.cover_image_id)
                if cover_image:
                    events.append({
                        'id': event.id,
                        'name': event.name,
                        'description': description.description,
                        'imageUrl': cover_image.location
                    })
    return events