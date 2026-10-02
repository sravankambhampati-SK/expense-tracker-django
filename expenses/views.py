from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .forms import ExpenseForm
from .models import Expense


def home(request):
    expenses_qs = Expense.objects.all().order_by('-date')

    paginator = Paginator(expenses_qs, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "expenses/home.html",
        {"page_obj": page_obj, "now": timezone.now()}
    )


def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ExpenseForm()

    return render(
        request,
        "expenses/add_expense.html",
        {"form": form, "now": timezone.now()}
    )


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ExpenseForm(instance=expense)

    return render(
        request,
        "expenses/edit_expense.html",
        {"form": form, "expense": expense, "now": timezone.now()}
    )


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == "POST":
        expense.delete()
        return redirect("home")

    return render(
        request,
        "expenses/confirm_delete.html",
        {"expense": expense, "now": timezone.now()}
    )