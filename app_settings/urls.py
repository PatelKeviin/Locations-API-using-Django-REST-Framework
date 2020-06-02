from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register(r'settings', views.SettingViewSet, basename='setting')

urlpatterns = [
    path('', include(router.urls))
]
