from django.conf.urls import url
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

from accounts.views import AccountViewSet, CurrencyViewSet, TransactionViewSet

urlpatterns = [
    url(r'^accounts/', AccountViewSet.as_view(), name='accounts-list'),
    url(r'^payments/', TransactionViewSet.as_view(), name='payments-list'),
    url(r'^currencies/', CurrencyViewSet.as_view(), name='currencies-list'),

    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='django-paymate'))
]
