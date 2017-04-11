from accounts.models import Account, Currency


def create_accounts(number=1):
    """
    Create test accounts.

    :param number: number of test instances to create.
    :return: 
    """
    return [Account.objects.create(name='test_%s' % i) for i in range(number)]


def create_currencies(number=1):
    """
    Create test currency.
    
    :param number: number of test instances to create.
    :return: 
    """
    return [Currency.objects.create(name='Test Currency %s' % i, code='TS%s' % i) for i in range(number)]
