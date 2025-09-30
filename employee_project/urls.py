from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.views import EmployeeViewSet, DepartmentViewSet
from attendance.views import AttendanceViewSet, PerformanceViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import JsonResponse

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet)
router.register(r"departments", DepartmentViewSet)
router.register(r"attendance", AttendanceViewSet)
router.register(r"performance", PerformanceViewSet)

schema_view = get_schema_view(
    openapi.Info(title="Employee API", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def health(_): return JsonResponse({"status": "ok"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("analytics/", include("analytics.urls")),
    path("health/", health),
]
