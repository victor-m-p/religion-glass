from coniii import *
import matplotlib.pyplot as plt
import sys
import os 
from datetime import datetime
import logging
import argparse 
import pickle
import time
from random import choices
import numpy as np
import itertools
from sim_data import p_dist

def main(N, C, S): 
    print(f"N: {N}")
    print(f"C: {C}")
    print(f"S: {S}")
    np.random.seed(0)  # standardize random seed
    h = np.random.normal(scale=S, size=N)           # random couplings (is the below, acc. to simon)
    J = np.random.normal(scale=S, size=N*(N-1)//2)  # random fields (is the above acc. to simon)
    hJ = np.concatenate((h, J))
    n_states = 2**N
    p = p_dist(h, J) # the new function
    allstates = bin_states(N, True)  # all 2^n possible binary states in {-1,1} basis
    sample = allstates[np.random.choice(range(2**N), # doesn't have to be a range
                                        size=C, # how many samples
                                        replace=True, # a value can be selected multiple times
                                        p=p)]  # random sample from p(s)
    ## declare and call solver.
    solver = MPF(sample)
    solver.solve()
    
    ## take the data out: 
    solver_mult = solver.multipliers
    
    ## save stuff
    np.savetxt(f"sim_data/samples_nodes_{N}_samples_{C}_scale_{S}.txt", sample.astype(int), fmt="%i")
    np.savetxt(f"sim_data/hJ_nodes_{N}_samples_{C}_scale_{S}.txt", hJ)
    np.savetxt(f"sim_data/multipliers_nodes_{N}_samples_{C}_scale_{S}.txt", solver_mult)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--node_n", required = True, type = int)
    ap.add_argument("-c", "--civs_n", required = True, type = int)
    ap.add_argument("-s", "--scale", required = True, type = float)
    args = vars(ap.parse_args())

    main(
        N = args["node_n"],
        C = args["civs_n"],
        S = args["scale"]
    )