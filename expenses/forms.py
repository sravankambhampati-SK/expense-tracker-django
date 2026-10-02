from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense

        fields = [
            "title",
            "amount",
            "category",
            "date",
            "description",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter expense title",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Add an optional description",
                }
            ),
        }


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="First name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your first name",
            }
        )
    )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        label="Last name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your last name",
            }
        )
    )

    email = forms.EmailField(
        required=True,
        label="Email address",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "name@example.com",
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Choose a username",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account already exists with this email address."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user