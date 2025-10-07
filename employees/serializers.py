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
    """
    Serialize Employee data.
    Includes nested Department info (read-only)
    and a department_id field for write operations.
    """

    # Nested department info (read-only)
    department = DepartmentSerializer(read_only=True)

    # Accept department_id when creating/updating employees
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source="department",          # Map to ForeignKey field
        write_only=True,
        help_text="Select department by ID when creating or updating an employee."
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
    """
    Serialize Performance records, showing employee names for clarity.
    """

    employee_name = serializers.CharField(source="employee.name", read_only=True)

    class Meta:
        model = Performance
        fields = ["id", "employee", "employee_name", "rating", "review_date"]
