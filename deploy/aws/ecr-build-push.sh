#!/usr/bin/env bash
set -euo pipefail

AWS_REGION="${AWS_REGION:?set AWS_REGION}"
AWS_ACCOUNT_ID="${AWS_ACCOUNT_ID:?set AWS_ACCOUNT_ID}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
REPOSITORY="${REPOSITORY:-dkg-api}"
DOCKERFILE="${DOCKERFILE:-Dockerfile}"
BUILD_CONTEXT="${BUILD_CONTEXT:-.}"
IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY}:${IMAGE_TAG}"

aws ecr describe-repositories --repository-names "${REPOSITORY}" >/dev/null 2>&1 \
  || aws ecr create-repository --repository-name "${REPOSITORY}" >/dev/null

aws ecr get-login-password --region "${AWS_REGION}" \
  | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

docker build -f "${DOCKERFILE}" -t "${IMAGE_URI}" "${BUILD_CONTEXT}"
docker push "${IMAGE_URI}"
echo "${IMAGE_URI}"
