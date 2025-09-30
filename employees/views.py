from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related("department").all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "department": ["exact"],
        "date_of_joining": ["gte", "lte"],
    }
    search_fields = ["name", "email", "phone_number", "address", "department__name"]
    ordering_fields = ["name", "date_of_joining", "department__name"]
