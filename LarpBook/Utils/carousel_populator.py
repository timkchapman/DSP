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
            # Fetch the associated album for the event
            album = models.Album.query.filter(models.Album.event.has(id=event_id)).first()

            # If album exists, fetch the first image from it
            if album:
                cover_image = models.Image.query.filter_by(album_id=album.id).first()
                if cover_image:
                    events.append({
                        'id': event.id,
                        'name': event.name,
                        'description': event.description,
                        'imageUrl': cover_image.location
                    })
    return events
