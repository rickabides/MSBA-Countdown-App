#!/bin/bash
# Set Image name. Assumes Google Cloud container app has been create ahead of time
IMAGE="gcr.io/project-123456/countdown"

# Set Google Cloud Region
REGION="us-west1"

# Build the Docker image and tag it
docker build -t countdown . && echo "Docker build successful." || { echo "Docker build failed."; exit 1; }

# Submit the Docker image to Google Cloud Build
gcloud builds submit --tag ${IMAGE} && echo "Cloud build successful." || { echo "Cloud build failed."; exit 1; }

# Deploy the Docker image on Google Cloud Run specifying the region
gcloud run deploy countdown --image ${IMAGE} --region ${REGION} --allow-unauthenticated && echo "Deployment successful." || { echo "Deployment failed."; exit 1; }

echo "All operations completed successfully."
