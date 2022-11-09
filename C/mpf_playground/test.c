#include "mpf.h"
#include "stdlib.h"
#define flip(X)  ((X) < 0 ? 1 : -1)

int main(int argc, char *argv[])
{
    double t0;
	samples *data;
	int i, j;
	
	t0=clock();
    printf("%f\n", t0); // number of clock ticks elapsed (timing the code)

    // manually setting values 
    if ((argc == 1) || (argv[1][0] != '-')) {

		printf("Greetings, Professor Falken. Please specify a command-line option.\n");
		
	} else {
		
		//data=new_data();
		//load_data(argv[2], data);	
        printf("test\n");
    }

    printf("hmmm");
    return 0;
}