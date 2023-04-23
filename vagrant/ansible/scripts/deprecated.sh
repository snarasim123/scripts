#!/bin/bash
echo "Updating /etc/resolv.conf"
sudo systemctl disable --now systemd-resolved.service
sudo echo "nameserver 8.8.8.8" > /etc/resolv.conf
sudo echo "options edns0" >> /etc/resolv.conf
RESOLVFILE=$(sudo cat /etc/resolv.conf)
echo "$RESOLVFILE"

echo "Installing default-java"
sudo apt-get -y install default-jre > /dev/null 2>&1
sudo apt-get -y install default-jdk > /dev/null 2>&1

