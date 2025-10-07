"""
Serializers convert model instances to JSON for API responses,
and validate JSON input before saving to the database.

Department serialization is imported from the departments app.
"""

from rest_framework import serializers
from departments.models import Department
from departments.serializers import DepartmentSerializer
from .models import Employee, Performance

class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True, allow_null=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source="department",
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "address",
            "date_of_joining",
            "department",
            "department_id",
        ]


class PerformanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.name", read_only=True)

    class Meta:
        model = Performance
        fields = ["id", "employee", "employee_name", "rating", "review_date"]
