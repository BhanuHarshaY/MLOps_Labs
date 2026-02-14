# Docker Lab 1 - Containerizing an ML Model

## Overview

This lab demonstrates how to use Docker to containerize a machine learning training pipeline. The goal is to package a Python script that trains a Logistic Regression model on the Wine dataset into a Docker image, so it can be run consistently on any machine with Docker installed.

## Project Structure

```
docker_lab1/
├── src/
│   └── main.py        # ML training script
├── dockerfile          # Docker image definition
└── ReadMe.md           # This file
```

## What the Code Does

The `main.py` script performs the following:

1. Loads the Wine recognition dataset from scikit-learn (178 samples, 13 features, 3 classes)
2. Splits the data into 80% training and 20% testing sets
3. Trains a Logistic Regression classifier with a maximum of 200 iterations
4. Evaluates the model on the test set and prints the accuracy
5. Saves the trained model as `wine_model.pkl` using joblib

## Prerequisites

- Docker Desktop installed and running ([Download here](https://www.docker.com/products/docker-desktop/))
- Git installed
- Terminal access

You can verify Docker is installed by running:

```bash
docker --version
```

## Steps to Re-run the Lab

### 1. Clone the Repository

```bash
git clone https://github.com/BhanuHarshaY/MLOps_Labs.git
cd MLOps_Labs/docker_lab1
```

### 2. Build the Docker Image

This reads the `dockerfile`, pulls the Python 3.9 base image, installs dependencies (scikit-learn, joblib), and copies the training script into the image.

```bash
docker build -t lab1:v1 .
```

### 3. Run the Container

This starts a container from the image and executes the training script. You should see the model accuracy and a success message printed to the terminal.

```bash
docker run lab1:v1
```

Expected output:

```
Model accuracy: 0.9722
Model training was successful
```

### 4. Save the Image (Optional)

To export the Docker image as a portable tar file:

```bash
docker save lab1:v1 > my_image.tar
```

This file can be shared and loaded on another machine using `docker load < my_image.tar`.

## Dockerfile Explanation

```dockerfile
FROM python:3.9-slim       # Base image with Python 3.9
WORKDIR /app               # Set working directory inside the container
COPY src/main.py .         # Copy the training script into the container
RUN pip install scikit-learn joblib   # Install Python dependencies
CMD ["python", "main.py"]  # Default command when container starts
```

## Key Docker Commands Reference

| Command | Description |
|---|---|
| `docker build -t lab1:v1 .` | Build image from dockerfile in current directory |
| `docker run lab1:v1` | Run a container from the image |
| `docker save lab1:v1 > my_image.tar` | Export image to a tar archive |
| `docker load < my_image.tar` | Import image from a tar archive |
| `docker images` | List all local images |
| `docker ps -a` | List all containers (running and stopped) |
