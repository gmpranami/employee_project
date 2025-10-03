"""
Serializers for Attendance and Performance models.
"""

from rest_framework import serializers
from .models import Attendance
from employees.models import Performance

class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance records."""
    class Meta:
        model = Attendance
        fields = "__all__"


class PerformanceSerializer(serializers.ModelSerializer):
    """Serializer for Performance reviews."""
    class Meta:
        model = Performance
        fields = "__all__"
