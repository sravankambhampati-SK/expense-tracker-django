from django.db import models

class Expense(models.Model):
    title=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    category=models.CharField(max_length=100)
    date=models.DateField()
    description=models.TextField(blank=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
