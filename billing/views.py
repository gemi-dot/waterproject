
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal

from .forms import SubscriberForm, WaterBillForm, SubscriberLedgerForm
from .models import Subscriber, WaterBill, SubscriberLedger

from itertools import groupby
from operator import attrgetter

from django.db.models import Sum


def home(request):
    return render(request, 'billing/home.html')


# Subscriber Views

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


def add_subscriber(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscriber_list')
    else:
        form = SubscriberForm()
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
    return render(request, 'billing/subscriber_form.html', {'form': form})


def delete_subscriber(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk)
    if request.method == 'POST':
        subscriber.delete()
        return redirect('subscriber_list')
    return render(request, 'billing/confirm_delete.html', {'object': subscriber, 'type': 'Subscriber'})


# WaterBill Views

def waterbill_list(request):
    bills = WaterBill.objects.all().order_by('-billing_month')
    return render(request, 'billing/waterbill_list.html', {'bills': bills})


def add_water_bill(request):
    if request.method == 'POST':
        form = WaterBillForm(request.POST)
        if form.is_valid():
            water_bill = form.save(commit=False)
            rate_per_cubic_meter = Decimal('15.00')
            water_bill.amount_due = water_bill.consumption * rate_per_cubic_meter
            water_bill.save()
            return redirect('waterbill_list')
    else:
        form = WaterBillForm()
    return render(request, 'billing/waterbill_form.html', {'form': form, 'form_title': 'Add Water Bill'})


def edit_water_bill(request, pk):
    water_bill = get_object_or_404(WaterBill, pk=pk)
    if request.method == 'POST':
        form = WaterBillForm(request.POST, instance=water_bill)
        if form.is_valid():
            water_bill = form.save(commit=False)
            rate_per_cubic_meter = Decimal('15.00')
            water_bill.amount_due = water_bill.consumption * rate_per_cubic_meter
            water_bill.save()
            return redirect('waterbill_list')
    else:
        form = WaterBillForm(instance=water_bill)
    return render(request, 'billing/waterbill_form.html', {'form': form, 'form_title': 'Edit Water Bill'})


def delete_water_bill(request, pk):
    bill = get_object_or_404(WaterBill, pk=pk)
    if request.method == 'POST':
        bill.delete()
        return redirect('waterbill_list')
    return render(request, 'billing/confirm_delete.html', {'object': bill, 'type': 'Water Bill'})


# Ledger Views

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


def subscriber_ledger(request, subscriber_id):
    subscriber = get_object_or_404(Subscriber, pk=subscriber_id)
    bills = WaterBill.objects.filter(subscriber=subscriber).order_by('billing_month')
    return render(request, 'billing/ledger_list.html', {'subscriber': subscriber, 'bills': bills})


def grouped_ledger_view(request):
    ledgers = SubscriberLedger.objects.select_related('subscriber', 'water_bill').order_by('subscriber__name', '-date_paid')

    # Group entries by subscriber
    grouped_ledgers = {}
    for ledger in ledgers:
        subscriber = ledger.subscriber
        if subscriber not in grouped_ledgers:
            grouped_ledgers[subscriber] = []
        grouped_ledgers[subscriber].append(ledger)

    return render(request, 'billing/ledger_grouped.html', {'grouped_ledgers': grouped_ledgers})


def grouped_ledger_view(request):
    grouped_data = (
        SubscriberLedger.objects
        .values('subscriber__id', 'subscriber__name')
        .annotate(total_paid=Sum('amount_paid'))
        .order_by('subscriber__name')
    )
    return render(request, 'billing/grouped_ledger.html', {'grouped_data': grouped_data})


def grouped_ledger_view(request):
    # Get grouped ledger data by subscriber
    raw_data = SubscriberLedger.objects.values(
        'subscriber__id', 'subscriber__name'
    ).annotate(
        total_amount=Sum('amount_paid')
    ).order_by('subscriber__name')

    # Rename keys to clean names for the template
    grouped_data = [
        {
            'id': item['subscriber__id'],
            'name': item['subscriber__name'],
            'total_amount': item['total_amount']
        }
        for item in raw_data
    ]

    return render(request, 'billing/grouped_ledger.html', {'grouped_data': grouped_data})






