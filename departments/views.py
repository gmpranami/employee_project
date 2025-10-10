"""
API viewset for managing departments.
Provides full CRUD functionality.
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Department
from .serializers import DepartmentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Department CRUD API.
    Features:
    - List all departments
    - Create new departments
    - Retrieve single department
    - Update or delete existing departments
    """
    class DepartmentViewSet(viewsets.ModelViewSet):
        queryset = Department.objects.all().order_by("name")
        serializer_class = DepartmentSerializer
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
        search_fields = ["name", "description"]
        ordering_fields = ["name"]
