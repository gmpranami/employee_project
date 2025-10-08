"""
URL configuration for the Employee Management System.

Includes:
- Admin panel
- Core API routes (Employees, Departments, Attendance, Performance)
- JWT authentication (login & refresh)
- Swagger documentation
- Analytics app (charts/visuals)
- Health check endpoint
- Root redirect → /swagger/ for easy navigation
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static


# --------------------------------------------------------------------
# SWAGGER SCHEMA VIEW CONFIGURATION
# --------------------------------------------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Employee Management API",            # Project title
        default_version="v1",
        description=(
            "Comprehensive API documentation for managing Employees, "
            "Departments, Attendance, Performance, and Analytics."
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# --------------------------------------------------------------------
# HEALTH CHECK ENDPOINT
# --------------------------------------------------------------------
def health(_):
    """Simple JSON health check endpoint for uptime monitoring."""
    return JsonResponse({"status": "ok"})


# --------------------------------------------------------------------
# ROOT REDIRECT
# --------------------------------------------------------------------
def root_redirect(request):
    """Redirect root URL (/) to Swagger documentation."""
    return redirect("/swagger/", permanent=False)


# --------------------------------------------------------------------
# MAIN URL PATTERNS
# --------------------------------------------------------------------
urlpatterns = [
    # Django admin site
    path("admin/", admin.site.urls),

    # --- Core API routes ---
    path("api/v1/", include("employees.urls")),       # Employees & Performance
    path("api/v1/", include("attendance.urls")),      # Attendance records
    path("api/v1/", include("departments.urls")),     # Departments 

    # --- JWT Authentication (Token generation and refresh) ---
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # --- Swagger API Documentation ---
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

    # --- Analytics routes (bonus feature) ---
     path("api/v1/analytics/", include("analytics.urls")),

    # --- Health check (useful for Render deployment monitoring) ---
    path("health/", health),

    path("api-auth/", include("rest_framework.urls")),  # adds login/logout

    # --- Redirect root (/) to Swagger UI ---
    path("", root_redirect),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)