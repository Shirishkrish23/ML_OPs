# Movie Rating Prediction API

## Overview

This project provides a Flask-based API for predicting movie ratings using a pre-trained RandomForest model. The application is containerized using Docker and orchestrated with Docker Compose. Continuous Integration and Continuous Deployment (CI/CD) are managed through GitHub Actions, ensuring automated testing, building, and deployment. Monitoring is set up using Prometheus and Grafana.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [CI/CD Pipeline](#cicd-pipeline)
- [Automated Retraining](#automated-retraining)
- [Monitoring](#monitoring)
- [Project Structure](#project-structure)

## Prerequisites

- Docker and Docker Compose installed on your local machine.
- GitHub repository with the provided codebase.
- Docker Hub account.
- Virtual Machine (VM) with SSH access for deployment.
- GitHub Secrets configured:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`
  - `VM_IP_ADDRESS`
  - `VM_USERNAME`
  - `SSH_PRIVATE_KEY`

## Setup and Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/shirishkrish23/ML_OPs.git
    cd ML_OPs
    ```

2. **Configure Git LFS**
    ```bash
    git lfs install
    git lfs pull
    ```

3. **Build Docker Images**
    ```bash
    docker-compose build
    ```

4. **Run Docker Containers**
    ```bash
    docker-compose up -d
    ```

## Running the Application

The Flask API will be accessible at `http://localhost:5000/`. You can interact with the API endpoints as follows:

- **Home Endpoint**
    ```
    GET /
    Response: "Movie Rating Prediction API is running!"
    ```

- **Predict Rating**
    ```
    POST /predict
    Body: {
        "user_id": <int>,
        "movie_id": <int>
    }
    Response: {
        "prediction": <predicted_rating>
    }
    ```

## CI/CD Pipeline

The CI/CD pipeline is configured using GitHub Actions and is defined in `.github/workflows/ci-cd.yml`. The pipeline includes the following steps:

1. **Checkout Code with LFS Support**
2. **Set Up Python Environment**
3. **Install Dependencies**
4. **Run Unit Tests**
5. **Build Docker Image**
6. **Push Docker Image to Docker Hub**
7. **Deploy to VM using Docker Compose**

**Trigger Events:**
- Push to `main` branch
- Pull requests to `main` branch
- Scheduled daily at midnight

## Automated Retraining

An additional job in the CI/CD pipeline handles automated retraining of the model:

1. **Triggered Daily via Cron Schedule**
2. **Checkout Code with LFS Support**
3. **Set Up Python Environment**
4. **Install Dependencies**
5. **Run Retraining Script (`retrain.py`)**
6. **Commit and Push Updated Model Files (`.pkl`)**
7. **Build and Push Updated Docker Image**
8. **Deploy Updated Model to VM**

**Note:** Retraining only occurs if triggered by the scheduled event.

## Monitoring

Monitoring is set up using Prometheus and Grafana:

- **Prometheus** scrapes metrics from the Flask application exposed at `/metrics`.
- **Grafana** visualizes the metrics collected by Prometheus.

**Access Points:**
- Prometheus: `http://localhost:9090/`
- Grafana: `http://localhost:3000/` (Default login: `admin` / `YourSecurePassword`)
- 
## Usage

- **API Interaction:** Use tools like `curl` or Postman to interact with the API endpoints.
- **Running Tests:** Execute `pytest` to run unit tests.
- **Monitoring Metrics:** Access Prometheus and Grafana dashboards to monitor application performance and metrics.
- **Automated Deployment:** Commit and push changes to the `main` branch to trigger the CI/CD pipeline for automated testing, building, and deployment.

## License
NULL

## Project Structure
```plaintext
ML_OPs/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── models/
│   │   ├── optimized_movie_rating_model.pkl
│   │   └── title_encoder.pkl
│   └── utils/
│       └── data_loader.py
├── tests/
│   └── test_app.py
├── scripts/
│   └── retrain.py
├── notebooks/
│   └── Model_movies.ipynb
├── data/
│   ├── u.data
│   └── u.item
├── config/
│   └── prometheus.yml
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .gitattributes
├── requirements.txt
└── README.md



