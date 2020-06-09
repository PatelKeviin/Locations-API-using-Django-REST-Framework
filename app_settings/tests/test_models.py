from django.test import TestCase
import sys
import os
import django
sys.path.append(r'C:\Users\kevin\OneDrive\Desktop\Data Science\DataDisca\module3')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_api.settings'
django.setup()
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
