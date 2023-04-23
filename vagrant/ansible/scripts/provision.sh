#!/bin/bash

# ANSIBLE_DIR="/home/vagrant/ansible" 
# ANSIBLE_HOSTS="/vagranthost"
# ANSIBLE_PLAYBOOK_DIR="/home/vagrant/ansible-playbooks" 
# HOSTS_LOCATION_ON_VM="/home/vagrant/ansible_hosts"

# mkdir ${HOSTS_LOCATION_ON_VM} && chown vagrant:vagrant ${HOSTS_LOCATION_ON_VM}
# cp /tmp/${ANSIBLE_HOSTS} ${HOSTS_LOCATION_ON_VM} && chmod -x ${HOSTS_LOCATION_ON_VM}

echo "Installing Git Maven "
apt-get update
apt-get install -y git maven python-yaml python-paramiko python-jinja2



# echo "Installing Ansible on guest VM"
# touch /home/vagrant/.bashrc
# echo "source $ANSIBLE_DIR/hacking/env-setup" >> /home/vagrant/.bashrc
# echo "export ANSIBLE_HOSTS=${HOSTS_LOCATION_ON_VM}" >> /home/vagrant/.bashrc

#echo "Downloading Ansible Playbooks to ${ANSIBLE_PLAYBOOK_DIR}"
#git clone https://3182c0cbb8b1f7e80e39ba605a8e597aa3a6dc05@github.com/snarasim123/ansible-playbooks.git ${ANSIBLE_PLAYBOOK_DIR} 
  echo "Removing old jdk/jre  "
  sudo apt-get -y --purge remove openjdk-8-jdk
  sudo apt-get -y --purge remove openjdk-8-jdk-headless
  # sudo apt-get -y --purge remove openjdk-11-jdk
  # sudo apt-get -y --purge remove openjdk-11-jdk-headless
  # sudo apt-get -y --purge remove openjdk-11-jre
  # sudo apt-get -y --purge remove openjdk-11-jre-headless                                 
  sudo apt-get -y --purge remove openjdk-8-jre
  sudo apt-get -y --purge remove openjdk-8-jre-headless
  

# echo "Cloning Ansible"
# mkdir -p ${ANSIBLE_DIR}
# git clone git://github.com/ansible/ansible.git ${ANSIBLE_DIR} 
# # First checkout v1.6.6
# #cd ${ANSIBLE_DIR}
# #git checkout tags/v1.6.6
# cd ${ANSIBLE_DIR}
# git checkout tags/v2.5.0

sudo echo "export PS1='\[\e]0;\W\a\]\n\[\e[37m\]\u@\h \[\e[37m\]\W\[\e[0m\]\n\$ '" >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc

sudo echo "export PS1='\[\e]0;\W\a\]\n\[\e[37m\]\u@\h \[\e[37m\]\W\[\e[0m\]\n\$ '" >> /home/vagrant/.profile
source /home/vagrant/.profile

echo "provision.sh done."
