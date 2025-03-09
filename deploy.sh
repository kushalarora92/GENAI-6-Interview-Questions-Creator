#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

IMAGE_NAME=$1
IMAGE_TAG=$2

echo "Deploying ${IMAGE_NAME}:${IMAGE_TAG}"

# Stop and remove the container if it exists
echo "Stopping and removing existing container with name ${IMAGE_NAME}..."
docker stop ${IMAGE_NAME} || true
docker rm ${IMAGE_NAME} || true

# Load the Docker image from the tar file
echo "Loading new image..."
docker load < image.tar

# Ensure static directory exists with proper permissions
echo "Setting up static directory..."
mkdir -p ~/static/docs
sudo chown -R 1000:1000 ~/static  # Match container's user ID
chmod -R 755 ~/static  # More secure permissions

# Run the new container
echo "Starting new container..."
docker run -d \
  --name ${IMAGE_NAME} \
  --restart unless-stopped \
  -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v ~/static:/app/static \
  ${IMAGE_NAME}:${IMAGE_TAG}

# Verify the container is running
echo "Verifying container status..."
if ! docker ps | grep -q ${IMAGE_NAME}; then
    echo "Container failed to start!"
    docker logs ${IMAGE_NAME}
    exit 1
fi

# Wait a bit and check if container is still running (in case it exits quickly)
sleep 5
if ! docker ps | grep -q ${IMAGE_NAME}; then
    echo "Container stopped shortly after starting!"
    docker logs ${IMAGE_NAME}
    exit 1
fi

# Clean up
rm image.tar

echo "Deployment complete!" 