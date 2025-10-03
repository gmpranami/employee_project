"""
Custom Django management command to seed the database with:
- Departments
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
from employees.models import Department, Employee, Performance
from attendance.models import Attendance

fake = Faker()

def daterange(start: date, end: date):
    """Helper generator: yields each date between start and end inclusive."""
    for n in range(int((end - start).days) + 1):
        yield start + timedelta(n)

class Command(BaseCommand):
    help = "Seed departments, employees, attendance, and performance data."

    def add_arguments(self, parser):
        parser.add_argument("--employees", type=int, default=50, help="Number of employees to create")
        parser.add_argument("--days", type=int, default=90, help="Number of days of attendance data")

    def handle(self, *args, **opts):
        n_emp = opts["employees"]
        days = opts["days"]

        # Create departments
        dept_names = ["Engineering", "Research", "HR", "Finance", "Marketing", "Sales", "Support"]
        depts = []
        for name in dept_names:
            d, _ = Department.objects.get_or_create(name=name)
            depts.append(d)

        # Create employees
        employees = []
        for _ in range(n_emp):
            dept = random.choice(depts)
            e = Employee.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone_number=fake.msisdn()[:10],
                address=fake.address(),
                date_of_joining=timezone.now().date() - timedelta(days=random.randint(0, 365)),
                department=dept,
            )
            employees.append(e)

        # Generate attendance & performance data
        start = timezone.now().date() - timedelta(days=days)
        end = timezone.now().date()

        att_count, perf_count = 0, 0
        for e in employees:
            # Attendance for weekdays
            for dt in daterange(start, end):
                if dt.weekday() >= 5:  # Skip weekends
                    continue
                status = random.choices(
                    [Attendance.STATUS_PRESENT, Attendance.STATUS_ABSENT, Attendance.STATUS_LATE],
                    weights=[0.85, 0.07, 0.08], k=1
                )[0]
                Attendance.objects.get_or_create(employee=e, date=dt, defaults={"status": status})
                att_count += 1

            # A few performance reviews per employee
            for _ in range(random.randint(2, 5)):
                Performance.objects.create(
                    employee=e,
                    rating=random.randint(1, 5),
                    review_date=start + timedelta(days=random.randint(0, days)),
                )
                perf_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(employees)} employees, {att_count} attendance rows, {perf_count} performance rows."
        ))
