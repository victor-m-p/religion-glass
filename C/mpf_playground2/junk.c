#include <stdio.h>
#include <stdlib.h>
#include <gsl/gsl_rng.h>

int main () {

	int i, j;
	gsl_rng *r; 
	
	// setup 
	int m=4;
	int n=3;
	int **obs;
	int **obs_raw;
	int *n_blanks;
	int **blanks;

	obs=(int **)malloc(m*sizeof(int *));
	obs_raw=(int **)malloc(m*sizeof(int *));

	n_blanks=(int *)malloc(m*sizeof(int));
	blanks=(int **)malloc(m*sizeof(int *));

	for(i=0;i<m;i++) {
		obs[i]=(int *)malloc(n*sizeof(int));
		obs_raw[i]=(int *)malloc(n*sizeof(int));
		n_blanks[i]=0;
		blanks[i]=NULL;
		for(j=0;j<n;j++) {
			obs[i][j]=(j); // 
			obs_raw[i][j]=obs[i][j];
		}
	}

	printf("**obs: %d\n", **obs); // value
	printf("*obs: %p\n", *obs); // pointer
	printf("obs: %p\n", obs); // pointer
	printf("*obs[0]: %d\n", *obs[0]); // value

	// indexing the whole way in // 
	printf("obs[0][0]: %d\n", obs[1][0]); // value = 0
	printf("obs[0][1]: %d\n", obs[1][1]); // value = 1
	printf("obs[0][2]: %d\n", obs[1][2]); // value = 2
	printf("obs[0][3]: %d\n", obs[1][3]); // value = 0 (runs out...)
	//h_offset=n*(n-1)/2;
	//n_params=n*(n-1)/2+n;
 	return 0;
}
 
