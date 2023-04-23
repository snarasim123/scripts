#!/bin/bash 
source variables.sh

echo 
echo "*** Running mongdb and mongo-express client ***"
echo 

docker-compose -f ./mongo.yml  run -d -p 27017:27017 --rm mongodb 
sleep 4
docker-compose -f ./mongo.yml  run -d -p 8081:8081 --rm mongo-express 
container_id=$(docker ps -q)
container_name=$(docker ps --format "{{.Names}}")
container_ip=$(docker inspect $container_id | grep -i "\"IPAddress")
docker ps

echo 
echo "*** Done ***"
echo 
