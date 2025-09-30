from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Attendance
from .serializers import AttendanceSerializer, PerformanceSerializer
from employees.models import Performance

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("employee", "employee__department").all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        "employee": ["exact"],
        "status": ["exact"],
        "date": ["gte", "lte", "exact"],
    }
    ordering_fields = ["date", "employee"]
    search_fields = ["employee__name", "employee__email", "employee__department__name"]

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("employee", "employee__department").all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        "employee": ["exact"],
        "rating": ["exact", "gte", "lte"],
        "review_date": ["gte", "lte", "exact"],
    }
    ordering_fields = ["review_date", "rating", "employee"]
    search_fields = ["employee__name", "employee__email", "employee__department__name"]
