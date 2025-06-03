
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.db.models import Sum, Q

from .forms import SubscriberForm, WaterBillForm, SubscriberLedgerForm
from .models import Subscriber, WaterBill, SubscriberLedger


from django.db.models.functions import TruncMonth


def home(request):
    return render(request, 'billing/home.html')


# -------------------
# Subscriber Views
# -------------------

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


# -------------------
# WaterBill Views
# -------------------

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


# -------------------
# Ledger Views
# -------------------

def add_ledger_entry(request):
    if request.method == 'POST':
        form = SubscriberLedgerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ledger_list')
    else:
        form = SubscriberLedgerForm()
    return render(request, 'billing/add_ledger_entry.html', {'form': form})


def subscriber_ledger(request, subscriber_id):
    subscriber = get_object_or_404(Subscriber, pk=subscriber_id)
    bills = WaterBill.objects.filter(subscriber=subscriber).order_by('billing_month')
    payments = SubscriberLedger.objects.filter(subscriber=subscriber).order_by('-date_paid')

    total_due = bills.aggregate(Sum('amount_due'))['amount_due__sum'] or 0
    total_paid = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    balance = total_due - total_paid

    context = {
        'subscriber': subscriber,
        'bills': bills,
        'payments': payments,
        'total_due': total_due,
        'total_paid': total_paid,
        'balance': balance,
    }
    return render(request, 'billing/subscriber_ledger.html', context)


def grouped_ledger(request):
    ledgers = SubscriberLedger.objects.all().order_by('subscriber__barangay', 'subscriber__name')
    context = {'ledgers': ledgers}
    return render(request, 'billing/grouped_ledger.html', context)




def ledger_list(request):
    subscriber_name = request.GET.get('subscriber_name', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    ledgers = SubscriberLedger.objects.all().order_by('-date_paid')

    if subscriber_name:
        ledgers = ledgers.filter(subscriber__name__icontains=subscriber_name)
    if date_from:
        ledgers = ledgers.filter(date_paid__gte=date_from)
    if date_to:
        ledgers = ledgers.filter(date_paid__lte=date_to)

    context = {
        'ledgers': ledgers,
        'subscriber_name': subscriber_name,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'billing/ledger_list.html', context)



# views.py


def grouped_ledger_view(request):
    subscribers = Subscriber.objects.all().order_by('barangay', 'name')
    ledger_data = []

    for subscriber in subscribers:
        entries = SubscriberLedger.objects.filter(subscriber=subscriber).order_by('-date_paid')
        total_paid = entries.aggregate(total=Sum('amount_paid'))['total'] or 0

        if entries.exists():
            ledger_data.append({
                'subscriber': subscriber,
                'entries': entries,
                'total_paid': total_paid
            })

    return render(request, 'billing/grouped_ledger.html', {'ledger_data': ledger_data})
