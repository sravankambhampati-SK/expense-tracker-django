from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.http import JsonResponse

from .forms import ExpenseForm, RegisterForm
from .models import Expense


@never_cache
def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Automatically log in the newly registered user.
            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully."
            )

            return redirect("home")
    else:
        form = RegisterForm()

    return render(
        request,
        "expenses/registration/login.html",
        {
            "form": form,
            "now": timezone.now(),
        }
    )


@never_cache
@login_required(login_url="login")
def home(request):
    selected_categories = request.GET.getlist("category")
    selected_date = request.GET.get("date", "").strip()
    selected_year = request.GET.get("year", "").strip()
    min_amount = request.GET.get("min_amount", "").strip()
    max_amount = request.GET.get("max_amount", "").strip()

    # Show only expenses belonging to the logged-in user.
    expenses_qs = Expense.objects.filter(
        user=request.user
    ).order_by("-date")

    if selected_categories:
        expenses_qs = expenses_qs.filter(
            category__in=selected_categories
        )

    if selected_date:
        expenses_qs = expenses_qs.filter(
            date=selected_date
        )

    if selected_year:
        expenses_qs = expenses_qs.filter(
            date__year=selected_year
        )
    if min_amount:
        expenses_qs = expenses_qs.filter(
            amount__gte=min_amount
    )

    if max_amount:
       expenses_qs = expenses_qs.filter(
            amount__lte=max_amount
    )    

    # Total after all filters but before pagination.
    total_amount = expenses_qs.aggregate(
        total=Sum("amount")
    )["total"] or 0

    # Only categories belonging to this logged-in user.
    used_category_values = (
        Expense.objects
        .filter(user=request.user)
        .exclude(category__isnull=True)
        .exclude(category="")
        .values_list("category", flat=True)
        .distinct()
    )

    categories = [
        (value, label)
        for value, label in Expense.CATEGORY_CHOICES
        if value in used_category_values
    ]

    # Only years from this user's expenses.
    years = [
        date.year
        for date in Expense.objects.filter(
            user=request.user
        ).dates("date", "year", order="DESC")
    ]

    # Preserve filters during pagination.
    filter_params = request.GET.copy()
    filter_params.pop("page", None)
    filter_query = filter_params.urlencode()

    paginator = Paginator(expenses_qs, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "expenses/home.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "years": years,
            "selected_categories": selected_categories,
            "selected_date": selected_date,
            "selected_year": selected_year,
            "min_amount": min_amount,
            "max_amount": max_amount,
            "total_amount": total_amount,
            "filter_query": filter_query,
            "now": timezone.now(),
        }
    )


@never_cache
@login_required(login_url="login")
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)

            # Never let the browser decide expense ownership.
            expense.user = request.user
            expense.save()

            messages.success(
                request,
                "Expense added successfully."
            )

            return redirect("home")
    else:
        form = ExpenseForm()

    return render(
        request,
        "expenses/add_expense.html",
        {
            "form": form,
            "now": timezone.now(),
        }
    )


@never_cache
@login_required(login_url="login")
def edit_expense(request, pk):
    # A user can edit only their own expense.
    expense = get_object_or_404(
        Expense,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Expense updated successfully."
            )

            return redirect("home")
    else:
        form = ExpenseForm(instance=expense)

    return render(
        request,
        "expenses/edit_expense.html",
        {
            "form": form,
            "expense": expense,
            "now": timezone.now(),
        }
    )


@never_cache
@login_required(login_url="login")
def delete_expense(request, pk):
    # A user can delete only their own expense.
    expense = get_object_or_404(
        Expense,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        expense.delete()

        messages.success(
            request,
            "Expense deleted successfully."
        )

        return redirect("home")

    return render(
        request,
        "expenses/confirm_delete.html",
        {
            "expense": expense,
            "now": timezone.now(),
        }
    )


@never_cache
def logout_view(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


@login_required(login_url="login")
@never_cache
def extend_session(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405,
        )

    # Extend the authenticated session for another 10 minutes.
    request.session.set_expiry(600)
    request.session.modified = True

    return JsonResponse(
        {
            "message": "Session extended successfully.",
            "expires_in_seconds": 600,
        }
    )