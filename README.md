````markdown
# Employee Management System (Django + DRF)

A modular Django project featuring **Employees**, **Departments**, **Attendance**, and **Performance** with:
- PostgreSQL + `.env` configuration (via `django-environ`)
- JWT auth (SimpleJWT)
- DRF CRUD APIs with pagination, filtering, search, and ordering
- Swagger UI (drf-yasg)
- Seed script (30–50+ employees, attendance, performance)
- Bonus: Chart.js views (Employees/Department, Monthly Attendance)

---

## 🔧 Tech Stack

- **Backend:** Django, Django REST Framework, django-filter
- **Auth:** SimpleJWT
- **Docs:** drf-yasg (Swagger)
- **Config:** django-environ (`.env`)
- **DB:** PostgreSQL
- **Seeding:** Faker

---

## ✅ Prerequisites

- Python 3.10+
- PostgreSQL 13+
- pip (and optionally virtualenv)
- (Windows) PowerShell recommended

---

## 🚀 Quick Start

### 1) Clone & Environment
```bash
# Linux/macOS
cp .env.example .env
# edit DATABASE_URL and SECRET_KEY
````

```powershell
# Windows PowerShell
Copy-Item .env.example .env
# edit DATABASE_URL and SECRET_KEY
```

`.env.example`:

```env
DEBUG=True
SECRET_KEY=change-me
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgresql://glynac:glynac@localhost:5432/employee_db
```

### 2) Install & Migrate

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

### 3) Create Admin

```bash
python manage.py createsuperuser
# Username: <your_user>
# Email: <your_email>
# Password: <your_pass>
```

### 4) Seed Data (sample)

```bash
python manage.py seed_data --employees 50 --days 90
# e.g. "Seeded 50 employees, 3200 attendance rows, 151 performance rows."
```

### 5) Run

```bash
python manage.py runserver
# http://127.0.0.1:8000
```

**Health:** `GET /health` → `{"status":"ok"}`
**Admin:** `http://127.0.0.1:8000/admin` (use the superuser)
**Swagger:** `http://127.0.0.1:8000/swagger/`

---

## 🔐 Authentication (JWT)

### Get tokens (Swagger)

1. In Swagger: **POST** `/api/auth/token/`
2. Body:

```json
{"username": "<your_user>", "password": "<your_pass>"}
```

3. Copy `access` and `refresh`.

Click **Authorize** (lock icon) → paste:

```
Bearer <access>
```

### Get tokens (PowerShell)

```powershell
$BASE  = "http://127.0.0.1:8000"
$login = Invoke-RestMethod "$BASE/api/auth/token/" -Method Post -ContentType 'application/json' `
  -Body (@{ username='<user>'; password='<pass>' } | ConvertTo-Json)

$TOKEN   = $login.access
$REFRESH = $login.refresh
$HEAD    = @{ Authorization = "Bearer $TOKEN" }
```

### Refresh access (PowerShell)

```powershell
$refresh = Invoke-RestMethod "$BASE/api/auth/token/refresh/" -Method Post -ContentType 'application/json' `
  -Body (@{ refresh=$REFRESH } | ConvertTo-Json)
$TOKEN = $refresh.access
$HEAD  = @{ Authorization = "Bearer $TOKEN" }
```

> **Important:** Always send `Authorization: Bearer <access>` (with a space).
> **Dev tip:** You can extend token lifetimes in `employee_project/settings.py`:
>
> ```python
> from datetime import timedelta
> SIMPLE_JWT = {
>   "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
>   "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
> }
> ```

---

## 🧭 API Overview (Base: `/api/v1/`)

| Resource    | Endpoints                                                       | Notes                             |
| ----------- | --------------------------------------------------------------- | --------------------------------- |
| Employees   | `GET,POST /employees/`; `GET,PATCH,DELETE /employees/{id}/`     | Search, filter, order, pagination |
| Departments | `GET,POST /departments/`; `GET,PATCH,DELETE /departments/{id}/` | `name` unique                     |
| Attendance  | `GET,POST /attendance/`; `GET,PATCH,DELETE /attendance/{id}/`   | Unique `(employee, date)`         |
| Performance | `GET,POST /performance/`; `GET,PATCH,DELETE /performance/{id}/` | rating 1..5                       |
| Health      | `GET /health`                                                   | `{"status":"ok"}`                 |

### Filters / Search / Ordering / Pagination

* **Employees**

  * Search: `?search=<text>`
  * Filter: `?department=<id>&min_doj=YYYY-MM-DD&max_doj=YYYY-MM-DD`
  * Order: `?ordering=field` or `?ordering=-field` (e.g. `-date_of_joining`)
  * Pagination: `?page=2`
* **Attendance**

  * Filter: `?employee=<id>&status=Present|Absent|Late&min_date=YYYY-MM-DD&max_date=YYYY-MM-DD`
* **Performance**

  * Filter: `?employee=<id>&min_rating=3&max_rating=5&min_date=YYYY-MM-DD&max_date=YYYY-MM-DD`
* **Departments**

  * Search: `?search=<text>`
  * Order: `?ordering=name`

---

## ✍️ CRUD Examples (PowerShell)

> Assume `$BASE` and `$HEAD` are set (see Auth section).

### Departments

```powershell
# Create
$dept = irm "$BASE/api/v1/departments/" -Headers $HEAD -Method Post `
  -ContentType 'application/json' -Body (@{ name='Research' } | ConvertTo-Json)
$DID = $dept.id

# List / Search / Order
irm "$BASE/api/v1/departments/" -Headers $HEAD | % results | ft id,name
irm "$BASE/api/v1/departments/?search=Res" -Headers $HEAD | % results | ft id,name
irm "$BASE/api/v1/departments/?ordering=name" -Headers $HEAD | % results | ft id,name

