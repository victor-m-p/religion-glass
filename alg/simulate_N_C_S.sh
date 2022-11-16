#!/user/bin/env bash
for civs in 100 
do
	for nodes in 3 5
	do
		for scale in 0.1 1.0 
		do  
			python simulate_N_C_S.py -n $nodes -c $civs -s $scale
	 	done
	done 
done
