from django import forms
from .models import Subscriber, WaterBill, SubscriberLedger

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'barangay', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'barangay': forms.TextInput(attrs={'class': 'form-control'}),
            # 'barangay': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

class WaterBillForm(forms.ModelForm):
    class Meta:
        model = WaterBill
        fields = ['subscriber', 'billing_month', 'consumption', 'due_date']
        widgets = {
            'subscriber': forms.Select(attrs={'class': 'form-select'}),
            'billing_month': forms.TextInput(attrs={'class': 'form-control'}),
            'consumption': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class SubscriberLedgerForm(forms.ModelForm):
    class Meta:
        model = SubscriberLedger
        fields = '__all__'
        widgets = {
            'subscriber': forms.Select(attrs={'class': 'form-select'}),
            'water_bill': forms.Select(attrs={'class': 'form-select'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_paid': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }