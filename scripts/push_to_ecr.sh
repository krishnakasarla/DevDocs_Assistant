#!/usr/bin/env bash
set -euo pipefail

: "${ECR_REGISTRY:?Set ECR_REGISTRY, for example 123456789012.dkr.ecr.us-east-1.amazonaws.com}"
: "${AWS_REGION:?Set AWS_REGION}"

IMAGE_TAG="${1:-${IMAGE_TAG:-latest}}"
BACKEND_REPOSITORY="${BACKEND_REPOSITORY:-devdocs-backend}"
FRONTEND_REPOSITORY="${FRONTEND_REPOSITORY:-devdocs-frontend}"

aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$ECR_REGISTRY"

docker build -t "devdocs-backend:$IMAGE_TAG" backend
docker build -t "devdocs-frontend:$IMAGE_TAG" frontend

docker tag "devdocs-backend:$IMAGE_TAG" "$ECR_REGISTRY/$BACKEND_REPOSITORY:$IMAGE_TAG"
docker tag "devdocs-frontend:$IMAGE_TAG" "$ECR_REGISTRY/$FRONTEND_REPOSITORY:$IMAGE_TAG"

docker push "$ECR_REGISTRY/$BACKEND_REPOSITORY:$IMAGE_TAG"
docker push "$ECR_REGISTRY/$FRONTEND_REPOSITORY:$IMAGE_TAG"
