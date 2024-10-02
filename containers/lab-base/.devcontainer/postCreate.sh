#!/usr/bin/env bash

set +e

ardl get eos --image-type cEOS --version ${CEOS_LAB_VERSION} --import-docker
docker tag arista/ceos:${CEOS_LAB_VERSION} arista/ceos:latest

# init demo dir as Git repo if requested for this demo env
if ${GIT_INIT}; then
  cd ${CONTAINERWSF}
  git init
  git config --global --add safe.directory ${PWD}
  if [ -z "$(git config user.name)" ]; then git config user.name "Lab User"; fi
  if [ -z "$(git config user.email)" ]; then git config user.email user@one-click.lab; fi
  git add .
  git commit -m "git init"
fi