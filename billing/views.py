
from django.shortcuts import render, redirect, get_object_or_404, redirect

from .forms import SubscriberForm, WaterBillForm
from .models import Subscriber, WaterBill
from django.db.models import Q

from decimal import Decimal

from .models import SubscriberLedger
from .forms import SubscriberLedgerForm


def home(request):
    return render(request, 'billing/home.html')


def add_subscriber(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscriber_list')
    else:
        form = SubscriberForm()
 #   return render(request, 'billing/add_subscriber.html', {'form': form})
    return render(request, 'billing/subscriber_form.html', {'form': form})


def edit_subscriber(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk)
    
    if request.method == 'POST':
        form = SubscriberForm(request.POST, instance=subscriber)
        if form.is_valid():
            form.save()
            return redirect('subscriber_list')
    else:
        form = SubscriberForm(instance=subscriber)

    #return render(request, 'billing/edit_subscriber.html', {'form': form})
    return render(request, 'billing/subscriber_form.html', {'form': form})


def delete_subscriber(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk)
    if request.method == 'POST':
        subscriber.delete()
        return redirect('subscriber_list')
    return render(request, 'billing/confirm_delete.html', {'subscriber': subscriber})


def subscriber_list(request):
    query = request.GET.get('q')
    barangays = Subscriber.objects.values_list('barangay', flat=True).distinct().order_by('barangay')

    if query:
        subscribers = Subscriber.objects.filter(barangay=query)
    else:
        subscribers = Subscriber.objects.all()

    return render(request, 'billing/subscriber_list.html', {
        'subscribers': subscribers,
        'barangays': barangays,
        'query': query
    })



def add_water_bill(request):
    if request.method == 'POST':
        form = WaterBillForm(request.POST)
        if form.is_valid():
            water_bill = form.save(commit=False)
            # Use Decimal for monetary calculation
            rate_per_cubic_meter = Decimal('15.0')
            water_bill.amount_due = water_bill.consumption * rate_per_cubic_meter
            water_bill.save()
            return redirect('waterbill_list')
    else:
        form = WaterBillForm()
    
    context = {
        'form': form,
        'form_title': 'Add Water Bill',
    }
    return render(request, 'billing/add_water_bill.html', context)


def edit_water_bill(request, pk):
    water_bill = get_object_or_404(WaterBill, pk=pk)
    if request.method == 'POST':
        form = WaterBillForm(request.POST, instance=water_bill)
        if form.is_valid():
            water_bill = form.save(commit=False)
            rate_per_cubic_meter = Decimal('15.0')
            water_bill.amount_due = water_bill.consumption * rate_per_cubic_meter
            water_bill.save()
            return redirect('waterbill_list')
    else:
        form = WaterBillForm(instance=water_bill)
    
    context = {
        'form': form,
        'form_title': 'Edit Water Bill',
    }
    return render(request, 'billing/add_water_bill.html', context)




def delete_water_bill(request, pk):
    bill = get_object_or_404(WaterBill, pk=pk)

    if request.method == 'POST':
        bill.delete()
        return redirect('waterbill_list')

    return render(request, 'billing/confirm_delete.html', {
        'object': bill,
        'type': 'Water Bill',
    })



def waterbill_list(request):
    bills = WaterBill.objects.all().order_by('-billing_month')
    return render(request, 'billing/waterbill_list.html', {'bills': bills})



def ledger_list(request):
    ledgers = SubscriberLedger.objects.select_related('subscriber', 'water_bill').order_by('-date_paid')
    return render(request, 'billing/ledger_list.html', {'ledgers': ledgers})

def add_ledger_entry(request):
    if request.method == 'POST':
        form = SubscriberLedgerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ledger_list')
    else:
        form = SubscriberLedgerForm()
    return render(request, 'billing/ledger_form.html', {'form': form, 'form_title': 'Add Payment'})
