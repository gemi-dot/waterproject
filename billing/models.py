from django.db import models

# Create your models here.
from django.db import models

class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class WaterBill(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    billing_month = models.CharField(max_length=20)  # e.g. "May 2025"
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.subscriber.name} - {self.billing_month}"

class LedgerEntry(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.subscriber.name} - {self.description}"
