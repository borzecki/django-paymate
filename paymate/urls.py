from django.conf.urls import url
from django.contrib import admin

from accounts.views import AccountViewSet, CurrencyViewSet, TransactionViewSet

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', AccountViewSet.as_view(), name='accounts-list'),
    url(r'^payments/', TransactionViewSet.as_view(), name='payments-list'),

    url(r'^currencies/', CurrencyViewSet.as_view(), name='currencies-list')
]
