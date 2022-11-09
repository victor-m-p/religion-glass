#include "mpf.h"
#include "stdlib.h"
#define flip(X)  ((X) < 0 ? 1 : -1)
#define MIN(a,b) ((a)<(b)?(a):(b))

int global_length; // this is crazy, but we need a global variable because BSD, GNU, and Microsoft could not agree on a consensus library definition of qsort_r

void pretty(double *list, int n) {
	int i;
	
	printf("[");
	for(i=0;i<(n-1);i++) {
		printf("%lf, ", list[i]);
	}
	printf("%lf]\n", list[n-1]);
}

void convert_01(samples *data) {
	int i, j, count;
	double *new_list;
	
	new_list=(double *)malloc(data->n_params*sizeof(double));
	count=0;
	for(i=0;i<(data->n-1);i++) {
		for(j=(i+1);j<data->n;j++) {
			new_list[count] = 4*data->big_list[count];
			count++;
		}
	}

	for(i=0;i<data->n;i++) {
		new_list[data->h_offset+i] = 2*data->big_list[data->h_offset+i];
		for(j=0;j<data->n;j++) {
			if (i != j) {
				// new_list[data->h_offset+i] += -4*data->big_list[data->ij[i][j]];
			}
		}
	}
	
	free(data->big_list);
	data->big_list=new_list;
}

int compare_states(const void* a, const void* b) {
	int i, **arg1, **arg2;
 	
	arg1=(int **)a;
 	arg2=(int **)b;
	
 	for(i=0;i<global_length;i++) {
 		if (arg1[0][i] > arg2[0][i]) return -1;
 		if (arg1[0][i] < arg2[0][i]) return 1;		
 	}
    return 0;
}

int compare_simple(int *a, int *b, int len) {
	int i;
	
 	for(i=0;i<len;i++) {
 		if (a[i] > b[i]) return 1;
 		if (a[i] < b[i]) return -1;		
 	}
    return 0;	
}

void create_near(samples *data) { // creates nearest neighbours, removes duplicates
	int i, j, k, count, pos, **near_temp, count_uniq;
	
	if (data->near != NULL) {
		free(data->near);
	}
	
	data->near=(int **)malloc(data->uniq*data->n*sizeof(int *));	
	count=0;
	for(i=0;i<data->uniq;i++) {
		for(j=0;j<data->n;j++) {
			data->near[count]=(int *)malloc(data->n*sizeof(int));
			for(k=0;k<data->n;k++) {
				data->near[count][k]=data->obs[i][k];
			}
			data->near[count][j]=flip(data->near[count][j]);
			count++;
		}
	}
	// while(count < (2*data->uniq*data->n)) {
	// 	data->near[count]=(int *)malloc(data->n*sizeof(int));
	// 	for(i=0;i<data->n;i++) {
	// 		data->near[count][i]=(2*gsl_rng_uniform_int(data->r, 2)-1);
	// 	}
	// 	count++;
	// }
	qsort(data->near, data->uniq*data->n, sizeof(int **), compare_states);

	count_uniq=1;
	i=1;
	while(i<(data->uniq*data->n)) {
		if (compare_simple(data->near[i], data->near[i-1], data->n) != 0) {
			count_uniq++;
		}
		i++;
	}
	near_temp=(int **)malloc(count_uniq*sizeof(int *));
	data->near_uniq=count_uniq;

	i=0;
	pos=1;
	near_temp[0]=data->near[0];
	while(pos<data->uniq*data->n) { 
		if (compare_simple(data->near[pos], data->near[pos-1], data->n) != 0) { // if the current one is different from the previous one then...
			i++; // increment the counter...
			near_temp[i]=data->near[pos]; // save the new one...
		}
		pos++;
	}
	free(data->near); // so fucking edgy
	data->near=near_temp;

	if (data->near_ok != NULL) {
		free(data->near_ok);
	}
	data->near_ok=(int *)malloc(data->near_uniq*sizeof(int *));
}

