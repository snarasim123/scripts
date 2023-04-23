#!/bin/bash
echo "Updating /etc/resolv.conf"
sudo systemctl disable --now systemd-resolved.service
sudo echo "nameserver 8.8.8.8" > /etc/resolv.conf
sudo echo "options edns0" >> /etc/resolv.conf
RESOLVFILE=$(sudo cat /etc/resolv.conf)
echo "$RESOLVFILE"

echo "Updating apt-get"
sudo apt-get -qq update

echo "Uninstalling older versions of docker"
sudo apt-get remove docker docker-engine docker.io containerd runc

echo "Installing docker"
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu    $(lsb_release -cs)    stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

sudo service docker stop

sudo sed '/ExecStart.*/c\ExecStart=/usr/bin/docker daemon -H fd:// -H tcp://0.0.0.0:4243/' /lib/systemd/system/docker.service > /lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo service docker restart

sudo curl http://localhost:4243/version

sudo echo "export PS1='\[\e]0;\W\a\]\n\[\e[37m\]\u@\h \[\e[37m\]\W\[\e[0m\]\n\$ '" >> /home/vagrant/.profile
source /home/vagrant/.profile


