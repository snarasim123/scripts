#!/bin/bash
source variables.sh

echo 
echo 
echo "*** Deleting all mongo containers ***"
echo 
containers=$(docker ps -qa --format "{{.ID}} {{.Names}}")
stringarray=($containers)
counter=1
status=false
for i in "${stringarray[@]}";
do
    n=$(($counter % 2))
    if [[  $n -eq 0 ]]; then        
        container_name=$i
        if [[ $container_name == *$app_name* ]]; then
            echo "Deleting Container - $container_name  $container_id ... "
            docker stop $container_id &> /dev/null
            docker container rm $container_id &> /dev/null
            echo
        fi
        
    fi
    if [[  $n -ne 0 ]]; then
        container_id=$i
    fi
    let counter=counter+1
done

echo 
echo "*** Done ***"
echo 

