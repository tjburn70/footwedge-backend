#! /usr/bin/env bash

set -e pipefail

PORT=8002
CONTAINER_NAME="search-service-api"
IMAGE_NAME="tjburn70/search-service-api:latest"

main() {
  docker container run -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}
}

main