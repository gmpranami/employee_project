from rest_framework.permissions import BasePermission, SAFE_METHODS

def in_group(user, name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name=name).exists()

class RBACPermission(BasePermission):
    """
    Superuser/Admin: full access
    HR: read + create/update; NO DELETE
    Employee: read-only; and ONLY their own Employee/Attendance/Performance
    """
    def has_permission(self, request, view):
        u = request.user
        if not u or not u.is_authenticated:
            return False

        if u.is_superuser or in_group(u, "Admin"):
            return True

        if in_group(u, "HR"):
            return request.method != "DELETE"

        # Employees/others: SAFE methods only
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        u = request.user

        if u.is_superuser or in_group(u, "Admin"):
            return True

        if in_group(u, "HR"):
            return request.method != "DELETE"

        # Employees: SAFE only + own objects
        if request.method not in SAFE_METHODS:
            return False

        emp = getattr(u, "employee_profile", None)
        if emp is None:
            return False

        # If it's an Employee object, must match self
        try:
            from employees.models import Employee
            if isinstance(obj, Employee):
                return obj.pk == emp.pk
        except Exception:
            pass

        # Objects with FK 'employee'
        owner_id = getattr(obj, "employee_id", None)
        return owner_id == getattr(emp, "pk", None)
