#!/bin/bash
templete_dir="../templete/"

#create case
mkdir -p ../run/case$2
cp  $templete_dir/*  ../run/case$2


#run model
cd ../run/case$2/
./downhill_simplex