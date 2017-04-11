from django.db.transaction import atomic
from rest_framework import generics

from .exceptions import TransactionDenied, PointlessTransaction
from .models import Account, Currency, Transaction, AccountBalance
from .serializers import AccountSerializer, CurrencySerializer, TransactionSerializer


class AccountViewSet(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CurrencyViewSet(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class TransactionViewSet(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @atomic
    def perform_create(self, serializer):
        transaction = serializer.save()
        to_balance, _ = AccountBalance.objects.get_or_create(currency=transaction.currency,
                                                             account=transaction.to_account)
        from_balance, _ = AccountBalance.objects.get_or_create(currency=transaction.currency,
                                                               account=transaction.from_account)

        if transaction.is_pointless():
            raise PointlessTransaction()

        if not from_balance.can_transfer(transaction.amount):
            raise TransactionDenied()

        to_balance.balance += transaction.amount
        from_balance.balance -= transaction.amount
        to_balance.save()
        from_balance.save()
