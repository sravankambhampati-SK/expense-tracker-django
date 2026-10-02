from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    # Define category choices (customize as needed)
    CATEGORY_CHOICES = [
        ("", "Select category"),      # optional placeholder
        ("food", "Food"),
        ("transport", "Transport"),
        ("shopping", "Shopping"),
        ("bills", "Bills & Utilities"),
        ("entertainment", "Entertainment"),
        ("health", "Health"),
        ("education", "Education"),
        ("other", "Other"),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'description']
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",   # enables browser calendar
                }
            ),
            "description": forms.Textarea(attrs={"rows": 3}),
        }