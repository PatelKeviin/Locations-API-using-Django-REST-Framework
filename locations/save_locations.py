import os
import sys
import django
import requests
sys.path.append(r'C:\Users\kevin\OneDrive\Desktop\Data Science\DataDisca\module3')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_api.settings'
django.setup()
from locations.models import Location


# function to get geo-codes for locations using Google API
def get_geo_coordinates_from_google(location_address: str, connection_params: dict):
    base_url = 'https://maps.googleapis.com/maps/api/geocode'
    endpoint = '{}/{}?address={}&key={}'.format(
        base_url,
        connection_params['output_format'],
        location_address,
        connection_params['api_key']
    )

    # make the GET request
    results = requests.get(endpoint).json()
    # print(address, results)

    # check if codes were successfully obtained or not
    if results['status'] == 'ZERO_RESULTS':
        return None

    location = results['results'][0]['geometry']['location']
    return {
        'longitude': location['lng'],
        'latitude': location['lat']
    }


if __name__ == '__main__':
    # NOTE: I am using models ONLY to save data longitude and latitude data in the SQLite table

    GOOGLE_API_KEY = 'AIzaSyB9tTEiOxcABi3UB1M7uN6BwQYDN6MzFzE'
    locations = ['New York', 'California']
    connection_params_ = {
        'output_format': 'json',
        'api_key': GOOGLE_API_KEY
    }

    # saving locations data in SQLite database
    for loc in locations:
        lat_lng = get_geo_coordinates_from_google('{},+US'.format(loc), connection_params_)
        latitude = lat_lng['latitude']
        longitude = lat_lng['longitude']

        location_instance = Location(lat=latitude, lon=longitude, loc=loc)
        location_instance.save()
