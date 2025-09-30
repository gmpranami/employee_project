import django_filters as df
from .models import Employee, Performance

class EmployeeFilter(df.FilterSet):
    min_doj = df.DateFilter(field_name="date_of_joining", lookup_expr="gte")
    max_doj = df.DateFilter(field_name="date_of_joining", lookup_expr="lte")
    class Meta:
        model = Employee
        fields = ["department","min_doj","max_doj"]

class PerformanceFilter(df.FilterSet):
    min_date = df.DateFilter(field_name="review_date", lookup_expr="gte")
    max_date = df.DateFilter(field_name="review_date", lookup_expr="lte")
    min_rating = df.NumberFilter(field_name="rating", lookup_expr="gte")
    max_rating = df.NumberFilter(field_name="rating", lookup_expr="lte")
    class Meta:
        model = Performance
        fields = ["employee","min_date","max_date","min_rating","max_rating"]
