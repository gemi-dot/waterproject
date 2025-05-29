from django import forms
from .models import Subscriber, WaterBill

from django import forms
from .models import Subscriber

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'barangay', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'barangay': forms.TextInput(attrs={'class': 'form-control'}),
            #'barangay': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),  # single-line input, not textarea
        }

class WaterBillForm(forms.ModelForm):
    class Meta:
        model = WaterBill
        fields = ['subscriber', 'billing_month', 'amount_due', 'due_date']