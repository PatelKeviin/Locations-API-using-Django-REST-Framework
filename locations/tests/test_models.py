from django.test import TestCase
import sys
import os
import django
sys.path.append(r'C:\Users\kevin\OneDrive\Desktop\Data Science\DataDisca\module3')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_api.settings'
django.setup()
from ..models import Location


class LocationTest(TestCase):
    """
    Test Module for Location model.
    """
    def setUp(self) -> None:
        """
        Create dummy location models for testing purposes.
        """
        Location.objects.create(loc='Melbourne', lat=37.8136, lon=144.9631)
        Location.objects.create(loc='Sydney', lat=33.8688, lon=151.2093)

    def test_location(self):
        mel_location = Location.objects.get(loc='Melbourne')
        syd_location = Location.objects.get(loc='Sydney')

        self.assertEqual(mel_location.__str__(), 'Melbourne')
        self.assertEqual(syd_location.__str__(), 'Sydney')
