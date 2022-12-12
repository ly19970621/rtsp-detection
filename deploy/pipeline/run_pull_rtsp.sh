#!/bin/bash

while true; do
	source ~/anaconda3/etc/profile.d/conda.sh
	conda activate paddle-det
	python pull_rtsp.py --config config/infer_rtsp_pphuman.yml & LASTPID=$!
	sleep 1800; kill $LASTPID
	sleep 1
done
