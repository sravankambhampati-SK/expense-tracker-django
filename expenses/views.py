from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import ExpenseForm
from .models import Expense


def home(request):
    # Get all expenses ordered by date
    expenses_qs = Expense.objects.all().order_by('-date')

    # Pagination: 8 per page
    paginator = Paginator(expenses_qs, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "expenses/home.html", {"page_obj": page_obj})


def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ExpenseForm()

    return render(request, "expenses/add_expense.html", {"form": form})