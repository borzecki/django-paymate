from django.contrib import admin

from accounts.models import Account, Currency, AccountBalance


class AccountBalanceInline(admin.TabularInline):
    model = AccountBalance
    extra = 1


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'name')
    inlines = [AccountBalanceInline]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
