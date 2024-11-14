#!/usr/bin/env bash

set +e

# replace all markdown vars in demo directory
grep -rl '{{gh.repo_name}}' . --exclude-dir .git | xargs sed -i 's/{{gh.repo_name}}/'"${GITHUB_REPOSITORY##*/}"'/g'
grep -rl '{{gh.org_name}}' . --exclude-dir .git | xargs sed -i 's/{{gh.org_name}}/'"${GITHUB_REPOSITORY%%/*}"'/g'
grep -rl '{{gh.repository}}' . --exclude-dir .git | xargs sed -i 's@{{gh.repository}}@'"${GITHUB_REPOSITORY}"'@g'
# update URL in clab init configs if set
if [ "${CVURL}" ]; then
  grep -rl '{{cv_url}}' . --exclude-dir .git | xargs sed -i 's@{{cv_url}}@'"${CVURL}"'@g'
  # check for legacy labs using hardcoded URL
  grep -rl 'cv-staging.corp.arista.io' . --exclude-dir .git | xargs sed -i 's@cv-staging.corp.arista.io@'"${CVURL}"'@g'
else
  # set defaul url to staging if nothing is defined
  grep -rl '{{cv_url}}' . --exclude-dir .git | xargs sed -i 's@{{cv_url}}@'"cv-staging.corp.arista.io"'@g'
fi

ardl get eos --image-type cEOS --version ${CEOS_LAB_VERSION} --import-docker
docker tag arista/ceos:${CEOS_LAB_VERSION} arista/ceos:latest

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
  # delet postCreate.sh after use to avoid confusing lab user
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