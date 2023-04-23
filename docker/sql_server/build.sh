#!/bin/bash 
echo 
echo "***Building mongo image***"
echo 
docker-compose  -f ./compose.yml  build
echo 
echo "***Done***"
echo 