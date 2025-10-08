from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta, date
from django.db import transaction

from departments.models import Department
from employees.models import Employee, Performance
from attendance.models import Attendance

fake = Faker()


def daterange(start: date, end: date):
    """Yield all days between start and end inclusive."""
    for n in range((end - start).days + 1):
        yield start + timedelta(n)


class Command(BaseCommand):
    help = "Seed departments, employees, attendance, and performance data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--employees",
            type=int,
            default=50,
            help="Number of employees to create (default=50)",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Days of attendance data (default=90)",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        n_emp = opts["employees"]
        days = opts["days"]

        # ✅ Always define this first
        dept_names = [
            "Engineering", "Research", "HR",
            "Finance", "Marketing", "Sales", "Support"
        ]

        # ✅ Stop here if already seeded
        if Employee.objects.exists():
            self.stdout.write(self.style.WARNING("⚠️  Employees already exist — skipping seeding."))
            return

        self.stdout.write(self.style.SUCCESS("🚀 Seeding database..."))

        # Step 1: Departments
        depts = []
        for name in dept_names:
            dept, _ = Department.objects.get_or_create(name=name)
            depts.append(dept)
        self.stdout.write(self.style.SUCCESS(f"✅ Departments ready: {len(depts)}"))

        # Step 2: Employees
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

        # Step 3: Attendance + Performance
        start_date = timezone.now().date() - timedelta(days=days)
        end_date = timezone.now().date()
        att_count = 0
        perf_count = 0

        for emp in employees:
            for dt in daterange(start_date, end_date):
                if dt.weekday() >= 5:
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

            for _ in range(random.randint(2, 5)):
                Performance.objects.create(
                    employee=emp,
                    rating=random.randint(1, 5),
                    review_date=start_date + timedelta(days=random.randint(0, days)),
                )
                perf_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"🎉 Done! {len(employees)} employees, {att_count} attendances, "
                f"{perf_count} performance reviews."
            )
        )
