from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    loc = serializers.CharField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
