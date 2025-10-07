from django.contrib import admin
from .models import Employee, Performance

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "department", "date_of_joining")
    list_filter = ("department", "date_of_joining")
    search_fields = ("name", "email")

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "rating", "review_date")
    list_filter = ("rating", "review_date", "employee__department")
    search_fields = ("employee__name", "employee__email")
