#!/bin/bash
templete_dir="templete/"
algorithms_dir="/home/zhangtao/UQ/partition_downhill_simplex/algorithms"
algorithms_method="downhill_simplex"

#create case
mkdir -p run/case$2
cp -r $algorithms_dir run/case$2/
mv $templete_dir/mpd.hosts$2 run/case$2/algorithms/$algorithms_method/mpd.host
mv $templete_dir/subrange$2  run/case$2/algorithms/$algorithms_method/subrange
cp $templete_dir/test1 run/case$2/algorithms/$algorithms_method/

#run model
cd run/case$2/algorithms/$algorithms_method
./run_downhill.sh
