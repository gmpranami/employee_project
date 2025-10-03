"""
Models for Employees and Departments.
Also defines Performance reviews linked to employees.
"""

from django.db import models

class Department(models.Model):
    """Represents a department in the organization."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Represents an employee record."""
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    date_of_joining = models.DateField()
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, related_name="employees"
    )

    class Meta:
        indexes = [
            models.Index(fields=["department", "date_of_joining"]),
            models.Index(fields=["email"]),
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.email})"


class Performance(models.Model):
    """Represents a performance review for an employee."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="performances")
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_date = models.DateField()

    class Meta:
        ordering = ["-review_date"]
        indexes = [
            models.Index(fields=["employee", "review_date"]),
            models.Index(fields=["rating"]),
        ]

    def __str__(self):
        return f"{self.employee.name} • {self.rating} on {self.review_date}"
