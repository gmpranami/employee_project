from rest_framework import serializers
from .models import Attendance
from employees.models import Performance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = "__all__"