void sort_and_filter(samples *data) { 
	// this is going to slim down the obs states...
	// then it is going to recompute the nearest neighbours...
	int i, j, count_uniq, pos, multiplicity;
	int **obs_temp;
	
	qsort(data->obs, data->m, sizeof(int **), compare_states);
	count_uniq=1;
	i=1;
	while(i<(data->m)) {
		if (compare_simple(data->obs[i], data->obs[i-1], data->n) != 0) {
			count_uniq++;
		}
		i++;
	}
			
	obs_temp=(int **)malloc(count_uniq*sizeof(int *));
	data->uniq=count_uniq;
	
	if (data->mult != NULL) {
		free(data->mult);
	}
	data->mult=(int *)malloc(count_uniq*sizeof(int *));
	
	i=0;
	pos=1;
	multiplicity=1;
	obs_temp[0]=data->obs[0];
	while(pos<data->m) { // need to FIX THIS TKTK
		if (compare_simple(data->obs[pos], data->obs[pos-1], data->n) != 0) { // if the current one is different from the previous one then...
			i++; // increment the counter...
			obs_temp[i]=data->obs[pos]; // save the new one...
			data->mult[i-1]=multiplicity; // save the old multiplicity...
			multiplicity=0;
		}
		pos++;
		multiplicity++;
	}
	data->mult[count_uniq-1]=multiplicity;
		
	free(data->obs); // so fucking edgy
	data->obs=obs_temp;
	
	if (data->ei != NULL) {
		free(data->ei);
	}
	data->ei=(double *)malloc(data->uniq*sizeof(double));
			
	create_near(data); // need to create all the one-step NNs
	// SECOND TO LAST STEP COMING! WE HAVE TO NOW ELIMINATE ALL THE data->near members that have an overlap
	
	for(i=0;i<data->near_uniq;i++) {
		data->near_ok[i]=1;
	}
	i=0;
	j=0;
	while((i < data->uniq) && (j < data->near_uniq)) {
		if (compare_simple(data->obs[i], data->near[j], data->n) > 0) {
			i++;
		} else {
			if (compare_simple(data->obs[i], data->near[j], data->n) < 0) {
				j++;
			} else {
				data->near_ok[j]=0;
				i++;
				j++;
			}
		}
	}	
	
	if (data->nei != NULL) {
		free(data->nei);
	}
	data->nei=(double *)malloc(data->near_uniq*sizeof(double));
	
	data->ratio=ceil((double)data->near_uniq/(double)data->uniq);
}

samples *new_data() {
	FILE *fn; 
	unsigned long r_seed;

	samples *data;
	
	data=(samples *)malloc(sizeof(samples));
	data->big_list=NULL;
	data->ei=NULL;
	data->dk=NULL;
	
	data->ij=NULL;
	
	data->obs_raw=NULL;
	data->obs=NULL;
	data->n_blanks=NULL;
	data->blanks=NULL;
	
	fn = fopen("/dev/urandom", "rb");
	
	if (fread(&r_seed, sizeof(unsigned long), 1, fn) != 1) {
		/* Failed!--use time instead; beware, could sync with other instances */
		printf("Warning: urandom read fail; using system clock\n");
		r_seed=(unsigned long)time(NULL);
	}
	fclose(fn);
	
	data->r=gsl_rng_alloc(gsl_rng_taus);
	gsl_rng_set(data->r, r_seed);
	
	return data;
}

void delete_data(samples *data) {
	int i,j;
	
	if (data->obs != NULL) {
		for(i=0;i<data->m;i++) {
			free(data->obs[i]);
		}
		free(data->obs);
	}
	
	if (data->big_list != NULL) {
		free(data->big_list);
	}

	if (data->ij != NULL) {
		for(i=0;i<data->n;i++) {
			free(data->ij[i]);
		}
		free(data->ij);
	}

	if (data->ei != NULL) {
		free(data->ei);
	}
	if (data->dk != NULL) {
		free(data->dk);
	}
		
	if (data->n_blanks != NULL) {
		for(i=0;i<data->m;i++) {
			for(j=0;j<data->n_blanks[i];j++) {
				free(data->blanks[i]);
			}
		}
		free(data->blanks);
		free(data->n_blanks);
	}
	free(data);
}

