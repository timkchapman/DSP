from LarpBook import Config
import requests

api_key = Config.GEOCODER_API_KEY

def geocode(address):
    baseUrl = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": api_key
    }

    response = requests.get(baseUrl, params = params)
    data = response.json()

    if data.get('results'):
        #Extract latitude and longitude from the first result
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        return latitude, longitude
    else:
        return None, None
    
def reverseGeocode(latitude, longitude):
    baseUrl = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "latlng": f"{latitude},{longitude}",
        "key": api_key
    }

    response = requests.get(baseUrl, params = params)
    data = response.json()

    if data.get('results'):
        for result in data['results']:
        # Check if result_type is street_address
            if 'street_address' in result['types']:
                return result['formatted_address']
            # If street address not found, check for postal_code
            elif 'postal_code' in result['types']:
                address = result['formatted_address']
        return address
    else:
        return None