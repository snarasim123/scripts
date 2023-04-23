#!/bin/bash
echo
source variables.sh

containers=$(docker ps -qa --format "{{.ID}} {{.Names}}")
stringarray=($containers)
counter=1
status=false
for i in "${stringarray[@]}";
do
    n=$(($counter % 2))
    if [[  $n -eq 0 ]]; then        
        container_name=$i
        if [[ $container_name == *"$app_name2"* ]]; then
            # echo Executing - docker exec -it $container_id mongoimport --numInsertionWorkers="$num_workers" -h "$hostname"  --authenticationDatabase "$auth_db_name" -u "$user_id" -p "$passwd_str" -d "$db_name"  -c "$collection_name" --file "$src_file"
            docker exec -it $container_id mongod --nojournal &
            # docker exec -it $container_id ulimit -a
            docker exec -it $container_id mongoimport  --bypassDocumentValidation --drop --numInsertionWorkers="$num_workers" -h "$hostname"  --authenticationDatabase "$auth_db_name" -u "$user_id" -p "$passwd_str" -d "$db_name"  -c "$collection_name" --file "$src_file"
            echo
        fi
        
    fi
    if [[  $n -ne 0 ]]; then
        container_id=$i
    fi
    let counter=counter+1
done