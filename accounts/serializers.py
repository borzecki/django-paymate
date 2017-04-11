from rest_framework import fields
from rest_framework.serializers import ModelSerializer

from .models import Account, Currency, Transaction, AccountBalance


class AccountBalanceSerializer(ModelSerializer):
    class Meta:
        model = AccountBalance
        fields = ('balance', 'currency')


class AccountSerializer(ModelSerializer):
    balances = fields.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'name', 'balances')

    def get_balances(self, instance):
        return AccountBalanceSerializer(instance.accountbalance_set.all(), many=True).data


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'name', 'code')


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'created', 'from_account', 'to_account',
                  'amount', 'currency')
