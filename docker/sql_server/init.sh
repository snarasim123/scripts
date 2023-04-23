#!/bin/bash
source variables.sh

echo
read -p "Deleting all Containers/Images/Db files - Continue ? " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        ./deleteall-containers.sh
        ./deleteall-images.sh
        ./deleteall-dbfiles.sh
        ./buildmongo.sh
    fi
