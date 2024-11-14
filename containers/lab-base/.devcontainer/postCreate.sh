#!/usr/bin/env bash

set +e

ardl get eos --image-type cEOS --version ${CEOS_LAB_VERSION} --import-docker
docker tag arista/ceos:${CEOS_LAB_VERSION} arista/ceos:latest

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