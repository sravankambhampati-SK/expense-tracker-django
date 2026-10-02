from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Expense management
    path("add_expense/", views.add_expense, name="add_expense"),
    path("edit_expense/<int:pk>/", views.edit_expense, name="edit_expense"),
    path("delete_expense/<int:pk>/", views.delete_expense, name="delete_expense"),

    # Authentication
    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="D:/Projects/ExpenseTracker/expenses/templates/expenses/registration/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    
    path(
    "extend-session/",
    views.extend_session,
    name="extend_session",
),
]