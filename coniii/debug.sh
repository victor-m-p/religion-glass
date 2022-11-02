#!/user/bin/env bash

for x in $(seq 0 0.0001 0.005)
do
	python debugging.py -f $x
done
