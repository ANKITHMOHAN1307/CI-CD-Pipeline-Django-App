# 🐳 Docker Image Build Workflow (`ciimage.yml`)

[![Docker Build Status](https://img.shields.io/github/actions/workflow/status/ANKITHMOHAN1307/CI-CD-Pipeline-Django-App/ciimage.yml?branch=newbrach-docker&label=Docker%20Build&style=for-the-badge&color=blue)](https://github.com/ANKITHMOHAN1307/CI-CD-Pipeline-Django-App/actions/workflows/ciimage.yml)

---

## 🧠 Overview
This workflow automates **Docker image creation and publishing** to Docker Hub after successful CI checks.  
It ensures every commit gets a unique, traceable image for deployment.

---

## 🚀 Workflow Purpose
- Build Docker image for Django app  
- Tag image with commit SHA for version control  
- Push image to Docker Hub repository  

---

## 📁 `.github/workflows/ciimage.yml`
```yaml
name: Docker Image Build & Push

on:
  push:
    branches:
      - newbrach-docer

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Build Docker Image
        run: docker build -t ankithmohan1307/django-app:${{ github.sha }} .

      - name: Docker Login
        run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Push Image to Docker Hub
        run: docker push ankithmohan1307/django-app:${{ github.sha }}
```

---

## 🧱 Key Actions

| Step                    | Description                                        |
| ----------------------- | -------------------------------------------------- |
| **Checkout Repository** | Gets the latest code from `newbrach-docer` branch  |
| **Build Docker Image**  | Builds the container image with app code           |
| **Docker Login**        | Authenticates using GitHub Secrets                 |
| **Push Image**          | Uploads the image to Docker Hub                    |

---

## 🔐 Required Secrets

Configure these in **GitHub Repository Settings → Secrets and variables → Actions**:

- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password or access token

---

## 🧾 Outcome

* A new Docker image pushed on every commit
* Image tagged as `ankithmohan1307/django-app:<commit-sha>`
* Image ready for deployment via Railway or Azure

---

## 🌿 Branch
**Target Branch:** `newbrach-docer`

---

## 🔗 Next Step

The `ci-database.yml` workflow runs migrations and connects the app to the production database on the `database` branch.
