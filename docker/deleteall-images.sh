#!/bin/bash
# docker images  --format "{{.ID}} {{.Repository}}"
source variables.sh

echo 
echo "*** WARNING - Deleting all images.. ***"
echo 

sleep 4

docker rm $(docker ps -aq)
docker rmi $(docker images -q)

echo 
echo "*** Done ***"
echo 

