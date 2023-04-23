images=$(docker images --filter "reference=$app_name1*"  --format "{{.ID}} {{.Repository}}")
stringarray=($images)
counter=1
for i in "${stringarray[@]}";
do
    n=$(($counter % 2))
    if [[  $n -eq 0 ]]; then        
        image_name=$i
        # if [[ $image_name == *$app_name1*  ||  $image_name == *$app_name2* ]]; then
            read -p "Delete image - $image_id $image_name? " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]
            then
                echo "Deleting image  - $image_id  $image_name ... "
                docker rmi $image_id  2> /dev/null
                echo
            else
                echo "Skipping image - $image_id $image_name "
                echo
            fi
        # fi
    fi
    if [[  $n -ne 0 ]]; then
        image_id=$i
    fi
    let counter=counter+1
done

echo
echo "Exiting."












