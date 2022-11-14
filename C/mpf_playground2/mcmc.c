#include "mpf.h"
#include "stdlib.h"
#define flip(X)  ((X) < 0 ? 1 : -1)

void mcmc_sampler(samples *data, int loc, int iter) {
	int i, j, pos, count, *config; // 
	double running, exp_running; // 
	
	config=data->obs[loc]; // pointer to a row of nodes (observations)
	// printf("config = %d\n", *config); // 1, -1
	//printf("*config: %d\n", *config);
	//printf("config 1: %d\n", config[1]);
	//printf("config 2: %d\n", config[2]);
	for(i=0;i<iter;i++) { // loop over each iteration
		pos=(int)gsl_rng_uniform_int(data->r, data->n); // pick a point randomly (node)

		//if(i==10){
			//printf("pos 10 = %d\n", pos);
			//printf("config[pos] for pos = 10: %d\n", config[pos]); // -1, 1 
		//}

		running=0;
		//printf("pos = %d\n", pos);
		// change in energy function from the proposed flip
		// the loop deals with the coupling Jij
		for(j=0;j<data->n;j++) { // loop over n 
			if (pos != j) {
				//printf("j = %d\n", j);
				//printf("config[pos] = %d\n", config[pos]);
				//printf("flip(config[pos]) = %d\n", flip(config[pos]));
				//printf("config[pos] - flip(config[pos]) = %d\n", config[pos] - flip(config[pos]));
				running += (config[pos] - flip(config[pos]))*config[j]*data->big_list[data->ij[pos][j]];
				// (-2, 2) * (1, -1) * (parameter) 
			}
		}
		// this part deals with the h. 
		running += (config[pos] - flip(config[pos]))*data->big_list[data->h_offset+pos]; 
		// (-2, 2) * (parameter)
		
		running = -1*running; // oops, i meant to get the other ratio; log P(xnew)/P(x)
		
		//printf("running: %f\n", running);
		exp_running=exp(running); 
		//printf("exp running: %f\n", exp_running);
		//printf("exp running/(1+exp_running): %f\n", exp_running/(1+exp_running));
		if (gsl_rng_uniform(data->r) < exp_running/(1+exp_running)) { // glauber %
			//printf("i = %d\n", i);
			//printf("obs[loc][pos] (before) = %d\n", data->obs[loc][pos]);
			//printf("config[pos] (before) = %d\n", config[pos]);
			config[pos]=flip(config[pos]);
			//printf("config[pos] (after) = %d\n", config[pos]);
			//printf("obs[loc][pos] (after): %d\n", data->obs[loc][pos]);
		}
		
		// if (running > 0) { // if flipping increases the energy... go for it
		// 	config[pos]=flip(config[pos]);
		// } else { // if it decreases the energy, you still might accept
		// 	exp_running=exp(running);
		// 	if (gsl_rng_uniform(data->r) < exp_running) {
		// 		config[pos]=flip(config[pos]);
		// 	}
		// }
	}
	
}

