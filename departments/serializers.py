"""
Serializer for the Department model.
Used to convert Department objects to/from JSON.
"""

from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    """Serialize and validate Department data for the API."""
    
    class Meta:
        model = Department
        fields = ["id", "name", "description"]
