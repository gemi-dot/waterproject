
from django.shortcuts import render, redirect
from .forms import SubscriberForm, WaterBillForm
from .models import Subscriber, WaterBill
from django.db.models import Q

def add_subscriber(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscriber_list')
    else:
        form = SubscriberForm()
    return render(request, 'billing/add_subscriber.html', {'form': form})

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
            form.save()
            return redirect('waterbill_list')
    else:
        form = WaterBillForm()
    return render(request, 'billing/add_water_bill.html', {'form': form})

def waterbill_list(request):
    bills = WaterBill.objects.select_related('subscriber').all()
    return render(request, 'billing/waterbill_list.html', {'bills': bills})
