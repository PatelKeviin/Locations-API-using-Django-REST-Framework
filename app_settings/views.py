from rest_framework import viewsets
from .models import Setting
from .serializers import SettingSerializer
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)


class SettingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows app settings to be viewed or edited.
    """
    serializer_class = SettingSerializer

    def get_queryset(self):
        name_param_value = self.request.query_params.get('name')
        type_param_value = self.request.query_params.get('type')

        if name_param_value is None and type_param_value is None:
            return Setting.objects.all().order_by('id')
        elif name_param_value is not None and type_param_value is None:
            return Setting.objects.filter(name=name_param_value).order_by('id')
        elif type_param_value is not None and name_param_value is None:
            return Setting.objects.filter(type=type_param_value).order_by('id')
        else:
            return Setting.objects.filter(name=name_param_value, type=type_param_value).order_by('id')

    def create(self, request, *args, **kwargs):
        name_data = request.data.get('name')
        type_data = request.data.get('type')
        value_data = request.data.get('value')

        print(name_data, type_data, value_data)
        if name_data is None or type_data is None or value_data is None:
            return Response(
                {'error': 'One of the fields from name, type or value is not given.'},
                status=HTTP_400_BAD_REQUEST
            )

        setting = Setting(name=name_data, type=type_data, value=value_data)
        setting.save()

        my_serializer = SettingSerializer(setting)
        return Response(my_serializer.data, status=HTTP_201_CREATED)

    # def retrieve(self, request, *args, **kwargs):
    #     name_param_value = request.query_params.get('name')
    #     type_param_value = request.query_params.get('type')
    #
    #     settings = None
    #
    #     if name_param_value is None and type_param_value is None:
    #         settings = Setting.objects.all().order_by('id')
    #     elif name_param_value is not None:
    #         settings = Setting.objects.filter(name=name_param_value).order_by('id')
    #     else:
    #         settings = Setting.objects.filter(type=type_param_value).order_by('id')
    #
    #     serializer = SettingSerializer(settings, many=True)
    #     return Response({"articles": serializer.data})
