from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.exceptions import PointlessTransaction, TransactionDenied
from accounts.models import Currency, Account, AccountBalance, Transaction
from accounts.tests.utils import create_accounts, create_currencies


def setup():
    create_accounts(2)
    create_currencies(1)


class PaymentViewsTests(APITestCase):
    def setUp(self):
        super().setUp()
        setup()

    def test_bank_payment(self):
        """
        Ensure we can supply account with funds from the "Bank".
        """
        response = self.payment(None, Account.objects.latest('pk').id, 200)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AccountBalance.objects.get(account=Account.objects.latest('pk').id).balance, 200)

    def test_payment_balance_correct(self):
        """
        Test performing transfer from one account to another.
        """
        from_account, to_account = Account.objects.all()

        self.payment(None, from_account.id, 200)
        response = self.payment(from_account.id, to_account.id, 200)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AccountBalance.objects.get(account=to_account.id).balance, 200)
        self.assertEqual(AccountBalance.objects.get(account=from_account.id).balance, 0)
        self.assertEqual(Transaction.objects.count(), 2)

    def test_pointless_payment_same_account(self):
        """
        Ensure `PointlessTransaction` is raised when `from_account` and `to_account` are equal.
        """
        response = self.payment(None, None, 20)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], PointlessTransaction.default_detail)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_pointless_payment_no_amount(self):
        """
        Ensure `PointlessTransaction` is raised when no amount is given.
        """
        from_account, to_account = Account.objects.all()
        response = self.payment(from_account.id, to_account.id, 0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], PointlessTransaction.default_detail)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_transaction_denied(self):
        """
        Ensure `PointlessTransaction` is raised with insufficient funds.
        """
        from_account, to_account = Account.objects.all()
        response = self.payment(from_account.id, to_account.id, 200)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], TransactionDenied.default_detail)
        self.assertEqual(Transaction.objects.count(), 0)

    def payment(self, from_account, to_account, amount, currency=None):
        """
        Perform a payment from `from_account` to `to_account` with specified `amount` of `currency`.
        
        :param from_account: id of Account object (can be None) 
        :param to_account: id of Account object (can be None)

        :param amount: amount to transfer between accounts
        :param currency: Currency object
        :return: Response object
        """
        if not currency:
            currency = Currency.objects.get()

        data = {'from_account': from_account, 'to_account': to_account,
                'currency': currency.id, 'amount': amount}
        return self.client.post(reverse('payments-list'), data, format='json')
