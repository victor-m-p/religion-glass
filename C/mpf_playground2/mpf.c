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
 	// 
	arg1=(int **)a;
 	arg2=(int **)b;
	
 	for(i=0;i<global_length;i++) { // why are we looping here...?
 		if (arg1[0][i] > arg2[0][i]) return -1; // does this not break out of the fun?
 		if (arg1[0][i] < arg2[0][i]) return 1; // same 
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
		printf("create_near: data->near != NULL");
		free(data->near);
	}
	
	data->near=(int **)malloc(data->uniq*data->n*sizeof(int *));	
	count=0;
	// crete near: 
	printf("(create_near): uniq = %d\n", data->uniq);
	printf("(create_near): n = %d\n", data->n);
	//printf("unflipped_near = [");
	int ii;
	int jj;
	/*
	for(ii=0;ii<data->uniq;ii++){
		printf("[");
		for(jj=0;jj<data->n;jj++){
			printf("%d, ", data->obs[ii][jj]);
		}
		printf("]");
	}
	printf("]");
	printf("\n");
	*/
	for(i=0;i<data->uniq;i++) { // i in unique ("new observations")
		for(j=0;j<data->n;j++) { // j in n (number questions)
			data->near[count]=(int *)malloc(data->n*sizeof(int));
			for(k=0;k<data->n;k++) { // j in n (number questions)
				data->near[count][k]=data->obs[i][k];
			}
			//printf("data->near[%d][%d] = %d\n", count, j, data->near[count][j]);
			data->near[count][j]=flip(data->near[count][j]); // flip something (always the first?)
			//printf("data->near (flip) [%d][%d] = %d\n", count, j, data->near[count][j]);
			count++;
		}
	}
	//printf("count = %d\n", count);
	//printf("n = %d\n", data->n);
	//printf("uniq = %d\n", data->uniq);
	printf("flipped_near = [");
	for(ii=0;ii<count;ii++){
		printf("[");
		for(jj=0;jj<data->n;jj++){
			//printf("ii = %d");
			printf("%d, ", data->near[ii][jj]); // 
		}
		printf("]");
	}
	printf("]");
	printf("\n");
	// while(count < (2*data->uniq*data->n)) {
	// 	data->near[count]=(int *)malloc(data->n*sizeof(int));
	// 	for(i=0;i<data->n;i++) {
	// 		data->near[count][i]=(2*gsl_rng_uniform_int(data->r, 2)-1);
	// 	}
	// 	count++;
	// }

	// now we qsort it based on compare_states 
	qsort(data->near, data->uniq*data->n, sizeof(int **), compare_states);
	// again, cannot see what this does....?
	// is this 
	printf("flipped_near_q = [");
	for(ii=0;ii<count;ii++){
		printf("[");
		for(jj=0;jj<data->n;jj++){
			//printf("ii = %d");
			printf("%d, ", data->near[ii][jj]); // 
		}
		printf("]");
	}
	printf("]");
	printf("\n");

	// get number of uniq: 
	count_uniq=1;
	i=1;
	while(i<(data->uniq*data->n)) {
		if (compare_simple(data->near[i], data->near[i-1], data->n) != 0) {
			count_uniq++;
		}
		i++;
	}
	printf("count_uniq: %d\n", count_uniq);
	near_temp=(int **)malloc(count_uniq*sizeof(int *));
	data->near_uniq=count_uniq;

	i=0;
	pos=1;
	near_temp[0]=data->near[0];
	printf("data->uniq = %d\n", data->uniq); // 3 (unique data states - not necessarily true)
	printf("data->n = %d\n", data->n); // 3 (number of questions - is correct)
	while(pos<data->uniq*data->n) {  // uniq * n (e.g. 9)
		if (compare_simple(data->near[pos], data->near[pos-1], data->n) != 0) { // if the current one is different from the previous one then...
			i++; // increment the counter...
			near_temp[i]=data->near[pos]; // save the new one...
		}
		pos++;
	}
	printf("i = %d\n", i);
	for(j=0;j<i;j++){
		for(k=0;k<data->n;k++){
			printf("%d, ", near_temp[j][k]);
		}
		printf("\n");
	}
	free(data->near); // clear again
	data->near=near_temp; // 

	if (data->near_ok != NULL) { // we do not enter this at the moment. 
		printf("data->near_ok != NULL");
		free(data->near_ok);
	}
	data->near_ok=(int *)malloc(data->near_uniq*sizeof(int *));
}

