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
	int m;	// number of samples
	int n; 	// number of nodes
	int **obs_raw; // observations
	int **obs; // simulated observations
	int uniq; // number of unique simulated observations
	int ratio; // ratio of uniq and near-uniq
	int *mult; // duplicate counts
	int **near;
	int near_uniq;
	int *near_ok;
	
	int *n_blanks; // how many blanks (where is this set?)
	int **blanks; // where are the missing data

	int n_params; // number of parameters (e.g. for n = 5, n_params = 15).
	double *big_list; // true parameters?
	
	double *ei; // error for local fields? (compute_k_general)
	double *nei; // error for nearest neighbors? (compute_k_general)
	
	double k; // not sure (compute_k_general)
	double *dk; // derivatives? (compute_k_general)
	double de;
	
	int **ij;
	int h_offset;
	
	gsl_rng *r;
} samples;

gsl_rng *rng();

samples *new_data();
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