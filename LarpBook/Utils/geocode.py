import os
import sys
import requests
from LarpBook import Config
import concurrent.futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

api_key = Config.GEOCODER_API_KEY

def geocode(address):
    baseUrl = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": api_key
    }

    try:
        response = requests.get(baseUrl, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)
        data = response.json()

        status = data.get('status')
        if status == 'Over_QUERY_LIMIT':
            print("Quota exceeded for the Google Maps Geocoding API.")
            return None, None
        elif status == 'ZERO_RESULTS':
            print("No results found for the provided address.")
            return None, None
        elif status == 'REQUEST_DENIED':
            print("Request denied. Check the API key.")
            return None, None
        elif status == 'INVALID_REQUEST':
            print("Invalid request. Check the address.")
            return None, None
        elif status == 'UNKNOWN_ERROR':
            print("Unknown error.")
            return None, None
        elif data.get('results'):
            # Extract latitude and longitude from the first result
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return latitude, longitude
        else:
            print("test failed.")
            return None, None

    except requests.RequestException as e:
        print("Error making geocoding request:", e)
        return None, None

    except ValueError as e:
        print("Error decoding JSON response:", e)
        return None, None


def reverseGeocode(latitude, longitude):
    baseUrl = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "latlng": f"{latitude},{longitude}",
        "key": api_key
    }
    try:
        response = requests.get(baseUrl, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)
        data = response.json()

        status = data.get('status')
        if status == 'Over_QUERY_LIMIT':
            print("Quota exceeded for the Google Maps Geocoding API.")
            return None, None
        elif status == 'ZERO_RESULTS':
            print("No results found for the provided address.")
            return None, None
        elif status == 'REQUEST_DENIED':
            print("Request denied. Check the API key.")
            return None, None
        elif status == 'INVALID_REQUEST':
            print("Invalid request. Check the address.")
            return None, None
        elif status == 'UNKNOWN_ERROR':
            print("Unknown error.")
            return None, None
        elif data.get('results'):
            for result in data['results']:
                if 'street_address' in result['types']:
                    return result['formatted_address']
                elif 'postal_code' in result['types']:
                    address = result['formatted_address']
            return address
        else:
            print("test failed.")
            return None, None

    except requests.RequestException as e:
        print("Error making geocoding request:", e)
        return None, None

    except ValueError as e:
        print("Error decoding JSON response:", e)
        return None, None

def batch_reverse_geocode(coordinates, event_ids):
    addresses = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(reverseGeocode, coord[0], coord[1]) for coord in coordinates]
        for future, coord, event_id in zip(concurrent.futures.as_completed(futures), coordinates, event_ids):
            try:
                address = future.result()
                addresses[event_id] = address  # Use event ID as the key
            except Exception as e:
                print(f"Error processing coordinate {coord}: {e}")
    return addresses

