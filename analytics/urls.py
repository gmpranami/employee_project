# analytics/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("charts/", views.charts_page, name="charts"),
    path("employees-per-department/", views.employees_per_department, name="employees-per-department"),
    path("monthly-attendance/", views.monthly_attendance, name="monthly-attendance"),
]
