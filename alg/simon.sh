#!/user/bin/env bash
for samples in 100 1000 10000
do
	for nodes in 5 10 20
	do 
		python simon_samples.py -n $nodes -s $samples
	done 
done
