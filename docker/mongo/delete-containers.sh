#!/bin/bash
#containers_name=$(docker ps --format "{{.Names}}")
containers=$(docker ps -qa --format "{{.ID}} {{.Names}}")
stringarray=($containers)
counter=1
status=false
for i in "${stringarray[@]}";
do
    n=$(($counter % 2))
    if [[  $n -eq 0 ]]; then        
        container_name=$i
        
        status=$(docker container inspect -f "{{.State.Running}}" $container_id )
        if [[  $status == "true" ]]; then
            echo "Container $container_name $container_id is running...."
        else
            echo "Container $container_name $container_id is stopped...."
        fi

        read -p "Delete Container - $container_name $container_id ? " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
            echo "Deleting Container id - $container_id ... "
            docker stop $container_id &> /dev/null
            docker container rm $container_id &> /dev/null
            echo
        else
            echo "Skipping Container - $container_id $container_name "
            echo
        fi
    fi
    if [[  $n -ne 0 ]]; then
        container_id=$i
    fi
    let counter=counter+1
done

echo
echo "Exiting."

