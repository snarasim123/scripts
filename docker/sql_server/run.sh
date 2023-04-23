#!/bin/bash 
# source variables.sh

echo 
echo "*** Running docker compose to start the container ***"
echo 

docker-compose -f ./compose.yml  run -d --rm sqlserver1 
sleep 5

container_id=$(docker ps -q)
container_name=$(docker ps --format "{{.Names}}")
container_ip=$(docker inspect $container_id | grep -i "\"IPAddress")
docker ps

echo 
echo "*** Done ***"
echo 