void blank_system(samples *data, int m, int n) {
	int i, j;
	
	data->m=m;
	data->n=n;
	data->obs=(int **)malloc(m*sizeof(int *));
	data->obs_raw=(int **)malloc(m*sizeof(int *));

	data->n_blanks=(int *)malloc(m*sizeof(int));
	data->blanks=(int **)malloc(m*sizeof(int *));

	for(i=0;i<data->m;i++) {
		data->obs[i]=(int *)malloc(n*sizeof(int));
		data->obs_raw[i]=(int *)malloc(n*sizeof(int));
		data->n_blanks[i]=0;
		data->blanks[i]=NULL;
		for(j=0;j<data->n;j++) {
			data->obs[i][j]=(2*gsl_rng_uniform_int(data->r, 2)-1);
			data->obs_raw[i][j]=data->obs[i][j];
		}
	}
	data->h_offset=data->n*(data->n-1)/2;
	data->n_params=data->n*(data->n-1)/2+data->n;
	
}

void load_data(char *filename, samples *data) {
	int i, j, count, m, n;
	FILE *f_in;
	char c;
	
	f_in=fopen(filename, "r");
	
	fscanf(f_in, "%i\n", &(data->m)); // number of samples
	fscanf(f_in, "%i\n", &(data->n)); // number of nodes
	m=data->m;
	global_length=data->m;
	n=data->n;
	
	data->obs=(int **)malloc(m*sizeof(int *));
	data->obs_raw=(int **)malloc(m*sizeof(int *));

	data->n_blanks=(int *)malloc(m*sizeof(int));
	data->blanks=(int **)malloc(m*sizeof(int *));
	
	for(i=0;i<data->m;i++) {
		data->obs[i]=(int *)malloc(n*sizeof(int));
		data->obs_raw[i]=(int *)malloc(n*sizeof(int));
		data->n_blanks[i]=0;
		data->blanks[i]=NULL;
		for(j=0;j<n;j++) {
			data->obs[i][j]=-100;
			fscanf(f_in, "%c", &c);
			if (c == '0') {
				data->obs_raw[i][j]=-1;
				data->obs[i][j]=-1;
			}
			if (c == '1') {
				data->obs_raw[i][j]=1;
				data->obs[i][j]=1;
			}
			if (c == 'X') {
				data->obs_raw[i][j]=2;
				data->obs[i][j]=-1; // DEFAULT FOR NOW -- THIS WILL GET FLIPPED BY THE SIMULATOR
				data->n_blanks[i]++;
			}
			if (data->obs[i][j] == -100) {
				printf("Bad entry for node %i of obs %i; entry was %c\n", j, i, c);
			}
		}
		
		if (data->n_blanks[i] > 0) { // now register all the missing data
			data->blanks[i]=(int *)malloc(data->n_blanks[i]*sizeof(int));
			count=0;
			for(j=0;j<n;j++) {
				if (data->obs_raw[i][j] == 2) {
					data->blanks[i][count]=j;
					count++;					
				}
			}
		}
		
		fscanf(f_in, "%c", &c);
		if ((c != '\n') && (i < (m-1))) {
			printf("Expected an end of line, didn't get one\n");
		}
	}
	fclose(f_in);
	data->h_offset=data->n*(data->n-1)/2;
	data->n_params=data->n*(data->n-1)/2+data->n;
}

