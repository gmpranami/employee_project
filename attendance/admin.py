from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "date", "status")
    list_filter = ("status", "date", "employee__department")
    search_fields = ("employee__name", "employee__email")
