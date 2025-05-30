from django.db import models

from decimal import Decimal
#rom .models import Subscriber, WaterBill

# Create your models here.

class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class WaterBill(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    billing_month = models.CharField(max_length=20)  # e.g. "May 2025"

    consumption = models.DecimalField(max_digits=10, decimal_places=2)  # cubic meters consumed
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    def save(self, *args, **kwargs):
        # Example: rate is 15 pesos per cubic meter
        rate_per_cubic_meter = 15
        self.amount_due = self.consumption * rate_per_cubic_meter
        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.subscriber.name} - {self.billing_month}"

class LedgerEntry(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.subscriber.name} - {self.description}"
    

class SubscriberLedger(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    water_bill = models.ForeignKey(WaterBill, on_delete=models.SET_NULL, null=True, blank=True)
    date_paid = models.DateField()
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.subscriber.name} paid {self.amount_paid} on {self.date_paid}"
    

class SubscriberLedger(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    water_bill = models.ForeignKey(WaterBill, on_delete=models.SET_NULL, null=True, blank=True)
    date_paid = models.DateField()
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.subscriber.name} paid {self.amount_paid} on {self.date_paid}"
