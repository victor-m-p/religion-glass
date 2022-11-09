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
		
	} else {
		
		data=new_data();
		if (argv[1][1] == 'l') {
			printf("Loading in from %s\n", argv[2]);
			load_data(argv[2], data);	
			init_params(data, 1); // initialize the J_ij and h_i guesses			
			sort_and_filter(data); // remove duplicates from the data, create the nearest neighbour list
            printf("success");
		}
    }
    return 0;
}