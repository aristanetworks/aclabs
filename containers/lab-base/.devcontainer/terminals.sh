#!/usr/bin/env bash

# This script requires VSCode `fabiospampinato.vscode-terminals` extension
# The script will wait for docker exec to be ready before making the terminal available to user input

clear
echo 'Waiting for the lab to start...'
until docker exec -it $1 ${TERMINAL_SHELL} -c "${TERMINAL_STATUS_COMMAND} 2> /dev/null" >/dev/null 2>&1; do 
    sleep 5
done
clear
echo "$1 is ready."
# Print additional instructions for the user if env var is set
if [ "${TERMINAL_READY_MESSAGE}" ]; then
    echo ${TERMINAL_READY_MESSAGE}
fi
docker exec -it $1 ${TERMINAL_READY_COMMAND}