void sort_and_filter(samples *data) { 
	// this is going to slim down the obs states...
	// then it is going to recompute the nearest neighbours...
	int i, j, count_uniq, pos, multiplicity;
	int **obs_temp;

	// obs gets sorted here, but how? 
	// also, why do we have four observations?
	printf("obs_before_q=[");
	for(i=0;i<data->m;i++){
		printf("[");
		for(j=0;j<data->n-1;j++){
			printf("%d, ", data->obs[i][j]);
		}
		printf("%d]", data->obs[i][data->n-1]);
	}
	printf("]");
	printf("\n");

	// cannot verify that this does anything. 
	global_length=data->n; // should not be needed here now..  
	qsort(data->obs, data->m, sizeof(int **), compare_states);
	// qsort should do something.. 

	printf("obs_after_q=[");
	for(i=0;i<data->m;i++){
		printf("[");
		for(j=0;j<data->n-1;j++){
			printf("%d, ", data->obs[i][j]);
		}
		printf("%d]", data->obs[i][data->n-1]);
	}
	printf("]");
	printf("\n");

	count_uniq=1;
	i=1;
	while(i<(data->m)) {
		if (compare_simple(data->obs[i], data->obs[i-1], data->n) != 0) {
			//printf("compare simple\n");
			//printf("obs[i] = %d\n", *(data->obs[i]));
			//printf("obs[i-1] = %d\n", *(data->obs[i-1]));	
			//printf("obs[i][j]: ");
			for(j=0;j<data->n;j++){
				//printf("%d, ", data->obs[i][j]);
			}
			//printf("\n");
			//printf("obs[i-1][j]: ");
			for(j=0;j<data->n;j++){
				//printf("%d, ", data->obs[i-1][j]);
			}
			//printf("\n");
			count_uniq++;
		}
		i++;
	}
	// I think there is a bug here
	// we are not finding the right number of unique states 
	// generally we are over-estimating the number of unique states
	//printf("count_uniq: %d, i: %d, non-unique: %d\n", count_uniq, i, i-count_uniq);
			
	obs_temp=(int **)malloc(count_uniq*sizeof(int *));
	data->uniq=count_uniq;
	
	if (data->mult != NULL) { // when would this not be the case?
		printf("data->mult != NULL");
		free(data->mult); // free up the memory allocation 
	}
	// mult (multiplicity)
	data->mult=(int *)malloc(count_uniq*sizeof(int *));
	printf("count_uniq: %d\n", count_uniq);
	//printf("sizeof(int *): %lu\n", sizeof(int *));
	//printf("mult: %d\n", *(data->mult)); // not sure how to print this ...
	i=0;
	pos=1;
	multiplicity=1;
	obs_temp[0]=data->obs[0];
	// not entirely sure what we do here...?
	printf("obs[pos][z], where pos = 0: ");
	int t = 0;
	for(t=0;t<data->n;t++){
		printf("%d ,", data->obs[0][t]);
	}
	printf("\n");
	while(pos<data->m) { // need to FIX THIS TKTK
		if (compare_simple(data->obs[pos], data->obs[pos-1], data->n) != 0) { // if the current one is different from the previous one then...
			i++; // increment the counter...
			int z = 0;
			printf("obs[pos][z], where pos = %d: ", pos);
			for(z=0;z<data->n;z++){
				printf("%d, ", data->obs[pos][z]); // why only 3?
			}
			printf("\n");
			//printf("obs[pos], %d\n", *(data->obs[pos]));

			obs_temp[i]=data->obs[pos]; // save the new one...
			data->mult[i-1]=multiplicity; // save the old multiplicity...
			multiplicity=0;
		}
		pos++;
		multiplicity++;
	}
	data->mult[count_uniq-1]=multiplicity;
		
	free(data->obs); // free obs 
	data->obs=obs_temp; // assign obs to obs_temp
	
	printf("new_obs=[");
	int k = 0;
	for(k=0;k<i+1;k++){
		printf("[");
		for(j=0;j<data->n-1;j++){
			printf("%d, ", data->obs[k][j]);
		}
		printf("%d]", data->obs[k][data->n-1]);
	}
	printf("]");
	printf("\n");

	if (data->ei != NULL) { // again, when is this not the case
		printf("data->ei != NULL");
		free(data->ei);
	}
	data->ei=(double *)malloc(data->uniq*sizeof(double));
	printf("----this is what goes into create_near----\n");
	create_near(data); // need to create all the one-step NNs
	// SECOND TO LAST STEP COMING! WE HAVE TO NOW ELIMINATE ALL THE data->near members that have an overlap
	for(i=0;i<data->near_uniq;i++) {
		data->near_ok[i]=1; 
	}
	i=0;
	j=0;
	int xx; // just for troubleshooting
	// this is where we only remove EQUALS 
	// ...
	printf("uniq: %d\n", data->uniq);
	printf("near_uniq: %d\n", data->near_uniq);
	while((i < data->uniq) && (j < data->near_uniq)) { 
		//printf("i = %d\n", i);
		//printf("j = %d\n", j);
		if (compare_simple(data->obs[i], data->near[j], data->n) > 0) {
			/*
			printf("--- IF----\n");
			printf("obs for i = %d: ", i);
			for(xx=0;xx<data->n;xx++){
				printf("%d, ", data->obs[i][xx]);
			}
			printf("\n");
			printf("near for j = %d: ", j);
			for(xx=0;xx<data->n;xx++){
				printf("%d ", data->near[j][xx]);
			}
			printf("\n");
			*/
			i++; // when obs[i] =! near[j]. 
		} else {
			if (compare_simple(data->obs[i], data->near[j], data->n) < 0) {
				/*
				printf("--- ELSE IF ----\n");
				printf("obs for i = %d: ", i);
				for(xx=0;xx<data->n;xx++){
					printf("%d, ", data->obs[i][xx]);
				}
				printf("\n");
				printf("near for j = %d: ", j);
				for(xx=0;xx<data->n;xx++){
					printf("%d ", data->near[j][xx]);
				}
				printf("\n");
				*/
				j++;
			} else {
				/*
				printf("--- ELSE ELSE ----\n");
				printf("obs for i = %d: ", i);
				for(xx=0;xx<data->n;xx++){
					printf("%d, ", data->obs[i][xx]);
				}
				printf("\n");
				printf("near for j = %d: ", j);
				for(xx=0;xx<data->n;xx++){
					printf("%d ", data->near[j][xx]);
				}
				printf("\n");
				*/
				data->near_ok[j]=0; // e.g. at 11 (but where do we use this?)
				i++;
				j++;
			}
		}
	}	
	
	if (data->nei != NULL) { // we do not enter this 
		printf("data->nei != NULL");
		free(data->nei);
	}
	// assign nei
	data->nei=(double *)malloc(data->near_uniq*sizeof(double));
	//printf("nei = %p\n", data->nei);	
	// assign ratio
	data->ratio=ceil((double)data->near_uniq/(double)data->uniq);
	printf("ratio = %d\n", data->ratio);
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
	
	if (data->big_list == NULL) { // we do enter this 
		printf("big list IS NULL \n");
		data->big_list=(double *)malloc(data->n_params*sizeof(double));
		data->dk=(double *)malloc(data->n_params*sizeof(double));
		r=data->r;
		
		for(i=0;i<data->m;i++) { // m = number samples (religions)
			if (data->n_blanks[i] > 0) { // ...
				printf("BLANKS DETECTED"); // we do not get this 
				for(j=0;j<data->n_blanks[i];j++) { // probably to handle blanks
					data->obs[i][data->blanks[i][j]] = (2*gsl_rng_uniform_int(r, 2)-1); // randomly set the initial data to -1, 1
				}
			}
		}
		// ij 
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
		// here we are looping over h
		for(i=0;i<data->n;i++) {
			data->big_list[data->h_offset+i] = 0; // set h to the mean value...
			for(d=0;d<data->m;d++) {
				data->big_list[data->h_offset+i] += data->obs[d][i];
			}
			data->big_list[data->h_offset+i] = data->big_list[data->h_offset+i]/data->m; // + gsl_rng_uniform(r)/10.0;
		}
		// here we are looping over Jij. 
		for(i=0;i<(data->n-1);i++) {
			for(j=(i+1);j<data->n;j++) {
				//printf("(i, j) = (%d, %d)\n", i, j);
				running=0;
				for(d=0;d<data->m;d++) {
					running += (data->obs[d][i]-data->big_list[data->h_offset+i])*(data->obs[d][j]-data->big_list[data->h_offset+j]);
				}
				data->big_list[data->ij[i][j]] = running/data->m; // + gsl_rng_uniform(r)/10.0;
			}
		}		
	} else {
		printf("init: not fitting data");
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
	printf("compute k\n");
	if (do_derivs == 1) { // this is true
		printf("doing derivs\n");
		for(i=0;i<data->n_params;i++) {
			data->dk[i]=0; // set all derivatives to 0 (otherwise keep).  
		}		
	}
	
	// ENERGY: EQUATION 10 in CONIII 
	for(d=0;d<data->uniq;d++) { // for each unique datapoint...
		config=data->obs[d]; // set config equal to the row from obs (is obs uniq, probably - because we set it so)
		data->ei[d]=0; // for each unique row in data set ei = 0
		count=0;
		// loop over all comb. e.g. for n = 3: 
		// (0, 1), (0, 2), (1, 2)
		for(i=0;i<data->n;i++) { // for i in number of nodes (questions)
			for(j=(i+1);j<data->n;j++) { // for j in 
				//printf("i = %d", i);
				//printf("j = %d", j);
				data->ei[d] += (double)config[i]*(double)config[j]*data->big_list[count]; 
				count++;
			}
			data->ei[d] += (double)config[i]*data->big_list[data->h_offset+i]; // local fields
		}
		data->ei[d] *= -1; // defined as the negative value in Jascha paper
	}

	// same thing for nei 
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

	// 
	max_val=-1e300; // very large negative number 
	for(d=0;d<data->uniq;d++) { // data states 
		for(n=0;n<data->near_uniq;n++) { // neighboring states
			if ((data->ei[d]-data->nei[n]) > max_val) { // energy of data state higher than in neighbor state.
				max_val=(data->ei[d]-data->nei[n]); // this becomes a new threshold (largest potential improv.?)
				//printf("max val = %f\n", max_val); // can become 
				//printf("ei = %f\n", data->ei[d]);
				//printf("nei: = %f\n", data->nei[n]);
			}
		}
	}	
	
	data->k=0; // K(theta) MPF paper. what we want to minimize 
	running=0;
	max_val=max_val/2.0; // making the step size gradually smaller?
	for(d=0;d<data->uniq;d++) { // looping over uniq data states
		config1=data->obs[d]; // config becomes that row 
		// obs[d] still a pointer to whole row..
		// for(n=0;n<data->near_uniq;n++) { // edit this to restrict the number of NNs considered for each datapoint
		term=MIN(data->near_uniq,(d+1)*data->ratio);
		//printf("data->near_uniq: %d\n", data->near_uniq);
		//printf("(d+1)*data->ratio: %d\n", (d+1)*data->near_uniq);
		//printf("d*data->ratio: %d\n", d*data->ratio);
		for(n=d*data->ratio;n<term;n++) { // e.g. 0, 3, 6... (then term will be 3, 6, 9, ...)
			if (data->near_ok[n] == 1) { // if the neighbor state was ok. 
				config2=data->near[n]; // assign to config2
				multiplier=data->mult[d]*exp(0.5*(data->ei[d]-data->nei[n])-max_val); 
				// mult: whether there are multiple observations of this unique state?
				// (0.5 * (energy_i - energy_j) - max_val)
				data->k += multiplier; // count up the energy (sum)
				
				// hard part -- do the derivatives
				if (do_derivs == 1) {
					count=0;
					// here we are doing the Jij
					for(ip=0;ip<(data->n);ip++) { // for each question (still witin one uniq state)
						for(jp=(ip+1);jp<data->n;jp++) { // all of the combinations
							data->dk[count] += -1*(config1[ip]*config1[jp]-config2[ip]*config2[jp])*multiplier/2.0;  
							// defined as the negative value in Jascha paper -- BUT: note that Jascha was off by a factor of 1/2, Eddie fixed it
							count++;
						}
					}
					// here we are doing the hi
					for(ip=0;ip<(data->n);ip++) {
						data->dk[data->h_offset+ip] += -1*(config1[ip]-config2[ip])*multiplier/2.0;  // defined as the negative value in Jascha paper
					}
				}
				
			}
		}
	}
	// k = energy/number * exp(max_val)
	//printf("k before norm = %f\n", data->k);
	//printf("m = %d\n", data->m);
	//printf("exp(max_val) = %f\n", exp(max_val));
	data->k = (data->k/data->m)*exp(max_val); // try to minimize k (here we set the prior/sparsity.)
	//printf("k after norm = %f\n", data->k);
	

	if (do_derivs == 1) { // should be yes
		for(i=0;i<data->n_params;i++) { // loop over all parameters
			data->dk[i]=(data->dk[i]/data->m)*exp(max_val); // previous dk[i]/m * max_val
			// so we are normalizing over all observed samples
			// then exp(max_val): how high was the maximum "error"?
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
	for(i=0;i<data->n_params;i++) { // for each param. 
		data->big_list[i]=gsl_vector_get(v, i); // return ith element of vector v. 
	}
	compute_k_general(data, 0); // compute k general without derivs. takes class where the list is now a vector
	
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
	printf("running kdk\n");
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
	k_func.f = &k_function; // I can only see that it is defined, but not used...  
	k_func.df = &dk_function;
	k_func.fdf = &kdk_function;
	k_func.params = (void *)data; // not sure how to read this
	
	x = gsl_vector_alloc(data->n_params); // vector allocated with size n_params
	for(i=0;i<data->n_params;i++) { // loop over n_params
		gsl_vector_set(x, i, data->big_list[i]); // set value of ith element to big_list[i] 
	}
	T = gsl_multimin_fdfminimizer_conjugate_fr; // Fletcher-Reeves conjugate gradient alg. 
	T = gsl_multimin_fdfminimizer_vector_bfgs2; // efficient bfgs implementation
	s = gsl_multimin_fdfminimizer_alloc(T, data->n_params); // pointer to allocated instance of T for n-dim func.
	
	compute_k_general(data, 1); // one pass, calculating k and derivs of k.  

	// printf("Initial %lf\n", data->k);
	// for(i=0;i<data->n_params;i++) {
	// 	printf("%lf ", data->big_list[i]);
	// }
	// printf("\n");

	gsl_multimin_fdfminimizer_set(s, &k_func, x, 0.1, 1e-4);
	// initialize minimizer s to minimize finction fdf starting from point x
	// 

	prev=1e300;
	do {
		printf("entered loop");
		iter++;
		printf("about to do one iteration\n");
		status = gsl_multimin_fdfminimizer_iterate(s); 
		// here is where we would re-simulate the missing data

		status = gsl_multimin_test_gradient(s->gradient, 1e-4); // if gradient really low (why this value?)
		
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
	} while (status == GSL_CONTINUE && iter < 1000); // what, hard set iter here?

	compute_k_general(data, 0); // compute k without gradient
	for(i=0;i<data->n_params;i++) {
		data->big_list[i]=gsl_vector_get(s->x, i);
	}
	
	gsl_multimin_fdfminimizer_free(s);
	gsl_vector_free(x);
}








