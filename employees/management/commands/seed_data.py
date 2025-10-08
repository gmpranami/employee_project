"""
Custom Django management command to safely seed the database with:
- Departments (from departments app)
- Employees
- Attendance records
- Performance reviews

Usage:
    python manage.py seed_data --employees 50 --days 90
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta, date
from django.db import transaction

# ✅ Imports
from departments.models import Department
from employees.models import Employee, Performance
from attendance.models import Attendance

fake = Faker()


# ---------------------------------------------------------------------
# Helper: date generator
# ---------------------------------------------------------------------
def daterange(start: date, end: date):
    for n in range(int((end - start).days) + 1):
        yield start + timedelta(n)


# ---------------------------------------------------------------------
# Command definition
# ---------------------------------------------------------------------
class Command(BaseCommand):
    help = "Seed departments, employees, attendance, and performance data safely."

    def add_arguments(self, parser):
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

    @transaction.atomic
    def handle(self, *args, **opts):
        n_emp = opts["employees"]
        days = opts["days"]

        # 🚨 Skip if already seeded
        if Employee.objects.exists():

        # --------------------------------------------------------------
        # Step 1: Create or get departments
        # --------------------------------------------------------------
            dept_names = ["Engineering", "Research", "HR", "Finance", "Marketing", "Sales", "Support"]
            depts = []
        for name in dept_names:
            dept, created = Department.objects.get_or_create(name=name)
            depts.append(dept)
        self.stdout.write(self.style.SUCCESS("✅ Departments ready."))

        # --------------------------------------------------------------
        # Step 2: Clear old data (optional, for safe reseeding)
        # --------------------------------------------------------------
        Attendance.objects.all().delete()
        Performance.objects.all().delete()
        Employee.objects.all().delete()
        self.stdout.write("🧹 Old employee, attendance, and performance data cleared.")

        # --------------------------------------------------------------
        # Step 3: Create employees
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

        self.stdout.write(self.style.SUCCESS(f"👥 Created {len(employees)} employees."))

        # --------------------------------------------------------------
        # Step 4: Create attendance & performance
        # --------------------------------------------------------------
        start_date = timezone.now().date() - timedelta(days=days)
        end_date = timezone.now().date()

        att_count = 0
        perf_count = 0

        for emp in employees:
            # Attendance for weekdays only
            for dt in daterange(start_date, end_date):
                if dt.weekday() >= 5:  # Skip weekends
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
                Attendance.objects.create(employee=emp, date=dt, status=status)
                att_count += 1

            # Performance reviews
            for _ in range(random.randint(2, 5)):
                Performance.objects.create(
                    employee=emp,
                    rating=random.randint(1, 5),
                    review_date=start_date + timedelta(days=random.randint(0, days)),
                )
                perf_count += 1

        # --------------------------------------------------------------
        # Step 5: Summary output
        # --------------------------------------------------------------
        self.stdout.write(
            self.style.SUCCESS(
                f"🎉 Seeding complete:\n"
                f"   • Departments: {len(depts)}\n"
                f"   • Employees: {len(employees)}\n"
                f"   • Attendance records: {att_count}\n"
                f"   • Performance reviews: {perf_count}"
            )
        )
