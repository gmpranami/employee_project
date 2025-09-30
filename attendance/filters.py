import django_filters as df
from .models import Attendance

class AttendanceFilter(df.FilterSet):
    min_date = df.DateFilter(field_name="date", lookup_expr="gte")
    max_date = df.DateFilter(field_name="date", lookup_expr="lte")
    class Meta:
        model = Attendance
        fields = ["employee","status","min_date","max_date"]
