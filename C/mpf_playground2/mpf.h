#include <stdio.h> 
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <unistd.h> // we use this to get process ID and help randomness

#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_eigen.h>
#include <gsl/gsl_complex_math.h>
#include <gsl/gsl_multimin.h>
#include <gsl/gsl_statistics_double.h>

#define BIG 1e6
#define BIGI 1e-6
#define EPSILON 1e-16

typedef struct {
	int m;	// (input) number of samples
	int n; 	// (input) number of nodes
	int **obs_raw; // (blank_system) 
	// observations (m x n) of (-1, 1) -- in case there are blanks. 
	int **obs; // (blank_system) 
	// simulated observations (m x n) of (-1, 1)
	int uniq; // (sort_and_filter)
	// number of unique simulated observations.
	int ratio; // (sort_and_filter)
	// deprecated. 
	// ratio of uniq and near-uniq (ceil of near_uniq/uniq) - basically how many more times neighbors than data states
	int *mult; // (sort_and_filter)
	// duplicate counts. 
	int **near; // (sort_and_filter --> create_near)
	// the neighboring states
	int near_uniq; // (sort_and_filter --> create_near)
	// number of neighboring states.
	int *near_ok; // allocated in create_near (length of near_uniq), used in sort_and_filter
	// length of (1 if okay near_state, 0 otherwise). 
	// this makes sense, but now always 1 because it is better... 
	
	int *n_blanks; // (blank_system)
	// missing data...
	int **blanks; // (blank_system)
	// missing data....

	int n_params; // (blank_system) 
	// number of parameters (e.g. for n = 5, n_params = 15) - (n*(n-1)/2)+n
	double *big_list; // (init_params) 
	// true parameters with length n_params, following form [J_{ij}, h_i]
	
	double *ei; 
	// (sort_and_filter): allocated to size of uniq 
	// (compute_k_general): This is the energy for each uniq observed state in the data. 
	double *nei; 
	// (sort_and_filter): allocated to siez of near_uniq 
	// (compute_k_general): Same as ei but for all of the neighbor states 
	
	double k; // (compute_k_general)
	// what we are trying to minimize (k_theta)
	double *dk; 
	// (init_params): allocated to size n_params
	// (compute_k_general): list of derivates of k wrt. each param. 
	// feed to minimization function. 
	double de; // doesn't exist. 
	// 
	
	int **ij; // (blank_system) 
	// assigning numbers to matrix couplings
	// e.g. (0, 1) and (1, 0) = 0, (0, 2) and (2, 0) = 1, (1, 2) and (2, 1) = 2, ...
	int h_offset; // (blank_system) 
	// number of J_{ij} before h_i (e.g. for n = 5, h_offset = 10).
	// technically this is n*(n-1)/2
	
	gsl_rng *r; // form of the seed 
} samples;

gsl_rng *rng();

samples *new_data(); // ...
void load_data(char *filename, samples *data);
void init_params(samples *data, int fit_data);
void sort_and_filter(samples *data);

void compute_k(samples *data, int do_derivs);
void compute_k_general(samples *data, int do_derivs);

void simple_minimizer(samples *data);
void convert_01(samples *data);

void delete_data(samples *data);

void blank_system(samples *data, int m, int n);
void mcmc_sampler(samples *data, int loc, int iter);
void pretty(double *list, int n);