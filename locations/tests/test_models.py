from django.test import TestCase
from . import setup_django
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
