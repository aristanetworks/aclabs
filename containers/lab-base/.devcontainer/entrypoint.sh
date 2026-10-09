#!/usr/bin/env bash

set +e

# do not use moby script when docker is already available
# calling moby script on top of working docker deployment can break it in some cases (for ex.: Codespaces)
if ! ${CODESPACES:-false} && ! ${REMOTE_CONTAINERS:-false}; then
    /usr/local/share/docker-init.sh
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

# always prune old containers to clean the lab on laptops
${CONTAINER_ENGINE} container prune -f

if [ -z "${CEOS_IMAGE_FULLPATH}" ]; then
    CEOS_IMAGE_FULLPATH="${CONTAINERWSF}/cEOS*tar.xz"
fi
if [ -z "${CEOS_MD5_FULLPATH}" ]; then
    CEOS_MD5_FULLPATH="${CONTAINERWSF}/cEOS*tar.xz.sha512sum"
fi
# check if ceos-lab image already present
if [ -z "$(${CONTAINER_ENGINE} image ls | grep 'arista/ceos')" ]; then
    if [ "${ARISTA_TOKEN}" ]; then
        # `uname -m` is used to find platform architecture
        # currently we check for arm64 and aarch64 and expect everything else to be an x86 machine
        echo "$(uname -m)"
        if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "arm64" ]; then
            ardl get eos --format cEOSarm --version ${CEOS_LAB_VERSION} --import-docker
            ${CONTAINER_ENGINE} tag arista/ceos:${CEOS_LAB_VERSION} arista/ceos:latest
        else
            ardl get eos --format cEOS --version ${CEOS_LAB_VERSION} --import-docker
            ${CONTAINER_ENGINE} tag arista/ceos:${CEOS_LAB_VERSION} arista/ceos:latest
        fi
        # confirm that cEOS image was deleted just in case ardl failed to do that
        rm -rf ${CEOS_IMAGE_FULLPATH} >/dev/null 2>&1
        rm -rf ${CEOS_MD5_FULLPATH} >/dev/null 2>&1
    else
        # if ARISTA_TOKEN is not defined - we'll try find image in the workspace cEOS*.tar.xz
        if [ -e ${CEOS_IMAGE_FULLPATH} ]; then
            ${CONTAINER_ENGINE} import ${CEOS_IMAGE_FULLPATH} arista/ceos:latest
            rm ${CEOS_IMAGE_FULLPATH}
            # also delete SHA if it was copied, currently we do not check if archive was broken
            rm -rf ${CEOS_MD5_FULLPATH} >/dev/null 2>&1
            echo "WARNING: cEOS-lab image was successfully imported from the workspace."
        else
            echo "WARNING: arista.com token was not defined and cEOS-lab image is not present in container workspace!"
        fi 2>/dev/null
    fi
else
    echo "WARNING: cEOS-lab image already present. Skipping the image pull/download."
fi

# add aliases if any were defined
if [ -f "${CONTAINERWSF}/addAliases.sh" ]; then
    chmod +x ${CONTAINERWSF}/addAliases.sh
    ${CONTAINERWSF}/addAliases.sh
fi

# when running on Codespaces, replace any Github variables in lab files
if ${CODESPACES}; then
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
fi

if [ -f "${CONTAINERWSF}/postCreate.sh" ]; then
    chmod +x ${CONTAINERWSF}/postCreate.sh
    ${CONTAINERWSF}/postCreate.sh
    # delete postCreate.sh after use to avoid confusing lab user
    rm ${CONTAINERWSF}/postCreate.sh
fi

# init demo dir as Git repo if requested for this demo env
if ${GIT_INIT:-false}; then
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

if [ -z "${CODE_SERVER_BIND_ADDR}" ]; then
    CODE_SERVER_BIND_ADDR="0.0.0.0:8080"
fi
code-server --bind-addr ${CODE_SERVER_BIND_ADDR} --auth password --disable-telemetry --disable-update-check --disable-workspace-trust "${CONTAINERWSF}" &

# Run onboarding, deployment, and readiness checks without blocking code-server.
mkdir -p "/tmp/aclabs-lab-start"
touch "/tmp/aclabs-lab-start/startup.log"
nohup /bin/lab_start_controller.py >> "/tmp/aclabs-lab-start/startup.log" 2>&1 &

# on Codespaces this will not work correctly
if ! ${CODESPACES:-false}; then
    # Execute command from docker cli if any.
    if [ ${@+True} ]; then
        exec "$@"
    # Otherwise just enter sh or zsh.
    else
        if [ -f "/bin/zsh" ]; then
            exec zsh
        else
            exec sh
        fi
    fi
fi