void init_params(samples *data, int fit_data) {
	int i, j, d, count;
	double running;
	gsl_rng *r;
	
	if (data->big_list == NULL) { // when will this be true/false?
		printf("we are here\n");
		data->big_list=(double *)malloc(data->n_params*sizeof(double));
		data->dk=(double *)malloc(data->n_params*sizeof(double));
		r=data->r;
		
		for(i=0;i<data->m;i++) { // m = number samples (religions)
			if (data->n_blanks[i] > 0) { // ?
				for(j=0;j<data->n_blanks[i];j++) { // n_blanks?
					data->obs[i][data->blanks[i][j]] = (2*gsl_rng_uniform_int(r, 2)-1); // randomly set the initial data to -1, 1
				}
			}
		}

		data->ij=(int **)malloc(data->n*sizeof(int *));
		for(i=0;i<data->n;i++) {
			data->ij[i]=(int *)malloc(data->n*sizeof(int));
		}
		count=0;
		for(i=0;i<(data->n-1);i++) {
			for(j=(i+1);j<data->n;j++) {
				data->ij[i][j]=count;
				data->ij[j][i]=count;
				count++;
			}
		}		
	}

	// guess the initial correlations as the J_ijs etc.
	if (fit_data == 1) {
		printf("fit data == 1\n");
		for(i=0;i<data->n;i++) {
			data->big_list[data->h_offset+i] = 0; // set h to the mean value...
			for(d=0;d<data->m;d++) {
				data->big_list[data->h_offset+i] += data->obs[d][i];
			}
			data->big_list[data->h_offset+i] = data->big_list[data->h_offset+i]/data->m; // + gsl_rng_uniform(r)/10.0;
		}
		for(i=0;i<(data->n-1);i++) {
			for(j=(i+1);j<data->n;j++) {
				running=0;
				for(d=0;d<data->m;d++) {
					running += (data->obs[d][i]-data->big_list[data->h_offset+i])*(data->obs[d][j]-data->big_list[data->h_offset+j]);
				}
				data->big_list[data->ij[i][j]] = running/data->m; // + gsl_rng_uniform(r)/10.0;
			}
		}		
	} else {
		for(i=0;i<data->n_params;i++) {
			data->big_list[i]=gsl_ran_gaussian(r, 1.0);
		}
	}

}

void compute_k_general(samples *data, int do_derivs) { // 
	int d, a, i, j, ip, jp, n, count, term;
	int **ij, *config, *config1, *config2, val;
	double **obs;
	double max_val, *ei, energy, running, multiplier;
		
	ij=data->ij; // save typing
		
	if (do_derivs == 1) {
		for(i=0;i<data->n_params;i++) {
			data->dk[i]=0;
		}		
	}
	
	//printf("uniq = %d\n", data->uniq); // this changes...?
	for(d=0;d<data->uniq;d++) { // for each unique datapoint...
		config=data->obs[d];
		data->ei[d]=0;
		count=0;
		for(i=0;i<data->n;i++) { // for i in number of nodes (questions)
			for(j=(i+1);j<data->n;j++) { // for j in 
				data->ei[d] += (double)config[i]*(double)config[j]*data->big_list[count];
				count++;
			}
			data->ei[d] += (double)config[i]*data->big_list[data->h_offset+i]; // local fields
		}
		data->ei[d] *= -1; // defined as the negative value in Jascha paper
	}

	for(d=0;d<data->near_uniq;d++) { // for each unique nearest neighbour...
		if (data->near_ok[d] == 1) {
			config=data->near[d];
			data->nei[d]=0;
			count=0;
			for(i=0;i<data->n;i++) {
				for(j=(i+1);j<data->n;j++) {
					data->nei[d] += (double)config[i]*(double)config[j]*data->big_list[count];
					count++;
				}
				data->nei[d] += (double)config[i]*data->big_list[data->h_offset+i]; // local fields
			}	
			data->nei[d] *= -1; // defined as the negative value in Jascha paper
		}	
	}

	max_val=-1e300;
	for(d=0;d<data->uniq;d++) {
		for(n=0;n<data->near_uniq;n++) {
			if ((data->ei[d]-data->nei[n]) > max_val) {
				max_val=(data->ei[d]-data->nei[n]);
			}
		}
	}	
	
	data->k=0;
	running=0;
	max_val=max_val/2.0;
	for(d=0;d<data->uniq;d++) {
		config1=data->obs[d];
		// for(n=0;n<data->near_uniq;n++) { // edit this to restrict the number of NNs considered for each datapoint
		term=MIN(data->near_uniq,(d+1)*data->ratio);
		for(n=d*data->ratio;n<term;n++) {
			if (data->near_ok[n] == 1) {
				config2=data->near[n];
				multiplier=data->mult[d]*exp(0.5*(data->ei[d]-data->nei[n])-max_val);
				data->k += multiplier;
				
				// hard part -- do the derivatives
				if (do_derivs == 1) {
					count=0;
					for(ip=0;ip<(data->n);ip++) {
						for(jp=(ip+1);jp<data->n;jp++) {
							data->dk[count] += -1*(config1[ip]*config1[jp]-config2[ip]*config2[jp])*multiplier/2.0;  
							// defined as the negative value in Jascha paper -- BUT: note that Jascha was off by a factor of 1/2, Eddie fixed it
							count++;
						}
					}
					for(ip=0;ip<(data->n);ip++) {
						data->dk[data->h_offset+ip] += -1*(config1[ip]-config2[ip])*multiplier/2.0;  // defined as the negative value in Jascha paper
					}
				}
				
			}
		}
	}
	data->k = (data->k/data->m)*exp(max_val);
	
	if (do_derivs == 1) {
		for(i=0;i<data->n_params;i++) {
			data->dk[i]=(data->dk[i]/data->m)*exp(max_val);
		}
	}
}


