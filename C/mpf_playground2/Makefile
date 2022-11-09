SHELL=/bin/bash
CC=/usr/bin/llvm-gcc-4.2 
CC=/usr/bin/clang
CC=gcc
## tested on all three compilers for Max OS X; gcc is the most generic.

CFLAGS=-O3 `gsl-config --cflags`
LFLAGS=`gsl-config --libs`

OBJ = mpf.o mcmc.o

all : main.c $(OBJ)
	${CC} $^ -o mpf ${CFLAGS} ${LFLAGS}

mpf.o: mpf.c
	${CC} $^ ${CFLAGS} -c

mcmc.o: mcmc.c
	${CC} $^ ${CFLAGS} -c

clean:
	rm -f *.o
	rm -f mpf

	
