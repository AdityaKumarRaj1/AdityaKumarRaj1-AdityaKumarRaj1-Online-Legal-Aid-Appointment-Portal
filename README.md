# ⚖️ Online Legal Aid Appointment Portal

A production-ready Django web application that simplifies legal aid access for citizens and provides a comprehensive tracking dashboard for lawyers and administrators.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.0+-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

1. [System Architecture](#-system-architecture)
2. [Features](#-features)
3. [User Roles & Permissions](#-user-roles--permissions)
4. [Database Design](#-database-design)
5. [ER Diagram](#-er-diagram)
6. [Project Structure](#-project-structure)
7. [Installation Guide](#-installation-guide)
8. [Appointment Workflow](#-appointment-workflow)
9. [API Reference](#-api-reference)
10. [Security](#-security)
11. [Deployment Guide](#-deployment-guide)
12. [Testing](#-testing)
13. [SRS Summary](#-srs-summary)

---

## 🏗 System Architecture

This application follows a **3-tier architecture**:

```
┌──────────────────────────────────────────────┐
│              PRESENTATION LAYER              │
│  HTML Templates + Bootstrap 5 + JavaScript   │
│  ─ Responsive UI, AJAX interactions          │
│  ─ Client-side validation                    │
└──────────────────────┬───────────────────────┘
                       │ HTTP/HTTPS
┌──────────────────────┴───────────────────────┐
│              APPLICATION LAYER               │
│     Django 5.x (Python Web Framework)        │
│  ─ Views, Forms, Serializers                 │
│  ─ Authentication & Authorization            │
│  ─ Business Logic & Workflow Engine          │
│  ─ REST API (Django REST Framework)          │
└──────────────────────┬───────────────────────┘
                       │ SQL/ORM
┌──────────────────────┴───────────────────────┐
│                DATA LAYER                    │
│           PostgreSQL Database                │
│  ─ Users, Lawyers, Appointments              │
│  ─ Categories, Documents                     │
│  ─ Indexed queries, relationships            │
└──────────────────────────────────────────────┘
```

### Technology Stack

| Layer        | Technology                              |
|:-------------|:----------------------------------------|
| Frontend     | HTML5, CSS3, JavaScript, Bootstrap 5.3  |
| Backend      | Django 5.x, Django REST Framework       |
| Database     | PostgreSQL 15+ (SQLite for dev)         |
| Auth         | Django Authentication System            |
| File Storage | Django FileField (local / cloud)        |
| API          | REST API for mobile integration         |

---

## ✨ Features

### 👤 Citizen Features
- ✅ Register and login securely
- ✅ Browse verified lawyers by category, name, experience
- ✅ Book appointments with preferred date/time
- ✅ Select legal category for each appointment
- ✅ Upload legal documents (PDF, DOC, images)
- ✅ Track appointment status (Pending → Accepted → Completed)
- ✅ View full appointment history
- ✅ Cancel pending/accepted appointments

### ⚖️ Lawyer Features
- ✅ Dedicated lawyer dashboard with analytics
- ✅ View incoming appointment requests
- ✅ Accept or reject appointments
- ✅ Mark appointments as completed
- ✅ Update professional profile and availability
- ✅ View client details and uploaded documents

### 🔧 Admin Features
- ✅ System-wide analytics dashboard
- ✅ Manage all users (citizens, lawyers, admins)
- ✅ Verify/reject lawyer registrations
- ✅ Manage legal categories
- ✅ Monitor all appointments across the platform
- ✅ Category-wise appointment statistics

---

## 👥 User Roles & Permissions

| Feature                    | Citizen | Lawyer | Admin |
|:---------------------------|:-------:|:------:|:-----:|
| Register / Login           |    ✅   |   ✅   |   ✅  |
| Browse Lawyers             |    ✅   |   ❌   |   ✅  |
| Book Appointment           |    ✅   |   ❌   |   ❌  |
| Upload Documents           |    ✅   |   ✅   |   ❌  |
| Accept/Reject Appointments |    ❌   |   ✅   |   ❌  |
| Lawyer Dashboard           |    ❌   |   ✅   |   ❌  |
| Admin Dashboard            |    ❌   |   ❌   |   ✅  |
| Manage Users               |    ❌   |   ❌   |   ✅  |
| Verify Lawyers             |    ❌   |   ❌   |   ✅  |
| Manage Categories          |    ❌   |   ❌   |   ✅  |

---

## 🗄 Database Design

### Tables & Schema

#### `users` (Custom User)
| Column          | Type         | Constraints              |
|:----------------|:-------------|:-------------------------|
| id              | BigAutoField | PK                       |
| username        | VARCHAR(150) | UNIQUE, NOT NULL         |
| email           | VARCHAR(254) | NOT NULL                 |
| first_name      | VARCHAR(30)  |                          |
| last_name       | VARCHAR(30)  |                          |
| role            | VARCHAR(10)  | CITIZEN/LAWYER/ADMIN     |
| phone           | VARCHAR(15)  |                          |
| address         | TEXT         |                          |
| city            | VARCHAR(100) |                          |
| state           | VARCHAR(100) |                          |
| pincode         | VARCHAR(10)  |                          |
| profile_picture | IMAGE        |                          |
| date_of_birth   | DATE         |                          |
| password        | VARCHAR(128) | Hashed                   |
| created_at      | DATETIME     | auto                     |

#### `lawyer_profiles`
| Column               | Type          | Constraints              |
|:---------------------|:--------------|:-------------------------|
| id                   | BigAutoField  | PK                       |
| user_id              | BigInt        | FK → users, UNIQUE       |
| bar_council_id       | VARCHAR(50)   | UNIQUE                   |
| experience_years     | INT           |                          |
| qualification        | VARCHAR(255)  |                          |
| bio                  | TEXT          |                          |
| consultation_fee     | DECIMAL(10,2) |                          |
| is_verified          | BOOLEAN       | Default: False           |
| verification_status  | VARCHAR(10)   | PENDING/VERIFIED/REJECTED|
| is_available         | BOOLEAN       | Default: True            |
| rating               | DECIMAL(3,2)  |                          |
| total_cases          | INT           |                          |

#### `legal_categories`
| Column      | Type         | Constraints      |
|:------------|:-------------|:-----------------|
| id          | BigAutoField | PK               |
| name        | VARCHAR(200) | UNIQUE           |
| slug        | VARCHAR(200) | UNIQUE           |
| description | TEXT         |                  |
| icon        | VARCHAR(50)  |                  |
| is_active   | BOOLEAN      | Default: True    |

#### `appointments`
| Column           | Type          | Constraints             |
|:-----------------|:--------------|:------------------------|
| id               | BigAutoField  | PK                      |
| citizen_id       | BigInt        | FK → users              |
| lawyer_id        | BigInt        | FK → lawyer_profiles    |
| category_id      | BigInt        | FK → legal_categories   |
| subject          | VARCHAR(300)  |                         |
| description      | TEXT          |                         |
| appointment_date | DATE          |                         |
| appointment_time | TIME          |                         |
| status           | VARCHAR(10)   | PENDING/ACCEPTED/etc.   |
| priority         | VARCHAR(6)    | LOW/MEDIUM/HIGH/URGENT  |
| created_at       | DATETIME      | auto                    |

#### `documents`
| Column        | Type         | Constraints           |
|:------------- |:-------------|:----------------------|
| id            | BigAutoField | PK                    |
| appointment_id| BigInt       | FK → appointments     |
| uploaded_by_id| BigInt       | FK → users            |
| title         | VARCHAR(255) |                       |
| document_type | VARCHAR(10)  | IDENTITY/LEGAL/etc.   |
| file          | FILE         |                       |
| file_size     | INT          |                       |
| uploaded_at   | DATETIME     | auto                  |

---

## 📊 ER Diagram

```
┌─────────────┐     1:1     ┌─────────────────┐
│    Users     │─────────────│  LawyerProfile   │
│             │              │                 │
│ - id (PK)  │              │ - id (PK)       │
│ - role     │              │ - user_id (FK)  │
│ - email    │              │ - bar_council_id│
│ - phone    │              │ - is_verified   │
└──────┬──────┘              └────────┬────────┘
       │                              │
       │ 1:N                          │ N:M
       │                              │
┌──────┴──────┐              ┌────────┴────────┐
│ Appointments│              │ LegalCategories  │
│             │──────────────│                 │
│ - id (PK)  │  N:1         │ - id (PK)       │
│ - citizen_id│              │ - name          │
│ - lawyer_id │              │ - slug          │
│ - category  │              └─────────────────┘
│ - status    │
│ - date/time │
└──────┬──────┘
       │ 1:N
       │
┌──────┴──────┐
│  Documents   │
│             │
│ - id (PK)  │
│ - apt_id   │
│ - file     │
│ - type     │
└─────────────┘
```

### Relationships
- **Users ↔ LawyerProfile**: One-to-One (a lawyer user has one profile)
- **Users ↔ Appointments**: One-to-Many (a citizen can have many appointments)
- **LawyerProfile ↔ Appointments**: One-to-Many (a lawyer can have many appointments)
- **LawyerProfile ↔ LegalCategories**: Many-to-Many (lawyers can specialize in multiple categories)
- **Appointments ↔ Documents**: One-to-Many (an appointment can have many documents)
- **LegalCategories ↔ Appointments**: One-to-Many (each appointment belongs to one category)

---

## 📁 Project Structure

```
legal/
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── .gitignore
├── README.md
│
├── legal_aid_portal/             # Main project config
│   ├── __init__.py
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                     # User management app
│   ├── models.py                 # Custom User model
│   ├── views.py                  # Auth views
│   ├── forms.py                  # Registration/login forms
│   ├── urls.py                   # Account URLs
│   ├── admin.py                  # Admin configuration
│   ├── serializers.py            # REST API serializers
│   ├── api_views.py              # REST API views
│   ├── api_urls.py               # API URL patterns
│   └── tests.py                  # Unit tests
│
├── lawyers/                      # Lawyer profiles app
│   ├── models.py                 # LawyerProfile, Availability
│   ├── views.py                  # Lawyer views & dashboard
│   ├── forms.py                  # Profile forms
│   ├── urls.py
│   ├── admin.py
│   ├── serializers.py
│   ├── api_views.py
│   └── api_urls.py
│
├── appointments/                 # Appointment management app
│   ├── models.py                 # Appointment, Document
│   ├── views.py                  # Booking, tracking views
│   ├── forms.py                  # Booking & upload forms
│   ├── urls.py
│   ├── admin.py
│   ├── serializers.py
│   ├── api_views.py
│   ├── api_urls.py
│   └── tests.py
│
├── categories/                   # Legal categories app
│   ├── models.py                 # LegalCategory
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── dashboard/                    # Dashboard app
│   ├── views.py                  # Citizen & Admin dashboards
│   └── urls.py
│
├── templates/                    # HTML templates
│   ├── base.html                 # Base template
│   ├── home.html                 # Landing page
│   ├── accounts/                 # Auth templates
│   ├── lawyers/                  # Lawyer templates
│   ├── appointments/             # Appointment templates
│   ├── categories/               # Category templates
│   └── dashboard/                # Dashboard templates
│
├── static/                       # Static files
│   ├── css/style.css             # Custom CSS
│   ├── js/main.js                # Custom JavaScript
│   └── images/
│
├── media/                        # User uploads
│   ├── documents/
│   └── profile_pics/
│
└── logs/                         # Application logs
```

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.10+
- PostgreSQL 15+ (or use SQLite for development)
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/legal-aid-portal.git
cd legal-aid-portal
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

**Option A: PostgreSQL (Recommended)**
```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE legal_aid_db;
\q
```

Set environment variables:
```bash
set DB_NAME=legal_aid_db
set DB_USER=postgres
set DB_PASSWORD=yourpassword
```

**Option B: SQLite (Quick Development)**
```bash
set USE_SQLITE=True
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Load Sample Data (Optional)
```bash
python manage.py shell
```
```python
from categories.models import LegalCategory
categories = [
    ('Family Law', 'bi-house-heart', 'Legal matters related to family and domestic relations'),
    ('Criminal Law', 'bi-shield-exclamation', 'Defense and prosecution in criminal cases'),
    ('Property Law', 'bi-building', 'Real estate, land disputes, and property rights'),
    ('Labor Law', 'bi-briefcase', 'Employment disputes and workers rights'),
    ('Cyber Law', 'bi-laptop', 'Cyber crimes, data protection, and IT law'),
    ('Tax Law', 'bi-calculator', 'Tax planning, disputes, and compliance'),
    ('Corporate Law', 'bi-bank', 'Business law, mergers, and acquisitions'),
    ('Constitutional Law', 'bi-book', 'Fundamental rights and constitutional matters'),
    ('Consumer Law', 'bi-cart', 'Consumer protection and dispute resolution'),
    ('Immigration Law', 'bi-globe', 'Visa, citizenship, and immigration matters'),
]
for name, icon, desc in categories:
    LegalCategory.objects.get_or_create(name=name, defaults={'icon': icon, 'description': desc})
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 🔄 Appointment Workflow

```
┌──────────┐     Book       ┌──────────┐     Review      ┌──────────┐
│ Citizen  │────────────────▶│ PENDING  │────────────────▶│  Lawyer  │
│ Register │                 │          │                  │ Reviews  │
└──────────┘                 └────┬─────┘                  └──┬───┬──┘
                                  │                           │   │
                                  │                    Accept │   │ Reject
                                  │                           │   │
                                  │                    ┌──────▼─┐ │
                                  │                    │ACCEPTED│ │
                                  │                    └──┬─────┘ │
                                  │                       │       │
                                  │              Complete │       │
                                  │                       │       │
                             ┌────▼─────┐         ┌──────▼─┐  ┌──▼──────┐
                             │CANCELLED │         │COMPLETE│  │REJECTED │
                             │(by user) │         │        │  │         │
                             └──────────┘         └────────┘  └─────────┘
```

1. **Citizen registers** → Creates account with CITIZEN role
2. **Citizen browses** → Searches lawyers by category/name/experience
3. **Citizen books** → Selects date, time, uploads documents → Status: `PENDING`
4. **Lawyer receives** → Sees request in dashboard
5. **Lawyer decides** → Accepts (`ACCEPTED`) or Rejects (`REJECTED`)
6. **Consultation happens** → Lawyer marks complete (`COMPLETED`)
7. **Citizen tracks** → Full visibility from citizen dashboard

---

## 🔌 API Reference

### Authentication
| Method | Endpoint                    | Description           |
|--------|-----------------------------|-----------------------|
| POST   | `/api/auth/register/`       | Register new user     |
| GET    | `/api/auth/profile/`        | Get current user      |
| PUT    | `/api/auth/profile/`        | Update profile        |

### Lawyers
| Method | Endpoint                    | Description           |
|--------|-----------------------------|-----------------------|
| GET    | `/api/lawyers/`             | List verified lawyers |
| GET    | `/api/lawyers/<id>/`        | Lawyer detail         |

### Appointments
| Method | Endpoint                           | Description                |
|--------|-------------------------------------|----------------------------|
| GET    | `/api/appointments/`               | List my appointments       |
| POST   | `/api/appointments/create/`        | Create appointment         |
| GET    | `/api/appointments/<id>/`          | Appointment detail         |
| PATCH  | `/api/appointments/<id>/status/`   | Update status (lawyer)     |

---

## 🔐 Security

| Feature                | Implementation                                    |
|:-----------------------|:--------------------------------------------------|
| Authentication         | Django's built-in auth system                     |
| Password Encryption    | PBKDF2 with SHA-256 hash (Django default)         |
| CSRF Protection        | Django CSRF middleware on all POST requests        |
| XSS Protection         | Template auto-escaping + CSP headers              |
| SQL Injection          | ORM parameterized queries                         |
| Clickjacking           | X-Frame-Options: DENY                             |
| HTTPS (Production)     | SECURE_SSL_REDIRECT + HSTS                        |
| File Upload Validation | Type checking + size limits (10 MB)               |
| Session Security       | Secure cookies, session expiry                    |
| Role-Based Access      | Decorator-based permission checks                 |

---

## 🌐 Deployment Guide (Production)

### Step 1: Server Setup
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql nginx
```

### Step 2: Clone & Configure
```bash
cd /var/www
git clone https://github.com/yourusername/legal-aid-portal.git
cd legal-aid-portal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Environment Variables
```bash
export DJANGO_SECRET_KEY='your-production-secret-key'
export DJANGO_DEBUG='False'
export DJANGO_ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
export DB_NAME='legal_aid_db'
export DB_USER='legal_user'
export DB_PASSWORD='secure_password'
```

### Step 4: Database & Static Files
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Step 5: Gunicorn
```bash
pip install gunicorn
gunicorn legal_aid_portal.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Step 6: Gunicorn Service
```ini
# /etc/systemd/system/legalaid.service
[Unit]
Description=Legal Aid Portal Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/legal-aid-portal
ExecStart=/var/www/legal-aid-portal/venv/bin/gunicorn \
    legal_aid_portal.wsgi:application \
    --bind unix:/var/www/legal-aid-portal/legalaid.sock \
    --workers 3

[Install]
WantedBy=multi-user.target
```

### Step 7: Nginx Configuration
```nginx
# /etc/nginx/sites-available/legalaid
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /var/www/legal-aid-portal/staticfiles/;
    }

    location /media/ {
        alias /var/www/legal-aid-portal/media/;
    }

    location / {
        proxy_pass http://unix:/var/www/legal-aid-portal/legalaid.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/legalaid /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl start legalaid
sudo systemctl enable legalaid
```

---

## 🧪 Testing

### Run All Tests
```bash
# Using SQLite for testing
set USE_SQLITE=True
python manage.py test
```

### Test Coverage
| Module        | Tests                                    |
|:--------------|:-----------------------------------------|
| Accounts      | User creation, login, register, logout   |
| Appointments  | Booking, cancel, accept, reject, detail  |
| Dashboard     | Access control, citizen/admin views      |
| API           | Registration, profile, CRUD              |

### Run Specific App Tests
```bash
python manage.py test accounts
python manage.py test appointments
```

---

## 📄 SRS Summary

### Software Requirements Specification

**Project:** Online Legal Aid Appointment Portal  
**Version:** 1.0  
**Date:** March 2026

#### Purpose
To provide an accessible platform for citizens to connect with verified lawyers and schedule legal consultations efficiently.

#### Scope
- Multi-role web application (Citizen, Lawyer, Admin)
- Appointment booking and lifecycle management
- Document upload and management
- Admin oversight and analytics
- REST API for future mobile integration

#### Non-Functional Requirements

| Requirement    | Specification                                      |
|:---------------|:---------------------------------------------------|
| **Security**   | HTTPS, CSRF, XSS protection, password hashing      |
| **Performance**| Page load < 2s, DB-indexed queries, caching-ready   |
| **Usability**  | Responsive design, accessible navigation            |
| **Reliability**| 99.5% uptime target, error logging                  |
| **Scalability**| Horizontal scaling via Gunicorn workers + Nginx LB   |

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Built with ❤️ using Django, PostgreSQL, and Bootstrap**
