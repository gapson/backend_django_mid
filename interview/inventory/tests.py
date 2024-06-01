from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from interview.inventory.models import Inventory, InventoryTag, InventoryLanguage, InventoryType


class InventoryListCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.inventory_type = InventoryType.objects.create(name="Test Type")
        self.inventory_language = InventoryLanguage.objects.create(name="Test Language")
        self.inventory_tag = InventoryTag.objects.create(name="Test Tag")
        self.inventory1 = Inventory.objects.create(
            name="Test Inventory 1", type=self.inventory_type, language=self.inventory_language, metadata={}
        )
        self.inventory2 = Inventory.objects.create(
            name="Test Inventory 2", type=self.inventory_type, language=self.inventory_language, metadata={}
        )
        self.url = reverse('inventory-list')

    def test_get_inventories_filtered_by_date(self):
        # Create test inventories with different creation dates

        # Simulate a GET request with a specific date filter
        today = datetime.now().date()
        response = self.client.get(self.url, {'date': today})

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        tomorrow = today + timedelta(days=1)
        response = self.client.get(self.url, {'date': tomorrow})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that only inventories created after the specified date are returned
        self.assertEqual(len(response.data), 0)  # No inventory created after the date

    def test_get_inventories_bad_date_format(self):
        bad_date = "invalid-date-format"  # Bad date format
        response = self.client.get(self.url, {'date': bad_date})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_msg = {'error': 'Invalid date format. Use YYYY-MM-DD.'}
        self.assertEqual(response.data, expected_error_msg)

    # Add more test cases as needed to cover other functionalities
