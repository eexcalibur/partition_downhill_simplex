#!/bin/bash
templete_dir="../templete/"

#create case
mkdir -p ../run/case$2
cp  $templete_dir/*  ../run/case$2

#run model
./downhill_simplex