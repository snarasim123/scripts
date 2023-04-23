#!/bin/bash

echo "Updating apt-get"
sudo apt-get -qq update

echo "Setting up docker compose"
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

echo "Writing docker-compose.yml"
sudo echo "version: '3.3' " > /home/vagrant/docker-compose.yml
sudo echo "services:" >> /home/vagrant/docker-compose.yml
sudo echo "  db:" >> /home/vagrant/docker-compose.yml
sudo echo "    image: mysql:5.7" >> /home/vagrant/docker-compose.yml
sudo echo "    volumes:" >> /home/vagrant/docker-compose.yml
sudo echo "      - db_data:/var/lib/mysql" >> /home/vagrant/docker-compose.yml
sudo echo "    ports:" >> /home/vagrant/docker-compose.yml
sudo echo "      - \"3306:3306\" " >> /home/vagrant/docker-compose.yml
sudo echo "    restart: always" >> /home/vagrant/docker-compose.yml
sudo echo "    environment:" >> /home/vagrant/docker-compose.yml
sudo echo "      MYSQL_ROOT_PASSWORD: somewordpress" >> /home/vagrant/docker-compose.yml
sudo echo "      MYSQL_DATABASE: wordpress" >> /home/vagrant/docker-compose.yml
sudo echo "      MYSQL_USER: wordpress" >> /home/vagrant/docker-compose.yml
sudo echo "      MYSQL_PASSWORD: wordpress" >> /home/vagrant/docker-compose.yml
sudo echo "   " >> /home/vagrant/docker-compose.yml
sudo echo "  wordpress:" >> /home/vagrant/docker-compose.yml
sudo echo "    depends_on:" >> /home/vagrant/docker-compose.yml
sudo echo "      - db" >> /home/vagrant/docker-compose.yml
sudo echo "    image: wordpress:latest" >> /home/vagrant/docker-compose.yml
sudo echo "    ports:" >> /home/vagrant/docker-compose.yml
sudo echo "      - \"8000:80\"" >> /home/vagrant/docker-compose.yml
sudo echo "    restart: always" >> /home/vagrant/docker-compose.yml
sudo echo "    environment:" >> /home/vagrant/docker-compose.yml
sudo echo "      WORDPRESS_DB_HOST: db:3306" >> /home/vagrant/docker-compose.yml
sudo echo "      WORDPRESS_DB_USER: wordpress" >> /home/vagrant/docker-compose.yml
sudo echo "      WORDPRESS_DB_PASSWORD: wordpress" >> /home/vagrant/docker-compose.yml
sudo echo "      WORDPRESS_DB_NAME: wordpress" >> /home/vagrant/docker-compose.yml

sudo echo "volumes:" >> /home/vagrant/docker-compose.yml
sudo echo "  db_data: {}" >> /home/vagrant/docker-compose.yml
  
echo "Spinning mysql docker container..."
sudo docker-compose up -d

sudo echo "export PS1='\[\e]0;\W\a\]\n\[\e[37m\]\u@\h \[\e[37m\]\W\[\e[0m\]\n\$ '" >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc

sudo echo "export PS1='\[\e]0;\W\a\]\n\[\e[37m\]\u@\h \[\e[37m\]\W\[\e[0m\]\n\$ '" >> /home/vagrant/.profile
source /home/vagrant/.profile



