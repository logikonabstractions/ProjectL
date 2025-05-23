#!/bin/sh
# Use first argument as image tag, defaulting to "my-app"
DOCKER_TAG=${1:-my-app}
# Use second argument as target platform, defaulting to "linux/amd64"
DOCKER_DEFAULT_PLATFORM=${2:-linux/amd64}
# Build the Docker image with the given platform and tag
docker build --platform $DOCKER_DEFAULT_PLATFORM -t $DOCKER_TAG .