#!/bin/bash

basename=$1
ntot=10000
sequence=50
THRESHOLDS="10 15 20 25"
CHANNELS="2 3"
div=20

if [ $# -eq 0 ]
  then
    echo "Input: folder where you want to save data"
    exit
fi

for ch in `echo $CHANNELS`;
do
    for thres in `echo $THRESHOLDS`;
    do
	outputname=${basename}/TrigCh${ch}_thres${thres}mV_${div}mVdiv
	thisthres=$(echo $thres*-0.001 | bc)
	thisdiv=$(echo $div*0.001 | bc)
	echo $outputname -n $ntot -s $sequence -c $ch -t $thisthres
	python ./fetch_fast.py $outputname -n $ntot -s $sequence -c $ch -t $thisthres -d $thisdiv
	done
done