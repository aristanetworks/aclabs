#!/usr/bin/env bash

set +e
echo "alias SPINE1='sshpass -p admin ssh -o \"StrictHostKeyChecking no\" admin@10.0.1.1'" >> ~/.zshrc
echo "alias SPINE2='sshpass -p admin ssh -o \"StrictHostKeyChecking no\" admin@10.0.1.2'" >> ~/.zshrc
echo "alias LEAF1='sshpass -p admin ssh -o \"StrictHostKeyChecking no\" admin@10.0.2.1'" >> ~/.zshrc
echo "alias Host1='sshpass -p admin ssh -o \"StrictHostKeyChecking no\" admin@10.0.2.2'" >> ~/.zshrc
echo "alias Host2='sshpass -p admin ssh -o \"StrictHostKeyChecking no\" admin@10.0.2.3'" >> ~/.zshrc