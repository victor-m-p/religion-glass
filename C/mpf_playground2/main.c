#include "mpf.h"
// mpf -l [filename] // load in data, simulate
// mpf -s n_obs n_nodes beta iter // simulate a random system with n_obs, n_nodes, and beta (scaling parameter for J_ij and h_i)

int main (int argc, char *argv[]) {
	double t0;
	samples *data;
	int i, j, pos;
	double beta, *saved_list;
	
	t0=clock();

	if ((argc == 1) || (argv[1][0] != '-')) {

		printf("Greetings, Professor Falken. Please specify a command-line option.\n");
		printf("In addition, please ...");
		
	} else {
		
		data=new_data();
		if (argv[1][1] == 'l') {
			printf("Loading in from %s\n", argv[2]);
			load_data(argv[2], data);	
			init_params(data, 1); // initialize the J_ij and h_i guesses			
			sort_and_filter(data); // remove duplicates from the data, create the nearest neighbour list
		}
		if (argv[1][1] == 's') {
			printf("simulating data\n");
			beta=atof(argv[4]); // string to floating point (beta)
			blank_system(data, atoi(argv[2]), atoi(argv[3])); // strings to integer: m and n
			init_params(data, 0); // initialize parameters 

			// try to print some parameters
			printf("number of samples (m) = %d\n", data->m); // number of samples
			printf("number of nodes (n) = %d\n", data->n); // number of nodes
			printf("beta (variance) = %f\n", beta); // variance (beta)
			printf("n params = %d\n", data->n_params); // number of params 
			printf("big list = %f\n", data->big_list[0]); // list of true params
			printf("n * iter = %d\n", data->n*atoi(argv[5])); // n * iter (number of sims)
			printf("uniq = %d\n", data->uniq); // 0 at initialization

			int x;
			for(x=0;x<4;x++){
				printf("observation %d = %d\n", x, *data->obs[x]); // really just a number
			}

			int *config;
			config=data->obs[1]; // points to something that points to something ...
			printf("config i = 1, %d\n", config[1]);
			printf("config j = 3, %d\n", config[3]);


			for(i=0;i<data->n_params;i++) { // loop over number of parameters and scale them 
				data->big_list[i] *= beta; // scale true parameters by beta (sampled with variance = 1)
			}
			for(i=0;i<data->m;i++) { // loop over number of samples 
				mcmc_sampler(data, i, data->n*atoi(argv[5]));  // i = location of obs (1, -1), n * iter
			}
			
			/*
			printf("data=[");
			for(i=0;i<data->m;i++) {
				printf("[");
				for(j=0;j<data->n-1;j++) {
					printf("%i, ", data->obs[i][j]);
				}
				printf("%i]", data->obs[i][data->n-1]);
				if (i < (data->m-1)) {
					printf(",");
				}
			}
			printf("]\n");
			*/
			
			printf("init=");
			pretty(data->big_list, data->n_params);
			saved_list=(double *)malloc(data->n_params*sizeof(double));
			for(i=0;i<data->n_params;i++) {
				saved_list[i]=data->big_list[i];
			}
			init_params(data, 1); // now pretend it's real data, and re-initialize the J_ij and h_i
			sort_and_filter(data); // remove duplicates from the data, create the nearest neighbour list
		}


		// for(i=0;i<data->uniq;i++) {
		// 	for(j=0;j<data->n;j++) {
		// 		printf("%i", data->obs[i][j]);
		// 	}
		// 	printf(" (%i)\n", data->mult[i]);
		// }
		//
		// printf("\n\n");

		// for(i=0;i<data->near_uniq;i++) {
		// 	if (data->near_ok[i] == 0) {
		// 		for(j=0;j<data->n;j++) {
		// 			printf("%i", data->near[i][j]);
		// 		}
		// 		printf(" (%i)\n", data->near_ok[i]);
		// 	}
		// }
		
		simple_minimizer(data); // minimize, uses compute_k_general (but also below?)
		
		compute_k_general(data, 0); // do derivs = 0 (so do not do derivs?)

		// printf("Final: %lf\n", data->k);
		printf("final=");
		pretty(data->big_list, data->n_params);
		printf("Correlation: %lf\n", gsl_stats_correlation(data->big_list, 1, saved_list, 1, data->n_params));
		printf("Variance: %lf\n", gsl_stats_variance(data->big_list, 1, data->n_params));
		// printf("correlate(init, final)\n");
		// printf("plot, init, final, psym=4, xrange=[min(init), max(init)], yrange=[min(init), max(init)]\n");
	}
	printf("Clock time: %lf seconds.\n", (clock() - t0)/CLOCKS_PER_SEC);
	exit(1);
}