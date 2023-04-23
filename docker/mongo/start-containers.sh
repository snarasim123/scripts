#!/bin/bash
source ./variables.sh

containers=$(docker container ls -a --format "{{.ID}} {{.Image}}")
stringarray=($containers)
counter=1
for i in "${stringarray[@]}";
do
    n=$(($counter % 2))
    if [[  $n -eq 0 ]]; then        
        container_name=$i
        if [[ $container_name == *$app_name1*  ||  $container_name == *$app_name2* ]]; then
            if [ "$( docker container inspect -f '{{.State.Status}}' $container_id )" == "running" ]; 
            then 
                echo "Skipping running Container - $container_id  $container_name ... "
                echo
            else
                read -p "Start Container - $container_id $container_name? " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]
                then
                    echo "Starting Container id - $container_id  $container_name ... "
                    docker start $container_id &> /dev/null
                    echo
                else
                    echo "Skipping Container - $container_id $container_name "
                    echo
                fi
            fi
        fi
    fi
    if [[  $n -ne 0 ]]; then
        container_id=$i
    fi
    let counter=counter+1
done

echo
echo "Exiting"


