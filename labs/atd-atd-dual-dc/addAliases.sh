#!/usr/bin/env bash

set +e
echo "alias s1-spine1='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.10'" >> ~/.zshrc
echo "alias s1-spine2='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.11'" >> ~/.zshrc
echo "alias s1-leaf1='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.12'" >> ~/.zshrc
echo "alias s1-leaf2='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.13'" >> ~/.zshrc
echo "alias s1-leaf3='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.14'" >> ~/.zshrc
echo "alias s1-leaf4='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.15'" >> ~/.zshrc
echo "alias s1-brdr1='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.100'" >> ~/.zshrc
echo "alias s1-brdr2='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.101'" >> ~/.zshrc
echo "alias s2-spine1='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.20'" >> ~/.zshrc
echo "alias s2-spine2='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.21'" >> ~/.zshrc
echo "alias s2-leaf1='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.22'" >> ~/.zshrc
echo "alias s2-leaf2='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.23'" >> ~/.zshrc
echo "alias s2-leaf3='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.24'" >> ~/.zshrc
echo "alias s2-leaf4='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.25'" >> ~/.zshrc
echo "alias s2-brdr1='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.200'" >> ~/.zshrc
echo "alias s2-brdr2='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.201'" >> ~/.zshrc
echo "alias s1-host1='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.16'" >> ~/.zshrc
echo "alias s1-host2='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.17'" >> ~/.zshrc
echo "alias s2-host1='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.26'" >> ~/.zshrc
echo "alias s2-host2='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@192.168.0.27'" >> ~/.zshrc