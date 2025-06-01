from django import forms
from .models import Subscriber, WaterBill, SubscriberLedger

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'barangay', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class WaterBillForm(forms.ModelForm):
    class Meta:
        model = WaterBill
        fields = ['subscriber', 'billing_month', 'consumption', 'due_date']

        widgets = {
            'billing_month': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SubscriberLedgerForm(forms.ModelForm):
    class Meta:
        model = SubscriberLedger
        fields = ['subscriber', 'water_bill', 'date_paid', 'amount_paid', 'remarks']

        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }
