import uuid

from django.db import models


class Currency(models.Model):
    """
    Model for representing currency.
    """

    class Meta:
        verbose_name_plural = 'Currencies'
        unique_together = ('name', 'code')

    created = models.DateTimeField(verbose_name='created on', auto_now_add=True)
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=3)

    def __str__(self):
        return 'Currency: %s' % self.name


class Account(models.Model):
    """
    Identity that can hold a balance of every currency.
    The name is the unique account identifier. (e.g. "user-892").
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(verbose_name='created on', auto_now_add=True, db_index=True)
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return 'Account: %s' % self.name


class AccountBalance(models.Model):
    """
    The balance of an account in a certain currency.
    """
    account = models.ForeignKey('Account', null=True)
    currency = models.ForeignKey('Currency')
    balance = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    allow_negative_balance = models.BooleanField(default=False)

    def can_transfer(self, amount):
        """
        Checks if specific amount can be transferred from Account.
        Special types of `AccountBalance` instances without assigned `Account`'s are `Banks`.

        :param amount: amount to transfer
        :return: True if conditions are met, False otherwise
        """
        return any([self.allow_negative_balance, self.account is None, self.balance >= amount])


class Transaction(models.Model):
    """
    Transfer between two account.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(verbose_name='created on', db_index=True, auto_now_add=True)
    from_account = models.ForeignKey('Account', null=True, db_index=True, related_name='transactions_from')
    to_account = models.ForeignKey('Account', null=True, db_index=True, related_name='transactions_to')
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    currency = models.ForeignKey('Currency')

    def is_pointless(self):
        """
        Pointless transaction would be the one which is issued for no amount of funds or from/to the same account.

        :return: True if conditions are met, False otherwise
        """
        return any([self.amount == 0, self.from_account == self.to_account])