# Update (unique name required)
irm "$BASE/api/v1/departments/$DID/" -Headers $HEAD -Method Patch `
  -ContentType 'application/json' -Body (@{ name='R&D HQ' } | ConvertTo-Json)

# Delete
irm "$BASE/api/v1/departments/$DID/" -Headers $HEAD -Method Delete
```

### Employees

```powershell
# Create
$emp = irm "$BASE/api/v1/employees/" -Headers $HEAD -Method Post `
  -ContentType 'application/json' -Body (@{
    name='John Tester'; email='john.tester@example.com'; phone_number='12345';
    address='42 Test Street'; date_of_joining='2024-08-15'; department=$DID
  } | ConvertTo-Json)
$EID = $emp.id

# Get / Search / Filter / Order / Page
irm "$BASE/api/v1/employees/$EID/" -Headers $HEAD
irm "$BASE/api/v1/employees/?search=John" -Headers $HEAD | Select-Object count
irm "$BASE/api/v1/employees/?department=$DID&min_doj=2024-01-01&max_doj=2025-12-31" -Headers $HEAD | Select-Object count
irm "$BASE/api/v1/employees/?ordering=-date_of_joining" -Headers $HEAD | % results | Select-Object -First 3 name,date_of_joining
irm "$BASE/api/v1/employees/?page=2" -Headers $HEAD | Select-Object count,next,previous

# Update
irm "$BASE/api/v1/employees/$EID/" -Headers $HEAD -Method Patch `
  -ContentType 'application/json' -Body (@{ phone_number='99999' } | ConvertTo-Json)

# Delete
irm "$BASE/api/v1/employees/$EID/" -Headers $HEAD -Method Delete
```

### Attendance

```powershell
# Create
irm "$BASE/api/v1/attendance/" -Headers $HEAD -Method Post `
  -ContentType 'application/json' -Body (@{
    employee=$EID; date='2025-09-01'; status='Present'
  } | ConvertTo-Json)

# Duplicate (should 400) — (employee, date) must be unique
try {
  irm "$BASE/api/v1/attendance/" -Headers $HEAD -Method Post `
    -ContentType 'application/json' -Body (@{
      employee=$EID; date='2025-09-01'; status='Late'
    } | ConvertTo-Json)
} catch { "Expected 400 -> HTTP " + $_.Exception.Response.StatusCode.value__ }

# Filter
irm "$BASE/api/v1/attendance/?employee=$EID&status=Present&min_date=2025-08-01&max_date=2025-09-30" `
  -Headers $HEAD | Select-Object count
```

### Performance

```powershell
# Create
irm "$BASE/api/v1/performance/" -Headers $HEAD -Method Post `
  -ContentType 'application/json' -Body (@{
    employee=$EID; rating=4; review_date='2025-08-20'
  } | ConvertTo-Json)

# Filter
irm "$BASE/api/v1/performance/?min_rating=4&min_date=2024-01-01" -Headers $HEAD | Select-Object count
```

---

## 📚 Swagger

* `http://127.0.0.1:8000/swagger/`
* Get tokens via **POST /api/auth/token/**
* Click **Authorize** → paste `Bearer <access>`
* “Try it out” on any endpoint

If you get **401**, refresh your token or re-login.

---

## 📊 Charts (Bonus)

* Page: `http://127.0.0.1:8000/analytics/charts/`

  * **Pie:** Employees per Department
  * **Bar:** Monthly Attendance
* JSON:

  * `/analytics/charts/data/employees-per-department/`
  * `/analytics/charts/data/monthly-attendance/`

---

## 🧪 Quick Checks & Counts

```powershell
# counts (proof after seeding)
(irm "$BASE/api/v1/employees/"   -Headers $HEAD).count
(irm "$BASE/api/v1/attendance/"  -Headers $HEAD).count
(irm "$BASE/api/v1/performance/" -Headers $HEAD).count
```

**Negative tests**

```powershell
# 401 (no token)
try { irm "$BASE/api/v1/employees/" } catch { "HTTP " + $_.Exception.Response.StatusCode.value__ }

# 404 (bad id)
try { irm "$BASE/api/v1/employees/999999/" -Headers $HEAD } catch { "HTTP " + $_.Exception.Response.StatusCode.value__ }

# 400 (bad payload)
try {
  irm "$BASE/api/v1/departments/" -Headers $HEAD -Method Post -ContentType 'application/json' -Body (@{} | ConvertTo-Json)
} catch { "HTTP " + $_.Exception.Response.StatusCode.value__ }
```

---

## 🧰 Common Errors & Fixes

| Error                    | Cause                                     | Fix                                                               |
| ------------------------ | ----------------------------------------- | ----------------------------------------------------------------- |
| 401 Unauthorized         | Missing/expired token or missing `Bearer` | Get new tokens, set header `Authorization: Bearer <access>`       |
| Token expired            | Access tokens are short-lived             | Use `POST /api/auth/token/refresh/` with `refresh` or login again |
| 400 Attendance duplicate | `(employee, date)` unique                 | Update existing record or choose a different date                 |
| 400 Dept duplicate name  | `Department.name` unique                  | Use a different name (e.g., add suffix)                           |
| 404 Not Found            | ID doesn’t exist                          | List first, then use an existing id                               |
| DB connection error      | Postgres not running / wrong URL          | Start DB, verify `DATABASE_URL`                                   |
| Invalid host header      | Host not in `ALLOWED_HOSTS`               | Add to `.env`: `ALLOWED_HOSTS=127.0.0.1,localhost`                |

#   e m p l o y e e _ p r o j e c t 
 
 
