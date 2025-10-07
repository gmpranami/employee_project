"""
ViewSets for Employees and Performance.
Provides CRUD APIs with filtering, search, and ordering.
JWT authentication required for all endpoints.
"""

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee, Performance
from .serializers import EmployeeSerializer, PerformanceSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    """Test view without authentication to isolate 500 error."""
    queryset = Employee.objects.select_related("department").all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "department": ["exact"],
        "date_of_joining": ["gte", "lte"],
    }
    search_fields = ["name", "email", "phone_number", "address", "department__name"]
    ordering_fields = ["name", "date_of_joining", "department__name"]


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("employee").all()
    serializer_class = PerformanceSerializer
