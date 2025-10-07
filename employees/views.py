"""
ViewSets for Employees and Performance.
Provides CRUD APIs with filtering, search, and ordering.
JWT authentication required for all endpoints.
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee, Performance
from .serializers import EmployeeSerializer, PerformanceSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """CRUD API for employees with advanced filtering and search."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "department": ["exact"],
        "date_of_joining": ["gte", "lte"],
    }
    search_fields = ["name", "email", "phone_number", "address", "department__name"]
    ordering_fields = ["name", "date_of_joining", "department__name"]


class PerformanceViewSet(viewsets.ModelViewSet):
    """CRUD API for performance reviews."""
    queryset = Performance.objects.select_related("employee").all()
    serializer_class = PerformanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {"employee": ["exact"], "rating": ["gte", "lte"]}
    search_fields = ["employee__name", "employee__email"]
    ordering_fields = ["rating", "review_date"]
