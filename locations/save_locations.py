import os
import sys
import django
import requests
import csv
sys.path.append(r'C:\Users\kevin\OneDrive\Desktop\Data Science\DataDisca\module3')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_api.settings'
django.setup()
from locations.models import Location


# function to get geo-codes for locations using Google API
def get_geo_coordinates_from_google(location_address: str, connection_params: dict):
    """
    Method to geo-code human readable address into latitudes and longitude codes using Google API.

    :param location_address: Physical address to geocode
    :param connection_params: Google API credentials for authorisation
    :return : Geocode information for the location
    """

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


def get_locations(path: str) -> list:
    """
    Method to retrieve unique locations from 'product_a' csv file.

    :param path: Path to 'product_a' csv file
    :return list: Unique locations as a list
    """
    unique_locations = set()

    with open(path) as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            unique_locations.add(row[13])

    return list(unique_locations)


if __name__ == '__main__':
    # NOTE: I am using models ONLY to save data longitude and latitude data in the SQLite table

    # get unique locations to save to database
    path_to_csv = r'C:\Users\kevin\OneDrive\Desktop\Data Science\DataDisca\module3\locations\data\product_a.csv'
    locations = get_locations(path_to_csv)

    # api key credentials
    GOOGLE_API_KEY = 'Your key'
    connection_params_ = {
        'output_format': 'json',
        'api_key': GOOGLE_API_KEY
    }

    # saving locations data in SQLite database
    for loc in locations:
        lat_lng = get_geo_coordinates_from_google('{},+US'.format(loc), connection_params_)

        if lat_lng is not None:
            latitude = lat_lng['latitude']
            longitude = lat_lng['longitude']

            location_instance = Location(lat=latitude, lon=longitude, loc=loc)
            location_instance.save()
