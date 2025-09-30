from django.urls import path
from . import views

urlpatterns = [
    path("charts/", views.charts_page, name="charts_page"),
    path("charts/data/employees-per-department/", views.employees_per_department, name="emp_per_dept"),
    path("charts/data/monthly-attendance/", views.monthly_attendance, name="monthly_attendance"),
]
