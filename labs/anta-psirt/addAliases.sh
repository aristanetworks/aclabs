#!/usr/bin/env bash

set +e

echo "alias eos1='sshpass -p ${LABPASSPHRASE} ssh -o \"StrictHostKeyChecking no\" ${LABUSERNAME}@172.100.100.11'" >> ~/.zshrc
echo "alias eos2='sshpass -p ${LABPASSPHRASE} ssh -o \"StrictHostKeyChecking no\" ${LABUSERNAME}@172.100.100.12'" >> ~/.zshrc
echo "alias eos3='sshpass -p ${LABPASSPHRASE} ssh -o \"StrictHostKeyChecking no\" ${LABUSERNAME}@172.100.100.13'" >> ~/.zshrc
echo "alias eos4='sshpass -p ${LABPASSPHRASE} ssh -o \"StrictHostKeyChecking no\" ${LABUSERNAME}@172.100.100.14'" >> ~/.zshrc
