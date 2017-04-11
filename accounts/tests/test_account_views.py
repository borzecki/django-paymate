from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account
from accounts.serializers import AccountSerializer

from .utils import create_accounts


class AccountViewsTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('accounts-list')
        data = {'name': 'Test'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'Test')

    def test_account_list(self):
        """
        Ensure GET endpoint is returning all serialized accounts.
        """
        create_accounts(10)
        url = reverse('accounts-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, AccountSerializer(Account.objects.all(), many=True).data)
