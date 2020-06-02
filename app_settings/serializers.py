from rest_framework import serializers
from .models import Setting


class SettingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Setting
        fields = ['id', 'name', 'type', 'value']
