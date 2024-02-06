#! /bin/bash

echo "--> Updating CentOS System"
echo arista123 | sudo -S yum -y update

echo "--> Disable SELinux"
echo arista123 | sudo setenforce 0

echo arista123 | sudo yum install -y ca-certificates \
    curl \
    git-all \
    make \
    nano \
    python39 \
    python39-pip \
    sudo \
    vim \
    wget

alias pip="pip3.9" \
alias pip3="pip3.9" \
alias python="python3.9"

echo "check python version"
python --version

echo "install ansible core"
pip3.9 install ansible-core>=2.16.3

echo "install avd ansible collection"
ansible-galaxy collection install arista.avd --upgrade

echo "install avd ansible requirements"
pip3.9 install -r ~/.ansible/collections/ansible_collections/arista/avd/requirements.txt
