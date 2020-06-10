from django.test import TestCase
from . import setup_django
from ..models import Setting


class SettingTest(TestCase):
    """
        Test Module for Location model.
    """

    def setUp(self) -> None:
        """
        Create dummy Setting models for testing purposes.
        """
        Setting.objects.create(name='test_name', type='test_type', value='test_value')

    def test_location(self):
        """
        Test whether the Setting models have been created in the SQLite database.
        """
        my_setting = Setting.objects.get(name='test_name')
        self.assertEqual(my_setting.__str__(), 'test_name')
