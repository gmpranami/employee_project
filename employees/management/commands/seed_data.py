"""
Custom Django management command to seed the database with:
- Departments (from departments app)
- Employees
- Attendance records
- Performance reviews

Usage:
    python manage.py seed_data --employees 50 --days 90

This script uses the Faker library to generate realistic data for
testing or demo purposes. It can be safely re-run without creating
duplicate departments.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta, date

# ✅ Updated imports (Department now lives in its own app)
from departments.models import Department
from employees.models import Employee, Performance
from attendance.models import Attendance

fake = Faker()


# ---------------------------------------------------------------------
# Helper function: date generator
# ---------------------------------------------------------------------
def daterange(start: date, end: date):
    """
    Generator that yields every date between start and end (inclusive).
    Used to easily create attendance records for each day.
    """
    for n in range(int((end - start).days) + 1):
        yield start + timedelta(n)


# ---------------------------------------------------------------------
# Command definition
# ---------------------------------------------------------------------
class Command(BaseCommand):
    """
    Seeds the database with departments, employees, attendance,
    and performance records for development or testing environments.

    Arguments:
        --employees : number of employees to create (default=50)
        --days      : number of days of attendance data (default=90)
    """

    help = "Seed departments, employees, attendance, and performance data."

    def add_arguments(self, parser):
        """
        Allow command-line arguments for custom dataset sizes.
        Example:
            python manage.py seed_data --employees 100 --days 180
        """
        parser.add_argument(
            "--employees",
            type=int,
            default=50,
            help="Number of employees to create (default=50)"
        )
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Number of days of attendance data to generate (default=90)"
        )

    def handle(self, *args, **opts):
        """
        Main execution method. Runs automatically when the command is called.
        Creates departments, employees, attendance, and performance data.
        """
        n_emp = opts["employees"]
        days = opts["days"]

        # --------------------------------------------------------------
        # Step 1: Create departments
        # --------------------------------------------------------------
        dept_names = ["Engineering", "Research", "HR", "Finance", "Marketing", "Sales", "Support"]
        depts = []

        for name in dept_names:
            dept, _ = Department.objects.get_or_create(name=name)
            depts.append(dept)

        self.stdout.write("Created or found all departments.")

        # --------------------------------------------------------------
        # Step 2: Create employees
        # --------------------------------------------------------------
        employees = []
        for _ in range(n_emp):
            dept = random.choice(depts)
            emp = Employee.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone_number=fake.msisdn()[:10],
                address=fake.address(),
                date_of_joining=timezone.now().date() - timedelta(days=random.randint(0, 365)),
                department=dept,
            )
            employees.append(emp)

        self.stdout.write(f"Created {len(employees)} employees.")

        # --------------------------------------------------------------
        # Step 3: Create attendance and performance data
        # --------------------------------------------------------------
        start_date = timezone.now().date() - timedelta(days=days)
        end_date = timezone.now().date()

        att_count = 0
        perf_count = 0

        for emp in employees:
            # --- Attendance for weekdays only ---
            for dt in daterange(start_date, end_date):
                if dt.weekday() >= 5:  # Skip weekends (Saturday/Sunday)
                    continue

                status = random.choices(
                    [
                        Attendance.STATUS_PRESENT,
                        Attendance.STATUS_ABSENT,
                        Attendance.STATUS_LATE,
                    ],
                    weights=[0.85, 0.07, 0.08],
                    k=1,
                )[0]

                Attendance.objects.get_or_create(
                    employee=emp,
                    date=dt,
                    defaults={"status": status},
                )
                att_count += 1

            # --- Performance reviews ---
            for _ in range(random.randint(2, 5)):
                Performance.objects.create(
                    employee=emp,
                    rating=random.randint(1, 5),
                    review_date=start_date + timedelta(days=random.randint(0, days)),
                )
                perf_count += 1

        # --------------------------------------------------------------
        # Step 4: Summary output
        # --------------------------------------------------------------
        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete: {len(employees)} employees, "
                f"{att_count} attendance records, and {perf_count} performance reviews created successfully."
            )
        )
