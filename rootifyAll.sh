#!/bin/bash


for f in `ls $1/*ch[23].traces`; do
    echo "File is $f"
    FILE=$f.root     
    if [ -f $FILE ]; then
	echo "File $FILE exists."
    else
	echo "File $FILE does not exist."
	python rootify.py $f
    fi    
done


for f in `ls $1/*/*ch[23].traces`; do
    echo "File is $f"
    FILE=$f.root     
    if [ -f $FILE ]; then
	echo "File $FILE exists."
    else
	echo "File $FILE does not exist."
	python rootify.py $f
    fi    
done

for f in `ls $1/*/*/*ch[23].traces`; do
    echo "File is $f"
    FILE=$f.root     
    if [ -f $FILE ]; then
	echo "File $FILE exists."
    else
	echo "File $FILE does not exist."
	python rootify.py $f
    fi        
done