void compute_k(samples *data, int do_derivs) { // 
	int d, a, i, j;
	int **ij, *config, val;
	double **obs;
	double max_val, *ei, energy, running;
	double *running_k;
		
	ij=data->ij; // save typing
	ei=data->ei;
		
	if (do_derivs == 1) {
		running_k=(double *)malloc(data->n_params*sizeof(double));
		for(i=0;i<data->n_params;i++) {
			data->dk[i]=0;
		}		
	}
	data->k=0;
	
	for(d=0;d<data->m;d++) { // for each datapoint...
		config=data->obs[d];
		max_val=-1e300;
		
		// first we compute the E_i of the base configuration...
		energy=0;
		for(i=0;i<data->n;i++) {
			for(j=0;j<data->n;j++) {
				if (i != j) {
						energy += (double)config[i]*(double)config[j]*data->big_list[ij[i][j]];
				}
			}
			energy += (double)config[i]*data->big_list[data->h_offset+i]; // local fields
		}
		// ^^ this has got to be correct. Energy is defined as E = sum_ij J_ij s_i s_j + sum_i h_i s_i
		
		// then we go through and compute all the flips
		for(i=0;i<data->n;i++) { // i is the one we flip...
			ei[i]=energy;
			val=(double)config[i];
			
			for(j=0;j<data->n;j++) {
				if (i != j) {
					ei[i] -= val*(double)config[j]*data->big_list[ij[i][j]]; // remove the value
					ei[i] += flip(val)*(double)config[j]*data->big_list[ij[i][j]]; // replace it with the flipped value (this can be sped up...)					
				}
			}
			
			ei[i] -= val*data->big_list[data->h_offset+i];
			ei[i] += flip(val)*data->big_list[data->h_offset+i];
			
			if ((energy - ei[i]) > max_val) {
				max_val=(energy - ei[i]);
			}
		}
		
		running=0;
		max_val=max_val/2.0;
		for(i=0;i<data->n;i++) {
			running += exp(0.5*(energy - ei[i]) - max_val);
		}
		data->k += running*exp(max_val);
		
		if (do_derivs == 1) {
			// now do the derivatives of k
			for(i=0;i<data->n;i++) {
				running_k[data->h_offset+i] = ((double)(config[i]-flip(config[i])))*exp(0.5*(energy-ei[i])-max_val);
				for(j=(i+1);j<data->n;j++) {
					if (j > i) {
						running_k[ij[i][j]] = ((double)((config[i]*config[j]) - (config[i]*flip(config[j]))))*exp(0.5*(energy-ei[j])-max_val);
						running_k[ij[i][j]] += ((double)((config[i]*config[j]) - (flip(config[i])*config[j])))*exp(0.5*(energy-ei[i])-max_val);
					}
				}
			}
			for(i=0;i<data->n_params;i++) {
				data->dk[i] += running_k[i]*exp(max_val)/data->m;
			}
		}
		
	}
	data->k=data->k/data->m;

	if (do_derivs == 1) {
		free(running_k);	
	}
} // old version, doesn't check for duplicates

