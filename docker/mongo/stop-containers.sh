#!/bin/bash
source variables.sh

containers=$(docker ps --format "{{.ID}} {{.Names}}")
stringarray=($containers)
counter=1
for i in "${stringarray[@]}";
do
    n=$(($counter % 2))
    if [[  $n -eq 0 ]]; then        
        container_name=$i
        if [[ $container_name == *$app_name1*  ||  $container_name == *$app_name2* ]]; then
            read -p "Stop Container - $container_id $container_name? " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]
            then
                echo "Stopping Container id - $container_id  $container_name ... "
                docker stop $container_id  2> /dev/null
                echo
            else
                echo "Skipping Container - $container_id $container_name "
                echo
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


