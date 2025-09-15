# Automated-CI-CD-Pipeline-Integration-for-a-Django-Web-Application
This project demonstrates the implementation of a complete CI/CD (Continuous Integration and Continuous Deployment) pipeline with DevSecOps practices using a simple Django-based web application. While the Django application the main focus of the project lies in automating the entire software delivery lifecycle, from code commit to cloud deployment.


# Docker Build & Push Workflow

This repository includes a **CI workflow** for building and publishing Docker images of the Django project.

##  Workflow Overview
- Triggered on **push to main branch**.  
- Builds a Docker image of the Django app.  
- Pushes the image to **Docker Hub** for deployment.  

##  Workflow Steps
1. **Checkout code** → Gets repository files.  
2. **Login to Docker Hub** → Uses stored GitHub secrets.  
3. **Build image** → Runs `docker build`.  
4. **Push image** → Uploads to Docker Hub registry.  

##  Learning Outcomes
- Automates Docker image creation.  
- Ensures reliable deployment builds.  
- Integrates with container-based environments.  

## 🖥️ Implementation
The workflow file: `.github/workflows/docker-ciImage.yml`

ct:latest
