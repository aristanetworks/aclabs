#!/bin/bash
useradd -m -s /bin/bash cvpadmin
echo "cvpadmin:arista123" | chpasswd
usermod -aG sudo cvpadmin