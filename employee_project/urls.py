"""
URL configuration for the Employee Management System.
Includes:
- Admin site
- API routes (Employees, Departments, Attendance, Performance)
- JWT authentication endpoints
- Swagger docs
- Analytics (charts)
- Health check
- Root redirect → /swagger/
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import JsonResponse

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(title="Employee API", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Healthcheck endpoint
def health(_):
    return JsonResponse({"status": "ok"})

# Redirect root → Swagger
def root_redirect(request):
    return redirect("/swagger/", permanent=False)

# URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ include app-level urls
    path("api/v1/", include("employees.urls")),
    path("api/v1/", include("attendance.urls")),

    # Auth (JWT)
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger & extras
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("analytics/", include("analytics.urls")),
    path("health/", health),
    path("", root_redirect),
]
