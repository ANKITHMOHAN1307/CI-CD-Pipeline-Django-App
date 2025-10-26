# ⚙️ Continuous Integration Workflow (`ci.yml`)

[![CI Status](https://img.shields.io/github/actions/workflow/status/ANKITHMOHAN1307/CI-CD-Pipeline-Django-App/ci.yml?branch=docker&label=CI%20Status&style=for-the-badge&color=blue)](https://github.com/ANKITHMOHAN1307/CI-CD-Pipeline-Django-App/actions/workflows/ci.yml)

---

## 🧠 Overview
This workflow runs **automated tests**, **linting**, and **build verification** on every push or pull request to the `docker` branch.  
It ensures that your Django application is production-ready before deployment.

---

## 🚀 Workflow Purpose
- Run Django test suite automatically  
- Check code formatting and style  
- Verify build integrity before deployment  

---

## 🧱 Workflow Summary

### 📁 `.github/workflows/ci.yml`
```yaml
name: Continuous Integration

on:
  push:
    branches: [ docker ]
  pull_request:
    branches: [ docker ]

jobs:
  test:
    runs-on: ubuntu-latest
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

      - name: Run Linting
        run: ruff check .

      - name: Run Tests
        run: python manage.py test
```

---

## ✅ Key Actions

| Step                     | Description                           |
| ------------------------ | ------------------------------------- |
| **Checkout Repository**  | Fetches code for testing              |
| **Set up Python**        | Defines the Python version for build  |
| **Install Dependencies** | Installs Django and required packages |
| **Linting**              | Checks code quality using `ruff`      |
| **Run Tests**            | Executes Django's test suite          |

---

## 🧾 Outcome

* ✅ Pass → Code merges allowed
* ❌ Fail → Build stops until errors fixed

---

## 🌿 Branch
**Target Branch:** `docker`

---

## 🔗 Next Step

After CI passes, the `ciimage.yml` workflow builds the Docker image on the `newbrach-docer` branch.
