# Role-Based Student Management System API

### A Secure • Scalable • Test-Driven Academic Management Backend

<p>
  <strong>Django REST Framework</strong> ·
  <strong>JWT Authentication</strong> ·
  <strong>PostgreSQL</strong> ·
  <strong>Supabase</strong> ·
  <strong>Docker</strong> ·
  <strong>OpenAPI</strong>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/Django-REST%20Framework-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/Docker-Development-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Supabase-Production-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase">
  <img src="https://img.shields.io/badge/OpenAPI-Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="OpenAPI Swagger">
</p>

<p>
  <img src="https://img.shields.io/badge/Architecture-Role--Based%20Access-purple?style=flat-square" alt="RBAC">
  <img src="https://img.shields.io/badge/Development-TDD-red?style=flat-square" alt="TDD">
  <img src="https://img.shields.io/badge/API-REST-orange?style=flat-square" alt="REST API">
  <img src="https://img.shields.io/badge/Documentation-Automated-blue?style=flat-square" alt="API Documentation">
</p>

<br>

> **A production-oriented Student Management REST API designed around strict role-based access control, secure JWT authentication, automated academic notifications, PostgreSQL persistence, and Test-Driven Development.**

</div>

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Core Capabilities](#-core-capabilities)
  - [Secure Authentication](#-secure-authentication)
  - [User Management](#-user-management)
  - [Course Management](#-course-management)
  - [Enrollment Management](#-enrollment-management)
  - [Automated Notifications](#-automated-notifications)
  - [Test-Driven Development](#-test-driven-development)
  - [Developer-Friendly API](#-developer-friendly-api)
- [Role-Based Access Control](#role-based-access-control)
  - [Permission Matrix](#permission-matrix)
  - [Admin](#admin)
    - [User Management](#user-management)
    - [Course Management](#course-management)
    - [Enrollment Management](#enrollment-management)
    - [System Oversight](#system-oversight)
  - [Teacher](#teacher)
    - [Profile Management](#profile-management)
    - [Course Visibility](#course-visibility)
    - [Enrollment Management](#enrollment-management-1)
    - [Student Visibility](#student-visibility)
  - [Student](#student)
    - [Profile Management](#profile-management-1)
    - [Course Visibility](#course-visibility-1)
- [Automated Email Notifications](#automated-email-notifications)
    - [User Provisioning](#user-provisioning)
    - [Course Assignment](#course-assignment)
    - [Student Enrollment](#student-enrollment)
    - [Student Removal](#student-removal)
    - [Notification Events](#notification-events)
  - [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#-project-structure)
- [Local Installation](#local-installation)
  - [Prerequisites](#prerequisites)
    - [1. Clone the Repository](#1️⃣-clone-the-repository)
    - [2. Create a Virtual Environment](#2️⃣-create-a-virtual-environment)
    - [3. Install Dependencies](#3️⃣-install-dependencies)
    - [4. Start PostgreSQL with Docker](#4️⃣-start-postgresql-with-docker)
- [Environment Configuration](#environment-configuration)
  - [Database Migrations](#database-migrations)
    - [Create an Initial Admin](#create-an-initial-admin)
    - [Running the API](#running-the-api)
  - [API Documentation](#api-documentation)
  - [Authentication](#authentication)
    - [Authentication Flow](#authentication-flow)
  - [Workflows](#workflows)
    - [New User](#new-user)
    - [Teacher Assignment](#teacher-assignment)
    - [Student Enrollment](#student-enrollment-1)
    - [Student Removal](#student-removal-1)
- [Supabase Production Setup](#supabase-production-setup)
    - [1. Retrieve Database Credentials](#1️⃣-retrieve-database-credentials)
    - [2. Update Production Environment Variables](#2️⃣-update-production-environment-variables)
    - [3. Apply Production Migrations](#3️⃣-apply-production-migrations)
- [License](#license)
---

#  Project Overview

The **Role-Based Student Management System API** is a comprehensive academic management backend built with **Django**, **Django REST Framework (DRF)**, **JWT Authentication**, and **PostgreSQL**.

The system is designed around a strict **Role-Based Access Control (RBAC)** model where every authenticated user operates within a clearly defined permission boundary.

Three primary roles are supported:

| Role | Responsibility | Access Level |
|---|---|---|
|  **Admin** | System-wide administration | Full |
|  **Teacher** | Course & enrollment management | Scoped |
|  **Student** | Personal academic information | Read-focused |

The API follows **RESTful architecture**, uses **JWT bearer authentication**, provides automatically generated **OpenAPI documentation**, and was developed using **Test-Driven Development (TDD)** principles.

---

# 🎯 Core Capabilities

### 🔐 Secure Authentication
- JWT-based authentication.
- Protected API endpoints.
- Bearer-token authorization.
- Role-aware permission enforcement.
- Secure separation between user roles.

### 👥 User Management
- Admin-controlled Teacher and Student creation.
- Role assignment.
- Profile management.
- Automated credential delivery via email.

### 📚 Course Management
- Course creation and modification.
- Teacher assignment.
- Course scheduling.
- Course duration and descriptions.
- Role-specific course visibility.

### 🎓 Enrollment Management
- Student enrollment.
- Student removal.
- Enrollment status tracking.
- Teacher-scoped enrollment management.
- System-wide administrative oversight.

### 📧 Automated Notifications
- Account provisioning emails.
- Teacher assignment notifications.
- Enrollment notifications.
- Removal notifications.

### 🧪 Test-Driven Development
- Django `TestCase`.
- DRF `APITestCase`.
- Authentication tests.
- Permission tests.
- Database behavior tests.
- Email notification tests.

### 📖 Developer-Friendly API
- RESTful endpoints.
- OpenAPI schema generation.
- Swagger UI.
- Clear separation of application domains.

---

# Role-Based Access Control

The API implements strict **Role-Based Access Control (RBAC)**.

Every protected request must provide a valid JWT:

```http
Authorization: Bearer <access-token>
```

Access is determined by both:
* Authenticated identity
* Assigned application role

### Permission Matrix

| Capability | Admin | Teacher | Student |
| :--- | :---: | :---: | :---: |
| View own profile | ✅ | ✅ | ✅ |
| Edit own profile | ✅ | ✅ | ⚠️ |
| Create users | ✅ | ❌ | ❌ |
| Assign roles | ✅ | ❌ | ❌ |
| View all users | ✅ | ❌ | ❌ |
| Create courses | ✅ | ❌ | ❌ |
| Update courses | ✅ | ❌ | ❌ |
| Delete courses | ✅ | ❌ | ❌ |
| Assign teachers | ✅ | ❌ | ❌ |
| View assigned courses | ✅ | ✅ | ✅ |
| Enroll students | ✅ | ✅ | ❌ |
| Remove students | ✅ | ✅ | ❌ |
| View enrollments | ✅ | ✅ | ❌ |
| View enrolled students | ✅ | ✅ | ❌ |
| View own enrolled courses | ✅ | ❌ | ✅ |

* Teacher access is restricted to courses assigned to that teacher.
---
### Admin

The Admin represents the highest-authority role within the system.
Admins have complete visibility and management capabilities across the academic platform.

#### User Management

Admins can:

* Create Teacher accounts.
* Create Student accounts.
* Assign application roles.
* View user profiles.
* Manage system users.
* Trigger automatic credential emails.

*When a new Teacher or Student is created, their login credentials are automatically sent to their registered email address.*

#### Course Management

Admins have complete CRUD access over courses:

* Create courses.
* View courses.
* Update courses.
* Delete courses.
* Assign teachers to courses.

*When a teacher is assigned to a course, the system automatically sends an assignment notification.*

#### Enrollment Management

Admins can:

* Enroll any student into any course.
* Remove any student from any course.
* View all enrollment records.
* Monitor enrollment status system-wide.

#### System Oversight

Admins have complete visibility over:

* Users.
* Courses.
* Teachers.
* Students.
* Enrollments.
* Academic relationships.
---
### Teacher

Teachers manage the academic progress associated with their assigned courses.
Teacher permissions are scoped to prevent unauthorized access to unrelated courses or students.

#### Profile Management

Teachers can:

* View their profile.
* Update permitted personal information.
* Change profile details where allowed.

*Email addresses are non-editable through the Teacher profile workflow.*

#### Course Visibility

Teachers can view courses assigned to them, including:

* Course title.
* Description.
* Duration.
* Schedule.
* Associated students.

Teachers cannot:

* Create courses.
* Delete courses.
* Manage courses belonging to other teachers.

#### Enrollment Management

Within their own assigned courses, Teachers can:

* Enroll students.
* Remove students.
* View enrolled students.
* Track enrollment status.

Supported enrollment states include:

* active
* dropped


*A Teacher cannot manipulate enrollment records belonging to another Teacher's course.*

#### Student Visibility

Teachers can view student profiles for students enrolled in their own courses.

---
### Student

Students have limited access focused on their own academic information.

#### Profile Management

Students can view:

* Name.
* Email.
* Enrollment year.
* Batch.
* Roll number.
* Other permitted profile information.

Students can edit:

* Name.
* Password.

*Students cannot modify protected academic fields or their email address.*

#### Course Visibility

Students can view their enrolled courses, including:

* Course title.
* Course description.
* Course duration.
* Course schedule.
* Assigned teacher.

*Students have read-focused access to their academic records.*

---

## Automated Email Notifications

The system automatically generates email notifications for important academic events.

#### User Provisioning

When an Admin creates a Teacher or Student:
```
Admin
  │
  ├── Creates User
  │
  └── System generates credentials
            │
            ▼
       Email sent to user
```

The newly created user receives their login credentials through email.

#### Course Assignment

When an Admin assigns a Teacher to a course:
```
Admin
  │
  └── Assigns Teacher
          │
          ▼
   Teacher notification
```
#### Student Enrollment

When a Student is enrolled:
```
Teacher/Admin
      │
      └── Enroll Student
              │
              ├──► Student notification
              │
              └──► Teacher notification
```
#### Student Removal

When a Student is removed from a course:
```
Teacher/Admin
      │
      └── Remove Student
              │
              ├──► Student notification
              │
              └──► Teacher notification
```

#### Notification Events
|Event|Student|Teacher|
| :--- | :---: | :---: |
|Account creation|✅|✅|
|Teacher assigned to course|❌|✅|
|Student enrolled|✅|✅|
|Student removed|✅|✅|

---

### Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.12+ |
| **Backend** | Django |
| **API Framework** | Django REST Framework (DRF) |
| **Authentication** | JWT / JSON Web Tokens |
| **JWT Library** | `djangorestframework-simplejwt` |
| **Database** | PostgreSQL |
| **Local Database** | Docker / Docker Compose |
| **Production Database** | Supabase PostgreSQL |
| **API Specification** | OpenAPI |
| **API Explorer** | Swagger UI |
| **Documentation Generator** | `drf-spectacular` |
| **Testing** | Django TestCase / DRF APITestCase |
| **Notifications** | Email-based automated notifications |
| **Version Control** | Git |

---

## System Architecture

The application follows a modular REST API architecture.

                         ┌───────────────────────┐
                         │       API Client      │
                         │ Web / Mobile / Postman│
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      JWT Auth Layer   │
                         │ Authentication + RBAC │
                         └───────────┬───────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
             ┌────────────┐   ┌────────────┐   ┌────────────┐
             │  Accounts  │   │  Courses   │   │Enrollments │
             │    App     │   │    App     │   │    App     │
             └─────┬──────┘   └─────┬──────┘   └─────┬──────┘
                   │                │                │
                   └────────────────┼────────────────┘
                                    │
                                    ▼
                         ┌───────────────────────┐
                         │      PostgreSQL       │
                         │        Database       │
                         └───────────────────────┘
                                    │
                                    ▼
                         ┌───────────────────────┐
                         │   Email Notification  │
                         │        Service        │
                         └───────────────────────┘


---

## 📁 Project Structure

```
student_management_system/
│
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── .env
├── .gitignore
├── README.md
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── courses/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── enrollments/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
└── core/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

*The exact structure may vary depending on the final configuration. I will try and keep the README.md up to date*

---

## Local Installation
### Prerequisites

Before starting, make sure the following are installed:
* Python 3.12+
* Docker
* Docker Compose
* Git

Verify your environment:
* python --version
* docker --version
* docker compose version
* git --version

#### 1️⃣ Clone the Repository
```
git clone https://github.com/AkhnasFurqan-Dev/student-management-system-django-drf.git
cd student_management_system
```
#### 2️⃣ Create a Virtual Environment
* Linux / macOS
```
python -m venv venv
source venv/bin/activate
```
* Windows
```
python -m venv venv
venv\Scripts\activate
```
#### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
#### 4️⃣ Start PostgreSQL with Docker

Make sure Docker is running. Then start the PostgreSQL container:
```
docker compose up -d
```
Verify running containers:
```
docker compose ps
```
---
## Environment Configuration

Create a .env file in the project root.

Example local configuration:
```
SECRET_KEY=your-super-secret-key-for-local-dev
DEBUG=True

DB_NAME=sms_dev
DB_USER=sms_user
DB_PASSWORD=sms_pass
DB_HOST=localhost
DB_PORT=5432
```
Add .env to .gitignore:
```
.env
venv/
__pycache__/
*.pyc
```

### Database Migrations

Once PostgreSQL is running and your environment variables are configured, run:
```
python manage.py makemigrations
python manage.py migrate
```
#### Create an Initial Admin
Run:
```
python manage.py createsuperuser
```
Follow the prompts to configure the administrator account.

#### Running the API

Start the Django development server:
```
python manage.py runserver
```
The API will be available at:
```
http://127.0.0.1:8000/
or
http://localhost:8000/
```
To access admin panel, login with superuser credentials you created at:
```
http://127.0.0.1:8000/admin
or
http://localhost:8000/admin
```
To run the test suite:
```
python manage.py test
```
---
### API Documentation

The API documentation is automatically generated using:

* OpenAPI
* drf-spectacular
* Swagger UI

With the development server running, use:

* Swagger UI
```
http://127.0.0.1:8000/api/docs/
```
* OpenAPI Schema
```
http://127.0.0.1:8000/api/schema/
```
---
### Authentication

Protected endpoints require a valid JWT access token.

An authenticated request looks like:
```
GET /api/<protected-endpoint>/
Authorization: Bearer eyJ...
```
#### Authentication Flow
```
┌──────────────┐
│     User     │
└──────┬───────┘
       │ Login
       ▼
┌──────────────┐
│ Auth Endpoint│
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ JWT Access Token │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Protected API    │
│ Request          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Authentication + │
│ RBAC Validation  │
└────────┬─────────┘
         │
      ┌──┴──┐
      │     │
    ALLOW  DENY
```
---
### Workflows

#### New User
```
      Admin
        │
        ▼
Create Teacher / Student
        │
        ▼
  Generate Account
        │
        ▼
Generate Credentials
        │
        ▼
    Send Email
        │
        ▼
User Can Authenticate
```
#### Teacher Assignment
```
    Admin
      │
      ▼
Select Course
      │
      ▼
Assign Teacher
      │
      ▼
Persist Assignment
      │
      ▼
Notify Teacher
```
#### Student Enrollment
```
Admin / Authorized Teacher
          │
          ▼
    Select Student
          │
          ▼
     Select Course
          │
          ▼
   Create Enrollment
          │
       ┌──┴──┐
       ▼     ▼
   Student  Teacher
   Email    Email
```
#### Student Removal
```
  Admin / Course Teacher
          │
          ▼
    Select Enrollment
          │
          ▼
   Remove / Update Status
          │
       ┌──┴──┐
       ▼     ▼
   Student  Teacher
   Email    Email
```
---

## Supabase Production Setup

For production deployment, the application can use a Supabase PostgreSQL database.

#### 1️⃣ Retrieve Database Credentials

From the Supabase dashboard, retrieve the database connection information.
Use the Session Pooler configuration where appropriate.

#### 2️⃣ Update Production Environment Variables

Example:
```
SECRET_KEY=<production-secret-key>
DEBUG=False

DB_NAME=postgres
DB_USER=postgres.<your-project-ref>
DB_PASSWORD=<your-database-password>
DB_HOST=aws-0-<region>.pooler.supabase.com
DB_PORT=5432
```
*Replace all placeholder values with the credentials provided by your Supabase project.*

#### 3️⃣ Apply Production Migrations

After configuring the production environment, migrate the database schema:
```
python manage.py migrate
```
*This creates the required Django database schema in your Supabase PostgreSQL database.*

The Role-Based Student Management System API combines:
```
                    ┌─────────────────────────┐
                    │   Student Management    │
                    │          API            │
                    └────────────┬────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
   ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
   │    RBAC     │       │    JWT      │       │ PostgreSQL  │
   │             │       │    Auth     │       │             │
   └─────────────┘       └─────────────┘       └─────────────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │       Django REST       │
                    │        Framework        │
                    └────────────┬────────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
             ▼                   ▼                   ▼
       ┌───────────┐       ┌───────────┐       ┌───────────┐
       │ Accounts  │       │  Courses  │       │Enrollments│
       └───────────┘       └───────────┘       └───────────┘
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 │
                         ┌───────▼───────┐
                         │ Automated     │
                         │ Notifications │
                         └───────────────┘
```
---
## License
#### MIT LICENSE
```
Copyright 2026 AKHNAS FURQAN

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```