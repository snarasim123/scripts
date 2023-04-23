#!/bin/bash
echo "Updating /etc/resolv.conf"
sudo systemctl disable --now systemd-resolved.service
sudo echo "nameserver 8.8.8.8" > /etc/resolv.conf
sudo echo "options edns0" >> /etc/resolv.conf
RESOLVFILE=$(sudo cat /etc/resolv.conf)
echo "$RESOLVFILE"

echo "Adding apt-keys"
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -
echo deb http://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list

echo "Updating apt-get"
sudo apt-get -qq update

echo "Installing default-java"
sudo apt-get -y install default-jre > /dev/null 2>&1
sudo apt-get -y install default-jdk > /dev/null 2>&1

echo "Installing git"
sudo apt-get -y install git > /dev/null 2>&1

echo "Installing maven"
sudo apt-get -y install maven > /dev/null 2>&1

echo "Installing git-ftp"
sudo apt-get -y install git-ftp > /dev/null 2>&1

echo "Installing jenkins"
sudo apt-get -y install jenkins > /dev/null 2>&1
sudo service jenkins start

echo "Generating ssh keys"
sudo -u jenkins ssh-keygen -t rsa -f /var/lib/jenkins/.ssh/id_rsa -q -P "" 

sudo echo "export PS1='\[\e]0;\W\a\]\n\[\e[37m\]\u@\h \[\e[37m\]\W\[\e[0m\]\n\$ '" >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc

sudo echo "export PS1='\[\e]0;\W\a\]\n\[\e[37m\]\u@\h \[\e[37m\]\W\[\e[0m\]\n\$ '" >> /home/vagrant/.profile
source /home/vagrant/.profile

#python 2.7

# pip install pyodbc==4.0.26
# pip install python-dateutil==2.8.1
# pip install pandas==0.24.2
# pip install gnupg==2.3.1
# pip install paramiko==2.4.2
# pip install python-json-logger==0.1.11
# pip install pymongo==3.7.2
# pip install simple-salesforce==0.74.2

# isql -v -k "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DWHSQL001;DATABASE=Load_Audit;UID=batch_etl;PWD=Awesum4@llppl"

# copy the following 3 lines into a file called testodbc.py
# import pyodbc
# connectString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ 'DWHSQL001' +';DATABASE='+ 'Load_Audit' +';UID='+ 'batch_etl' +';PWD='+ 'Awesum4@llppl;'
# defaultConn = pyodbc.connect(connectString, autocommit=True)
#
# test above file by calling python testodbc.py
# make sure no errors are printed
# 
# copy dp_config.py
#
# create dp.log, set permissions to be written by any user.
#

echo "Getting jenkins initAdminPassword"
JENKINSPWD=$(sudo cat /var/lib/jenkins/secrets/initialAdminPassword)
echo "*** initAdminPassword  $JENKINSPWD"


