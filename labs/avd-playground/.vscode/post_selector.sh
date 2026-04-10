#!/usr/bin/env bash

exec > /dev/null 2>&1

set +e

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
