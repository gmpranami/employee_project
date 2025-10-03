Employee Management System (Django + DRF)
A modular Django project for managing Employees, Departments, Attendance, and Performance.
Includes JWT authentication, Swagger docs, PostgreSQL, and optional seeding for demo data.

🔧 Tech Stack
Backend: Django, Django REST Framework, django-filter
Auth: SimpleJWT (JWT-based authentication)
Docs: drf-yasg (Swagger UI)
DB: PostgreSQL (via django-environ)
Seeding: Faker (sample employees, attendance, performance)
Server: Gunicorn + WhiteNoise (for static files)
✅ Prerequisites
Python 3.10+
PostgreSQL 13+
pip (and optionally virtualenv)
(Windows) PowerShell recommended
🚀 Local Development
1. Setup Environment
# Clone the repo
git clone https://github.com/gmpranami/employee_project.git
cd employee_project

# Create env file
cp .env.example .env
Edit .env and set your values:

DEBUG=True
SECRET_KEY=change-me
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgresql://user:password@localhost:5432/employee_db
2. Install & Migrate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
3. Create Superuser
python manage.py createsuperuser
4. Seed Data (optional)
python manage.py seed_data --employees 50 --days 90
5. Run Server
python manage.py runserver
Health check: http://127.0.0.1:8000/health/ → {"status":"ok"}
Swagger UI: http://127.0.0.1:8000/swagger/
Admin panel: http://127.0.0.1:8000/admin/
🔐 Authentication (JWT)
1. Get Token
POST /api/auth/token/
{
  "username": "<your_user>",
  "password": "<your_pass>"
}
Response:

{"refresh": "<refresh>", "access": "<access>"}
2. Use Token
Add header to all requests:

Authorization: Bearer <access>
3. Refresh Token
POST /api/auth/token/refresh/
{"refresh": "<refresh>"}
🧭 API Overview
Base path: /api/v1/

Resource	Endpoints
Employees	GET,POST /employees/; GET,PATCH,DELETE /employees/{id}/
Departments	GET,POST /departments/; GET,PATCH,DELETE /departments/{id}/
Attendance	GET,POST /attendance/; GET,PATCH,DELETE /attendance/{id}/
Performance	GET,POST /performance/; GET,PATCH,DELETE /performance/{id}/
Health	GET /health
Supports: filtering, searching, ordering, pagination.

🌐 Deployment (Render)
This project is configured for Render using render.yaml.

1. Deploy
Connect GitHub repo to Render

Select Blueprint → branch main

Render provisions:

Web service (Django + Gunicorn)
PostgreSQL database (employee-db)
2. Auto Environment Vars (from render.yaml)
DATABASE_URL → auto from employee-db
SECRET_KEY → auto generated
ALLOWED_HOSTS → .onrender.com,localhost,127.0.0.1
3. Live Links (after deploy)
Health: https://employee-project-pza8.onrender.com/health/
Swagger: https://employee-project-pza8.onrender.com/swagger/
Admin: https://employee-project-pza8.onrender.com/admin/
4. Create Superuser on Render
From Render Dashboard → employee-project → Shell:

python manage.py createsuperuser
Then login at /admin/.

📚 Swagger Docs
Local: http://127.0.0.1:8000/swagger/
Render: https://employee-project-pza8.onrender.com/swagger/
🧰 Common Issues
Error	Fix
DisallowedHost	Add .onrender.com to ALLOWED_HOSTS
gunicorn: command not found	Ensure gunicorn in requirements.txt
psycopg2 not found	Ensure psycopg2-binary in requirements.txt
Static files not loading	Add whitenoise.middleware.WhiteNoiseMiddleware to MIDDLEWARE
401 Unauthorized	Use JWT token in Authorization header
📊 Bonus (Charts)
Employees per Department
Monthly Attendance
Endpoints:

/analytics/charts/ (HTML charts)
/analytics/charts/data/employees-per-department/
/analytics/charts/data/monthly-attendance/
License
MIT License.

About
Django REST API for Employee Management with JWT auth, CRUD, Swagger docs, and visualizations.

Resources
 Readme
 Activity
Stars
 0 stars
Watchers
 0 watching
Forks
 0 forks
Releases
No releases published
Create a new release
Packages
No packages published
Publish your first package
Languages
Python
93.8%
 
HTML
5.3%
 
Dockerfile
0.9%
Footer
© 2025 GitHub, Inc.