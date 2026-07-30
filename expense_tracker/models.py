from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=50,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "name",
                ],
                name="unique_category_per_user",
            ),
        ]

    def __str__(self):
        return self.name


class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ("Income", "Income"),
        ("Expense", "Expense"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    transaction_date = models.DateField()

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title