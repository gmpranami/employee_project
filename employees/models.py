"""
Models for Employees and Performance Reviews.

This module defines:
- Employee: Stores employee details linked to a department.
- Performance: Tracks employee performance reviews and ratings.

Department model has been moved to the departments app.
"""

from django.db import models
from departments.models import Department




class Employee(models.Model):
    """
    Represents an employee record in the company.
    Each employee belongs to one department.
    """

    name = models.CharField(
        max_length=120,
        help_text="Full name of the employee."
    )
    email = models.EmailField(
        unique=True,
        help_text="Employee’s unique email address."
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        help_text="Contact number (optional)."
    )
    address = models.TextField(
        blank=True,
        help_text="Residential address (optional)."
    )
    date_of_joining = models.DateField(
        help_text="The date the employee joined the organization."
    )

    department = models.ForeignKey(
    Department,
    on_delete=models.CASCADE,
    related_name="employees"
)

    class Meta:
        # Database-level optimizations
        indexes = [
            models.Index(fields=["department", "date_of_joining"]),
            models.Index(fields=["email"]),
        ]
        ordering = ["name"]  # Default ordering by name (A–Z)
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        """Display employee name and email."""
        return f"{self.name} ({self.email})"


class Performance(models.Model):
    """
    Represents a performance review for an employee.
    Ratings are integer values from 1 (lowest) to 5 (highest).
    """

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,      # If employee is deleted, remove associated performance
        related_name="performances",
        help_text="Employee being reviewed."
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        help_text="Performance rating from 1 (Poor) to 5 (Excellent)."
    )
    review_date = models.DateField(
        help_text="Date when the performance review was recorded."
    )

    class Meta:
        ordering = ["-review_date"]  # Most recent reviews first
        indexes = [
            models.Index(fields=["employee", "review_date"]),
            models.Index(fields=["rating"]),
        ]
        verbose_name = "Performance Review"
        verbose_name_plural = "Performance Reviews"

    def __str__(self):
        """Display example: 'Alice • 4 on 2025-10-01'."""
        return f"{self.employee.name} • {self.rating} on {self.review_date}"
