#!/bin/bash
source variables.sh

echo 
echo "*** Deleting mongodb data files ***"
echo 

rm -rf ./mongo-data/database/*
rm -rf ./mongo-data/database/.*

echo 
echo "*** Done ***"
echo 