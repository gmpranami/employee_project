"""
Serializers for Department and Employee models.
Convert model instances into JSON and validate input data.
"""

from rest_framework import serializers
from .models import Department, Employee

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model."""
    class Meta:
        model = Department
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model."""
    class Meta:
        model = Employee
        fields = "__all__"
