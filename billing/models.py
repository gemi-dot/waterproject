from django.db import models
from decimal import Decimal

class Subscriber(models.Model):
    """Model representing a subscriber."""
    name = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class WaterBill(models.Model):
    """Model representing a water bill for a subscriber."""
    RATE_PER_CUBIC_METER = Decimal('15.00')

    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    billing_month = models.DateField()  # stores first day of the month (e.g., 2025-05-01)
    consumption = models.DecimalField(max_digits=10, decimal_places=2)  # cubic meters consumed
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    def save(self, *args, **kwargs):
        self.amount_due = self.consumption * self.RATE_PER_CUBIC_METER
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subscriber.name} - {self.billing_month.strftime('%B %Y')}"


class LedgerEntry(models.Model):
    """General ledger entry for a subscriber."""
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True, editable=False)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.subscriber.name} - {self.description}"


class SubscriberLedger(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    water_bill = models.ForeignKey(WaterBill, on_delete=models.CASCADE, null=True, blank=True)
    date_paid = models.DateField()
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subscriber} - {self.date_paid} - ₱{self.amount_paid}"
