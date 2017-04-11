from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Currency


class CurrencyViewsTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new currency object.
        """
        url = reverse('currencies-list')
        data = {'name': 'US Dollar', 'code': 'USD'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Currency.objects.count(), 1)
        self.assertEqual(Currency.objects.get().code, 'USD')
