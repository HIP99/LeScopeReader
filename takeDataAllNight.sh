##!/bin/bash

export FOLDER=/unix/dune/purity/2018September14Vacumm/NewLampPosition/Silver/
export FIELD=Field_-20.20

mkdir -p $FOLDER 

for iruns in `seq 1 50`; do
    name=$(date +%H.%M )
    echo RUN IS $iruns and $name
    python ./fetch_fast.py ${FOLDER}/${FIELD}_FibreIn_${name} -n 1000 -s 100
    sleep 1800
done

echo "DONE !"