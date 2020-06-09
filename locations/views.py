from rest_framework import viewsets
from django.db import connection
from .serializers import LocationSerializer
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK)


def dictfetch(cursor, location, fetchall=False):
    """
    Returns all rows from a cursor as a dictionary.
    """

    desc = cursor.description
    if fetchall:
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    fetched = cursor.fetchone()
    if fetched is not None:
        return dict(zip([col[0] for col in desc], fetched))
    else:
        return dict(zip([col[0] for col in desc], (location, -1, -1)))


def get_location_data(locations):
    data = []
    with connection.cursor() as cursor:
        if len(locations) == 0:
            cursor.execute("SELECT loc, lat, lon FROM 'locations_location'")
            data = dictfetch(cursor, None, fetchall=True)

        for loc_ in locations:
            cursor.execute("SELECT loc, lat, lon FROM 'locations_location' WHERE loc = %s", [loc_])
            data.append(dictfetch(cursor, loc_))

    return data


# Create your views here.
class LocationViewSet(viewsets.ViewSet):
    """
    A model-less API.
    """

    def list(self, request):
        locations = request.GET.getlist('location')
        location_data = get_location_data(locations)

        my_serializer = LocationSerializer(data=location_data, many=True)
        if my_serializer.is_valid():
            return Response(my_serializer.data, status=HTTP_200_OK)
        else:
            return Response({'error': 'something went wrong :('})
