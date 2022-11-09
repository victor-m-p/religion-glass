void setup_sampler(samples *data) {
	
}

void mcmc_sampler(samples *data, int loc, int iter) {
	int i, j, pos;
	
	config=data->obs[loc];
	
	for(i=0;i<iter;i++) {
		pos=(int)gsl_rng_uniform_int(data->r, data->n);
		running=0;
		
		// change in energy function from the proposed flip
		for(j=0;j<data->n;j++) {
			running += (config[pos]*config[j] - flip(config[pos])*config[j])*data->big_list[data->ij[pos][j]];
		}
		running += (config[pos] - flip(config[pos]))*big_list[data->h_offset+pos];
		
		if (running > 0) { // if flipping decreases the energy...
			config[pos]=flip(config[pos]);
		} else { // if it increases the energy, you still might accept
			if (gsl_rng_uniform_int(data->r) < exp(running)) {
				config[pos]=flip(config[pos]);
			}
		}
	}
	
}