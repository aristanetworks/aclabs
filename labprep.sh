#! /bin/bash

echo "--> Updating CentOS System"
echo arista123 | sudo -S yum -y update

echo "--> Install Linux Packages"
echo arista123 | sudo yum install -y ca-certificates \
    curl \
    git-all \
    nano \
    python39 \
    python39-pip \
    sudo \
    vim \
    wget

echo "--> Clone Tech Library CICD Repository into the home directory"
git clone https://github.com/PacketAnglers/tech-library-cicd.git ~/tech-library-cicd

echo "--> Set Aliases for Python"
alias pip="pip3.9" \
alias pip3="pip3.9" \
alias python="python3.9"

echo "--> Install Python Modules"
pip3 install -r ~/tech-library-cicd/requirements.txt

echo "--> Install Ansible Galaxy Collections"
ansible-galaxy collection install -r ~/tech-library-cicd/requirements.yml --force