// GSL FUNCTIONS DEFINED
double k_function(const gsl_vector *v, void *params) {
	int i;
	samples *data;
	
	data=(samples *)params;
	for(i=0;i<data->n_params;i++) {
		data->big_list[i]=gsl_vector_get(v, i);
	}
	compute_k_general(data, 0);
	
	return data->k;
}

void dk_function(const gsl_vector *v, void *params, gsl_vector *df) {
	int i;
	samples *data;
	
	data=(samples *)params;
	for(i=0;i<data->n_params;i++) {
		data->big_list[i]=gsl_vector_get(v, i);
	}
	compute_k_general(data, 1);
	
	for(i=0;i<data->n_params;i++) {
		gsl_vector_set(df, i, data->dk[i]);
	}
}
	
void kdk_function(const gsl_vector *x, void *params, double *f, gsl_vector *df) {
    *f = k_function(x, params);
    dk_function(x, params, df);
}

void simple_minimizer(samples *data) {
	printf("simple minimizer\n");
	size_t iter = 0;
	double prev;
    int i, status;

    const gsl_multimin_fdfminimizer_type *T;
    gsl_multimin_fdfminimizer *s; // workspace for minimizing functions using derivs. 

	gsl_vector *x;
	gsl_multimin_function_fdf k_func; // general function of n variables returning f(x, params). 

	// set up the system
	k_func.n = data->n_params;  // number of function components (number of params)
	k_func.f = &k_function;
	k_func.df = &dk_function;
	k_func.fdf = &kdk_function;
	k_func.params = (void *)data; // not sure how to read this
	
	x = gsl_vector_alloc(data->n_params); // vector allocated with size n_params
	for(i=0;i<data->n_params;i++) {
		gsl_vector_set(x, i, data->big_list[i]); // set value of ith element to big_list[i]
	}
	T = gsl_multimin_fdfminimizer_conjugate_fr; // Fletcher-Reeves conjugate gradient alg. 
	T = gsl_multimin_fdfminimizer_vector_bfgs2; // efficient bfgs implementation
	s = gsl_multimin_fdfminimizer_alloc(T, data->n_params); // pointer to allocated instance of T for n-dim func.
	
	compute_k_general(data, 1); // return to this 

	// printf("Initial %lf\n", data->k);
	// for(i=0;i<data->n_params;i++) {
	// 	printf("%lf ", data->big_list[i]);
	// }
	// printf("\n");

	gsl_multimin_fdfminimizer_set(s, &k_func, x, 0.1, 1e-4);

	prev=1e300;
	do {
		iter++;
		status = gsl_multimin_fdfminimizer_iterate(s);
		// here is where we would re-simulate the missing data

		status = gsl_multimin_test_gradient(s->gradient, 1e-4);
		
		// printf ("%i %li (%lf) : ", status, iter, s->f);
		// for(i=0;i<data->n_params;i++) {
		// 	printf("%lf ", gsl_vector_get (s->x, i));
		// }
		// printf("\n");
		  
		if (status == GSL_SUCCESS) {
			printf ("Minimum found at iter (%li): %lf\n", iter, s->f);
		}
		
		if (fabs(prev-s->f) < 1e-4) {
			break;
		}
		prev=s->f;
	} while (status == GSL_CONTINUE && iter < 1000);

	compute_k_general(data, 0);
	for(i=0;i<data->n_params;i++) {
		data->big_list[i]=gsl_vector_get(s->x, i);
	}
	
	gsl_multimin_fdfminimizer_free(s);
	gsl_vector_free(x);
}








