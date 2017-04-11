from rest_framework.exceptions import APIException


class TransactionDenied(APIException):
    status_code = 400
    default_detail = "Transaction has been denied due to lack of funds."
    default_code = 'transaction_denied'


class PointlessTransaction(APIException):
    status_code = 400
    default_detail = "This transaction simply doesn't make sense."
    default_code = 'pointless_transaction'
