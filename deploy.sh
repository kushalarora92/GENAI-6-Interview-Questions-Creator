#!/bin/bash

IMAGE_TAG=$1

# Stop and remove the existing container if it exists
docker stop ai6-interview || true
docker rm ai6-interview || true

# Load the Docker image from the tar file
docker load < image.tar

# Ensure static directory exists with proper permissions
mkdir -p ~/static/docs
sudo chown -R 1000:1000 ~/static  # Match container's user ID
chmod -R 755 ~/static  # More secure permissions

# Run the new container
docker run -d \
  --name ai6-interview \
  --restart unless-stopped \
  -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v ~/static:/app/static \
  ai6-interview-questions:$IMAGE_TAG

# Clean up
rm image.tar 