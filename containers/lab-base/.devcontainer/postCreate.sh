#!/usr/bin/env bash

set +e

# replace all markdown vars in demo directory
if [ "${GITHUB_REPOSITORY}" ]; then
  grep -rl '{{gh.repo_name}}' . --exclude-dir .git | xargs sed -i 's/{{gh.repo_name}}/'"${GITHUB_REPOSITORY##*/}"'/g'
  grep -rl '{{gh.org_name}}' . --exclude-dir .git | xargs sed -i 's/{{gh.org_name}}/'"${GITHUB_REPOSITORY%%/*}"'/g'
  grep -rl '{{gh.repository}}' . --exclude-dir .git | xargs sed -i 's@{{gh.repository}}@'"${GITHUB_REPOSITORY}"'@g'
else
  # if not running on Codespaces and GITHUB_REPOSITORY is not set - set aristanetworks/acLabs by default
  grep -rl '{{gh.repo_name}}' . --exclude-dir .git | xargs sed -i 's/{{gh.repo_name}}/'"acLabs"'/g'
  grep -rl '{{gh.org_name}}' . --exclude-dir .git | xargs sed -i 's/{{gh.org_name}}/'"aristanetworks"'/g'
  grep -rl '{{gh.repository}}' . --exclude-dir .git | xargs sed -i 's@{{gh.repository}}@'"aristanetworks/acLabs"'@g'
fi
# update URL in clab init configs if set
if [ "${CVURL}" ]; then
  grep -rl '{{cv_url}}' . --exclude-dir .git | xargs sed -i 's@{{cv_url}}@'"${CVURL}"'@g'
  # check for legacy labs using hardcoded URL
  grep -rl 'cv-staging.corp.arista.io' . --exclude-dir .git | xargs sed -i 's@cv-staging.corp.arista.io@'"${CVURL}"'@g'
else
  # set defaul url to staging if nothing is defined
  grep -rl '{{cv_url}}' . --exclude-dir .git | xargs sed -i 's@{{cv_url}}@'"cv-staging.corp.arista.io"'@g'
fi

# for D-in-D case container engine will be always Docker
# however we do not want to hardcode it for future cases
if [ "$(command -v podman)" ]; then
    CONTAINER_ENGINE="podman"
elif [ "$(command -v docker)" ]; then
    CONTAINER_ENGINE="docker"
else
    echo "ERROR: Failed to find container engine. Please install docker or podman." >&2
    exit 1
fi

# always prune old containers a clean lab on laptops
${CONTAINER_ENGINE} container prune -f

# check if ceos-lab image already present
if [ -z "$(${CONTAINER_ENGINE} image ls | grep 'arista/ceos')" ]; then
    if [ "${ARISTA_TOKEN}" ]; then
        # `uname -m` is used to find platform architecture
        # currently we check for arm64 and aarch64 and expect everything else to be an x86 machine
        echo "$(uname -m)"
        if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "arm64" ]; then
            ardl get eos --image-type cEOSarm --version ${CEOS_LAB_VERSION} --import-docker
            ${CONTAINER_ENGINE} tag arista/ceos:${CEOS_LAB_VERSION} arista/ceos:latest
        else
            ardl get eos --image-type cEOS --version ${CEOS_LAB_VERSION} --import-docker
            ${CONTAINER_ENGINE} tag arista/ceos:${CEOS_LAB_VERSION} arista/ceos:latest
        fi
    else
        # if ARISTA_TOKEN is not defined - we'll try to pull it from a private container registry
        if docker pull arista/ceos:${CEOS_LAB_VERSION} >/dev/null 2>&1; then
            echo "WARNING: pulled cEOS-lab image from the private container registry successfully."
        else
            echo "WARNING: arista.com token was not defined and image is not available on the private registry!"
        fi
    fi
else
    echo "WARNING: cEOS-lab image already present. Skipping the image pull/download."
fi

# check if image is still missing and print a warning
if [ -z "$(${CONTAINER_ENGINE} image ls | grep 'arista/ceos')" ]; then
    echo "WARNING: cEOS-lab image download failed. Try to upload and import it manually."
    echo "         Please make sure that image is imported with a correct name - arista/ceos:latest"
    echo "         The lab will not auto start! Run 'make start' when image is ready."
else
    make start
fi

if [ "${CV_API_TOKEN}" ]; then
  if [ "${CVURL}" ]; then
    CVTOKEN=$(curl -H "Authorization: Bearer ${CV_API_TOKEN}" "https://www.${CVURL}/api/v3/services/admin.Enrollment/AddEnrollmentToken" -d '{"enrollmentToken":{"reenrollDevices":["*"],"validFor":"24h"}}' | sed -n 's|.*"token":"\([^"]*\)".*|\1|p')
  else
    CVTOKEN=$(curl -H "Authorization: Bearer ${CV_API_TOKEN}" "https://www.cv-staging.corp.arista.io/api/v3/services/admin.Enrollment/AddEnrollmentToken" -d '{"enrollmentToken":{"reenrollDevices":["*"],"validFor":"24h"}}' | sed -n 's|.*"token":"\([^"]*\)".*|\1|p')
  fi
  echo "$CVTOKEN" > ${CONTAINERWSF}/clab/cv-onboarding-token
fi

if [ -f "${CONTAINERWSF}/postCreate.sh" ]; then
  chmod +x ${CONTAINERWSF}/postCreate.sh
  ${CONTAINERWSF}/postCreate.sh
  # delete postCreate.sh after use to avoid confusing lab user
  rm ${CONTAINERWSF}/postCreate.sh
fi

# init demo dir as Git repo if requested for this demo env
if ${GIT_INIT}; then
  cd ${CONTAINERWSF}
  # if not a git repo already - init
  if [ -z "$(git status 2>/dev/null)" ]; then
    git init
    git config --global --add safe.directory ${PWD}
    if [ -z "$(git config user.name)" ]; then git config user.name "Lab User"; fi
    if [ -z "$(git config user.email)" ]; then git config user.email user@one-click.lab; fi
    git add .
    git commit -m "git init"
  fi
fi
