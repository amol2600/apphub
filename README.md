# AppHub - Expense Tracker

A modern Expense Tracker built with **Django** and **PostgreSQL** that helps users manage their personal finances with secure authentication, dashboards, charts, filtering, and print support.

> **Status:** Production Ready (Expense Tracker Module)

---

# Features

## Authentication

- User Registration
- Email Verification (Brevo API)
- Secure Login & Logout
- Forgot Password
- Password Reset via Email (Brevo API)
- Django Password Validation
- User-specific Data Isolation

---

## Expense Management

- Add Transactions
- Edit Transactions
- Delete Transactions
- Add Categories
- Edit Categories
- Delete Categories
- Category-based Organization

---

## Dashboard

- Total Income
- Total Expenses
- Current Balance
- Category-wise Pie Chart

---

## Search & Filters

- Search Transactions
- Filter by Category
- Filter by Transaction Type

---

## Printing

- Print-Friendly Transaction List
- Automatic Removal of Navigation and Action Buttons
- Optimized Print Styling

---

## Security

- Email Verification
- Password Reset Tokens
- Password Validation
- CSRF Protection
- Session Authentication
- User Data Isolation
- Secure Production Configuration

---

# Tech Stack

## Backend

- Django 6
- Python 3

## Database

- PostgreSQL (Neon)

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## Email Service

- Brevo Transactional Email API

## Deployment

- Render
- Gunicorn
- WhiteNoise

---

# Project Structure

```text
accounts/
apphub/
expense_tracker/
home/
static/
templates/
manage.py
requirements.txt
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/amol2600/apphub.git
```

Go into the project

```bash
cd apphub
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key

# Local Development=True
# Production=False
DEBUG=False

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432

BREVO_API_KEY=your_brevo_api_key
BREVO_SENDER_EMAIL=your_verified_sender@example.com
BREVO_SENDER_NAME=AppHub
```

---

# Database

Apply migrations

```bash
python manage.py migrate
```

Create a superuser

```bash
python manage.py createsuperuser
```

Run the development server

```bash
python manage.py runserver
```

---

# Deployment

This project is configured for production deployment on **Render** using:

- Gunicorn
- WhiteNoise
- PostgreSQL (Neon)
- Brevo Transactional Email API

---

# Future Scope

The following modules are planned for future development:

- Password Manager
- URL Shortener
- REST API (Django REST Framework)

---

# License

This project is licensed under the MIT License.