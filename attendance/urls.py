from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, PerformanceViewSet

router = DefaultRouter()
router.register(r"attendance", AttendanceViewSet, basename="attendance")
router.register(r"performance", PerformanceViewSet, basename="performance")

urlpatterns = [
    path("", include(router.urls)),
]
