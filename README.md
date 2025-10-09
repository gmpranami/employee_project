Employee Management System (Django + DRF)

A complete Employee Management System built using Django and Django REST Framework (DRF).
It allows you to manage Employees, Departments, Attendance, and Performance through both an interactive Swagger API and the Django Admin Panel.

This system includes:

JWT Authentication (using SimpleJWT)

Swagger API Documentation

PostgreSQL Database Integration

Automatic Data Seeding with Faker

Production Deployment on Render

Optional Analytics with Charts


Overview

This project is designed as a backend API for a corporate HR system.
It enables HR managers or admins to:

➕ Add, update, or delete employees and departments

🕒 Record and view attendance and performance data

⚙️ Manage all data through a centralized admin panel

🔐 Use JWT-based authentication for secure API access

📘 View and test APIs through Swagger

App Structure:

employees/ → Handles employee and performance data

departments/ → Manages department records

attendance/ → Tracks attendance

analytics/ → Optional extension for analytics and charts

⚙️ Tech Stack

Component	Technology

Framework	Django 5 + Django REST Framework

Authentication	SimpleJWT (JWT Tokens)

Documentation	drf-yasg (Swagger UI)

Database	PostgreSQL (via django-environ)

Demo Data	Faker

Server (Prod)	Gunicorn + WhiteNoise

Hosting	Render Cloud Platform


Features

✅ CRUD operations for Employees, Departments, Attendance, and Performance

✅ JWT authentication for secure API access

✅ Swagger-based API documentation

✅ Search, filter, and pagination support

✅ Health check endpoint for Render uptime

✅ Automatic demo data seeding (optional)

✅ Deployable with PostgreSQL on Render

✅ Bonus analytics (charts + data APIs)


🧠 How It Works

The backend provides RESTful APIs for managing employee-related data.

Each app (employees, departments, attendance) exposes its routes under /api/v1/.

Authentication is handled via JWT tokens (/api/auth/token/ & /api/auth/token/refresh/).

Swagger UI (/swagger/) allows users to view and test APIs interactively.

Admin users can log in through /admin/ for visual management.

Analytics module provides visual summaries of employees and attendance trends.

🧭 Live Demo (Render Deployment)

Feature	URL

🩺 Health Check	https://employee-project-pza8.onrender.com/health/

📘 Swagger Docs	https://employee-project-pza8.onrender.com/swagger/

⚙️ Admin Panel	https://employee-project-pza8.onrender.com/admin/

🔑 Log in to /admin/ using your superuser credentials after creating one via Render Shell.

Charts (HTML View) https://employee-project-pza8.onrender.com/api/v1/analytics/charts/


🧰 Local Setup Guide

1️⃣ Clone the Repository

git clone https://github.com/gmpranami/employee_project.git

cd employee_project

2️⃣ Create Environment File

cp .env.example .env

Edit .env:

DEBUG=True

SECRET_KEY=change-me

ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=postgresql://<username>:<password>@localhost:5432/employee_db


3️⃣ Install Dependencies

pip install -r requirements.txt


4️⃣ Apply Migrations

python manage.py makemigrations

python manage.py migrate


5️⃣ Create Superuser

python manage.py createsuperuser


6️⃣ Seed Demo Data

python manage.py seed_data --employees 50 --days 60


7️⃣ Run Server

python manage.py runserver

Your app will be live at → http://127.0.0.1:8000/

🔐 Authentication (JWT)

1️⃣ Get Access Token

POST /api/auth/token/

{

"username": "<your_username>",

"password": "<your_password>"

}


Response:

{
  
  "refresh": "<refresh_token>",
  
  "access": "<access_token>"

}


Header:

Authorization: Bearer <access_token>

2️⃣ Refresh Token

POST /api/auth/token/refresh/

{
  "refresh": "<refresh_token>"
}

📚 API Overview

Base path: /api/v1/

Resource	Local Endpoint	Render Endpoint	Methods	Description

👥 Employees	http://127.0.0.1:8000/api/v1/employees/
	
	https://employee-project-pza8.onrender.com/api/v1/employees/
	
	GET, POST	Manage employees

🧾 Employee Detail	/employees/{id}/	/employees/{id}/	GET, PATCH, DELETE	Retrieve or modify specific employee

🏢 Departments	http://127.0.0.1:8000/api/v1/departments/
	
	https://employee-project-pza8.onrender.com/api/v1/departments/
	
	GET, POST	Manage departments

🕒 Attendance	http://127.0.0.1:8000/api/v1/attendance/

	https://employee-project-pza8.onrender.com/api/v1/attendance/
	
	GET, POST	Track attendance

⭐ Performance	http://127.0.0.1:8000/api/v1/performance/

	https://employee-project-pza8.onrender.com/api/v1/performance/
	
	GET, POST	Manage performance reviews

📈 Charts (HTML)

http://127.0.0.1:8000/api/v1/analytics/charts/

https://employee-project-pza8.onrender.com/api/v1/analytics/charts/

GET

View data charts

🩺 Health Check	http://127.0.0.1:8000/health/

	https://employee-project-pza8.onrender.com/health/
	
	GET	Check server status

⚙️ Admin Panel (CRUD)


Manage all data visually from Django Admin:

➕ Add employees, departments, attendance, and performance

✏️ Edit existing records

❌ Delete records

🔍 View linked relationships (e.g., employees by department)

Environment	URL
Local	http://127.0.0.1:8000/admin/

Render	https://employee-project-pza8.onrender.com/admin/
☁️ Deployment on Render

This project is pre-configured for Render deployment.

🚀 Steps to Deploy

Connect your GitHub repository on Render
.

Create a Web Service → select your repo (employee_project).

Set environment variables:


SECRET_KEY=<your_secret_key>

DATABASE_URL=<render_postgres_db_url>

ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1

DEBUG=False


Render will automatically:

Install dependencies (pip install -r requirements.txt)

Run migrations (python manage.py migrate)

Serve using Gunicorn + WhiteNoise

Once deployed, open your app at:

https://employee-project-xxxx.onrender.com/


To create an admin user (on Render Shell):

python manage.py createsuperuser

🧩 Example Use Case

👩‍💼 HR Admin logs into /admin/

🏢 Adds new departments

👥 Adds employees to those departments

🕒 Marks attendance and performance data

🔐 Generates JWT tokens for secure API access

📊 Views charts via /api/v1/analytics/charts/

📘 Views data and tests endpoints via /swagger/

👩‍💻 Author

Medha
GitHub: @gmpranami

