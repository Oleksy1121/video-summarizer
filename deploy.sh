#!/bin/bash
set -e
source .env

PROJECT_ID="ml-portfolio-xyz123"
REGION="europe-west4"
IMAGE="europe-west4-docker.pkg.dev/${PROJECT_ID}/ml-portfolio-app/video-summarizer-backend:latest"

echo "Building Docker image..."
docker build -t $IMAGE .

echo "Pushing to Artifact Registry..."
docker push $IMAGE

echo "Deploying to Cloud Run..."
gcloud run deploy video-summarizer-backend \
  --image=$IMAGE \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY

echo "Done!"