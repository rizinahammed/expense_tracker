from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    """
    Model for transaction categories, scoped to each user.
    """
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'user')  # Ensure unique category names per user

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Model for income and expense transactions.
    """
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.type.capitalize()}: {self.amount} - {self.category.name}"
