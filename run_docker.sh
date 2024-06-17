#!/bin/bash

# Build the Docker image
docker build -t my-app .

# Run the Docker container
docker run -p 8501:8501 my-app
