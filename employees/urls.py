"""
Defines API routes for Employees and Performance endpoints.
"""

from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PerformanceViewSet

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"performance", PerformanceViewSet, basename="performance")

urlpatterns = router.urls
