"""
ViewSets for Attendance and Performance APIs.
Supports filtering, search, and ordering.
JWT authentication required.
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Attendance
from .serializers import AttendanceSerializer, PerformanceSerializer
from employees.models import Performance
from rest_framework_simplejwt.authentication import JWTAuthentication

class AttendanceViewSet(viewsets.ModelViewSet):
   
    """CRUD API for employee attendance records."""
    queryset = Attendance.objects.select_related("employee", "employee__department").all()
    serializer_class = AttendanceSerializer
    authentication_classes = [JWTAuthentication]
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
    """CRUD API for employee performance reviews."""
    queryset = Performance.objects.select_related("employee", "employee__department").all()
    serializer_class = PerformanceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        "employee": ["exact"],
        "rating": ["exact", "gte", "lte"],
        "review_date": ["gte", "lte", "exact"],
    }
    ordering_fields = ["review_date", "rating", "employee"]
    search_fields = ["employee__name", "employee__email", "employee__department__name"]
