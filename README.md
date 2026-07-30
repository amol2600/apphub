# AppHub - Expense Tracker

A modern Expense Tracker built with **Django** and **PostgreSQL** that helps users manage their personal finances with secure authentication, dashboards, charts, filtering, and printing support.

> **Status:** Production Ready (Expense Tracker Module)

---

## Features

### Authentication

- User Registration
- Email Verification
- Secure Login & Logout
- Forgot Password
- Password Reset via Email
- Django Password Validation
- User-specific Data Isolation

---

### Expense Management

- Add Transactions
- Edit Transactions
- Delete Transactions
- Add Categories
- Edit Categories
- Delete Categories
- Category-based Organization

---

### Dashboard

- Total Income
- Total Expenses
- Current Balance
- Category-wise Pie Chart

---

### Search & Filters

- Search Transactions
- Filter by Category
- Filter by Transaction Type

---

### Printing

- Print-Friendly Transaction List
- Automatic Removal of Navigation and Action Buttons
- Optimized Print Styling

---

### Security

- Password Validation
- Email Verification
- CSRF Protection
- Session Authentication
- User Data Isolation

---

## Tech Stack

### Backend

- Django 6
- Python

### Database

- PostgreSQL (NeonDB)

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Email

- Gmail SMTP

### Deployment

- Render

---

## Project Structure

```
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

## Installation

Clone the repository

```bash
https://github.com/amol2600/apphub.git
```

Go into the project

```bash
cd <repository-name>
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

DEFAULT_FROM_EMAIL=your_email@gmail.com
```

---

## Database

Run migrations

```bash
python manage.py migrate
```

Create a superuser

```bash
python manage.py createsuperuser
```

Start the server

```bash
python manage.py runserver
```

---

## Deployment

This project is configured for deployment on **Render** using:

- Gunicorn
- WhiteNoise
- PostgreSQL (NeonDB)

---

## Future Scope

The following modules are planned for future development:

- Password Manager
- URL Shortener
- REST API (Django REST Framework)

---

## License

This project is licensed under the MIT License.

