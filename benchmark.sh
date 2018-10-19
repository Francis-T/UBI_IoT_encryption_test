#!/bin/sh

# ENC_TYPES=(RSA FHE)
# BUF_SIZES=(1024 2048 4096 8192 16384)
# DATA_SIZES=(100 250 500 750 1000)
ENC_TYPES=(FHE)
BUF_SIZES=(4096)
DATA_SIZES=(100)

for ET in ${ENC_TYPES[@]};
do
    for BS in ${BUF_SIZES[@]};
    do
        for DS in ${DATA_SIZES[@]};
        do
            python3 node_runner.py SERVER $ET $DS $BS &
            sleep 2.0
            python3 node_runner.py CLIENT $ET $DS $BS
            
            sleep 5.0
        done;
    done;
done;


