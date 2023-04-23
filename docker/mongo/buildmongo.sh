#!/bin/bash 
echo 
echo "***Building mongo image***"
echo 
docker-compose  -f ./mongo.yml  build
echo 
echo "***Done***"
echo 