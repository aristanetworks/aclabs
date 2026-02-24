#!/usr/bin/env bash

set +e
echo "alias spine1='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@172.144.100.2'" >> ~/.zshrc
echo "alias spine2='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@172.144.100.3'" >> ~/.zshrc
echo "alias pe11='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@172.144.100.4'" >> ~/.zshrc
echo "alias pe12='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@172.144.100.5'" >> ~/.zshrc
echo "alias pe21='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@172.144.100.6'" >> ~/.zshrc
echo "alias pe22='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@172.144.100.7'" >> ~/.zshrc
echo "alias client1='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@172.144.100.8'" >> ~/.zshrc
echo "alias client2='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@172.144.100.9'" >> ~/.zshrc
echo "alias client3='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@172.144.100.10'" >> ~/.zshrc
echo "alias client4='sshpass -p arista ssh -o \"StrictHostKeyChecking no\" arista@172.144.100.11'" >> ~/.zshrc