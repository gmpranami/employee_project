"""
Attendance model for tracking daily employee presence.

Each record represents an employee’s attendance status on a specific date.
Status values can be "Present", "Absent", or "Late".

Used for generating reports, analytics, and HR summaries.
"""

from django.db import models
from employees.models import Employee


class Attendance(models.Model):
    """
    Stores attendance status for employees on specific dates.

    Ensures:
    - One record per employee per date
    - Fast lookups using indexes
    - Clean relationship with Employee model
    """

    # -------------------------------
    # Attendance status options
    # -------------------------------
    STATUS_PRESENT = "Present"
    STATUS_ABSENT = "Absent"
    STATUS_LATE = "Late"

    STATUS_CHOICES = (
        (STATUS_PRESENT, "Present"),
        (STATUS_ABSENT, "Absent"),
        (STATUS_LATE, "Late"),
    )

    # -------------------------------
    # Model fields
    # -------------------------------
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance",
        help_text="Employee associated with this attendance record."
    )

    date = models.DateField(
        help_text="Date of the attendance record."
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        help_text="Attendance status (Present, Absent, or Late)."
    )

    # -------------------------------
    # Meta options for indexing & constraints
    # -------------------------------
    class Meta:
        unique_together = ("employee", "date")  # Prevent duplicate records per day
        ordering = ["-date"]  # Show most recent attendance first
        indexes = [
            models.Index(fields=["employee", "date"]),  # Optimize filtering
        ]
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"

    # -------------------------------
    # String representation
    # -------------------------------
    def __str__(self):
        """Readable representation shown in admin and logs."""
        return f"{self.employee.name} - {self.date} - {self.status}"
