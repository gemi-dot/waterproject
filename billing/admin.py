
# Register your models here.
from django.contrib import admin
from .models import Subscriber, WaterBill, LedgerEntry

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('name', 'barangay', 'address')
    search_fields = ('name', 'barangay')

@admin.register(WaterBill)
class WaterBillAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'billing_month', 'amount_due', 'due_date')
    list_filter = ('billing_month',)
    search_fields = ('subscriber__name',)

@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'description', 'amount', 'entry_date')
    list_filter = ('entry_date',)
    search_fields = ('subscriber__name', 'description')
