from django.conf import settings
from django.db import models


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("food", "Food"),
        ("transport", "Transport"),
        ("shopping", "Shopping"),
        ("bills", "Bills & Utilities"),
        ("entertainment", "Entertainment"),
        ("health", "Health"),
        ("education", "Education"),
        ("games", "Games"),
        ("other", "Other"),
    ]

    # Each expense belongs to exactly one logged-in user.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    title = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    date = models.DateField()

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"