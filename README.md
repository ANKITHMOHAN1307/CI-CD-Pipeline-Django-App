# 🗄️ CI Database Workflow (`ci-database.yml`)

[![Database CI Status](https://img.shields.io/github/actions/workflow/status/ANKITHMOHAN1307/CI-CD-Pipeline-Django-App/ci-database.yml?branch=database&label=Database%20CI&style=for-the-badge&color=blue)](https://github.com/ANKITHMOHAN1307/CI-CD-Pipeline-Django-App/actions/workflows/ci-database.yml)

---

## 🧠 Overview
This workflow manages **database setup, migrations, and schema updates** during the CI/CD process.  
It ensures the production database stays consistent with Django models.

---

## 🚀 Workflow Purpose
- Set up a temporary PostgreSQL or MySQL database  
- Run Django migrations automatically  
- Validate database connectivity before deployment  

---

## 📁 `.github/workflows/ci-database.yml`
```yaml
name: Database Setup and Migration

on:
  push:
    branches:
      - database
  workflow_dispatch:

jobs:
  database:
    runs-on: ubuntu-latest
    services:
      db:
        image: postgres:14
        env:
          POSTGRES_USER: django
          POSTGRES_PASSWORD: secret
          POSTGRES_DB: app_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U django"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Migrations
        env:
          DATABASE_URL: postgres://django:secret@localhost:5432/app_db
        run: python manage.py migrate
```

---

## 🧱 Key Actions

| Step                       | Description                               |
| -------------------------- | ----------------------------------------- |
| **Setup Database Service** | Starts PostgreSQL container               |
| **Checkout Repository**    | Gets the latest code from `database` branch |
| **Install Dependencies**   | Installs Django and database drivers      |
| **Run Migrations**         | Applies all migrations on the CI database |

---

## 🗄️ Database Configuration

This workflow uses **PostgreSQL 14** as a service container with:
- **User:** `django`
- **Password:** `secret`
- **Database:** `app_db`
- **Port:** `5432`

Health checks ensure the database is ready before running migrations.

---

## 🧾 Outcome

* Database schema validated before deployment
* Catches migration issues early
* Ensures production and CI databases stay in sync

---

## 🌿 Branch
**Target Branch:** `database`

---

## 🔧 Manual Trigger

This workflow can also be triggered manually using **workflow_dispatch** from the GitHub Actions tab.

---

## 🔗 Integration

Once this completes, the final deployment step (Railway or Azure) is triggered using the Docker image created by `ciimage.yml`.
