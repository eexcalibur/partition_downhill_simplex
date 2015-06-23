#!/bin/bash
paras="hkconv_c0:hkconv_cmftau:cldfrc_rhminh:cldfrc_rhminl:cldsed_ai"
pwd_dir="/home/CSM-tunner/UQ/CAPT/llnl_capt/uq_calibrator/"
case_path="/share1/CSM-tunner/cesm.run/capt_cam5_tune/cesm_case$2"
metrics_path="$case_path/metrics"

#run
mv  $pwd_dir/mpd.hosts$2 $case_path/mpd.hosts
cd  $case_path
paras_num=`echo $paras | awk -F ':' '{print NF}'`
for i in `seq 1 $paras_num`
do
	para=`echo $paras |cut -d : -f $i`
	var_line=`cat $case_path/parameters`
    para_val="$para=`echo $var_line |cut -d ' ' -f $i`"
    #echo $para_val
    sed -i "/\<$para\>/c \\  $para_val" $case_path/atm_in
done
echo `date`: "configure case [EXP_notracer_$2] successfully"
pwd
./run_cesm.sh > output

#diag
cd $metrics_path
./get_metrics.csh > metrics.log
