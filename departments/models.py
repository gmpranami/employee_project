"""
Model for Department entities.
Each department represents a functional unit within the organization.
"""

from django.db import models

class Department(models.Model):
    """
    Stores department information such as name and description.
    Example: Human Resources, Finance, IT, Marketing, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, help_text="Optional short description of the department.")

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        """Readable representation of the department name."""
        return self.name
