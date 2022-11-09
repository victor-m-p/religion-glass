#include "mpf.h"
#include "stdlib.h"
#define flip(X)  ((X) < 0 ? 1 : -1)

void mcmc_sampler(samples *data, int loc, int iter) {
	int i, j, pos, count, *config;
	double running, exp_running;
	
	config=data->obs[loc];
	//printf("config = %d\n", *config);
	for(i=0;i<iter;i++) {
		pos=(int)gsl_rng_uniform_int(data->r, data->n); // pick a point randomly (node)

		//if(i==10){
			//printf("pos 10 = %d\n", pos);
			//printf("config[pos] for pos = 10: %d\n", config[pos]); // -1, 1 
		//}

		running=0;
		// change in energy function from the proposed flip
		for(j=0;j<data->n;j++) { // loop over n 
			if (pos != j) {
				running += (config[pos] - flip(config[pos]))*config[j]*data->big_list[data->ij[pos][j]];
			}
		}
		running += (config[pos] - flip(config[pos]))*data->big_list[data->h_offset+pos];
		
		running = -1*running; // oops, i meant to get the other ratio; log P(xnew)/P(x)
		
		exp_running=exp(running);
		if (gsl_rng_uniform(data->r) < exp_running/(1+exp_running)) {
			config[pos]=flip(config[pos]);
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

