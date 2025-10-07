"""
Serializers convert model instances to JSON for API responses,
and validate JSON input before saving to the database.

Department serialization is imported from the departments app.
"""

from rest_framework import serializers
from .models import Employee, Performance

class EmployeeSerializer(serializers.ModelSerializer):
    """Basic serializer without nested department to test API stability."""

    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "address",
            "date_of_joining",
            "department_id",  # Only show ID
        ]


class PerformanceSerializer(serializers.ModelSerializer):
    """Performance serializer (unchanged)."""
    class Meta:
        model = Performance
        fields = ["id", "employee", "rating", "review_date"]
