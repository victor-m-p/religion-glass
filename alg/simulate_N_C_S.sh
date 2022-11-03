#!/user/bin/env bash
for civs in 100 1000 10000
do
	for nodes in 5 10 20
	do
		for scale in 0.1 1.0 3.0
		do  
			python simulate_N_C_S.py -n $nodes -c $civs -s $scale
	 	done
	done 
done
