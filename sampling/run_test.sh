#!/bin/bash

#./test1 0.840188 0.394383 0.783099 0.798440 0.911647
#./test1 0.840181 0.394381 0.783091 0.798449 0.911641
echo $1

v1=`sed -n "2p" $1`
v2=`sed -n "3p" $1`
v3=`sed -n "4p" $1`
v4=`sed -n "5p" $1`
v5=`sed -n "6p" $1`

./test1 $v1 $v2 $v3 $v4 $v5
touch $2

cat res_data  > $2
