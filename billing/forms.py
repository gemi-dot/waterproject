from django import forms
from .models import Subscriber, WaterBill

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'barangay', 'address']

class WaterBillForm(forms.ModelForm):
    class Meta:
        model = WaterBill
        fields = ['subscriber', 'billing_month', 'amount_due', 'due_date']
