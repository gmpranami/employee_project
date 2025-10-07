# analytics/views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta

from employees.models import Employee
from attendance.models import Attendance

def charts_page(request):
    # if your template is at templates/charts.html:
    return render(request, "charts.html")

def employees_per_department(request):
    rows = (Employee.objects
            .values("department__name")
            .annotate(total=Count("id"))
            .order_by("department__name"))
    labels = [r["department__name"] or "Unassigned" for r in rows]
    values = [r["total"] for r in rows]
    return JsonResponse({"labels": labels, "values": values})

def monthly_attendance(request):
    today = timezone.now().date()
    start = (today.replace(day=1) - timedelta(days=180)).replace(day=1)
    present_value = getattr(Attendance, "STATUS_PRESENT", "present")
    qs = (Attendance.objects
          .filter(date__gte=start)
          .annotate(month=TruncMonth("date"))
          .values("month")
          .annotate(present=Count("id", filter=Q(status=present_value)))
          .order_by("month"))
    labels = [row["month"].strftime("%Y-%m") for row in qs]
    values = [row["present"] for row in qs]
    return JsonResponse({"labels": labels, "values": values})
