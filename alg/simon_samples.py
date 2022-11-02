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

def main(n_nodes, n_samples): 
    
    print(n_nodes)
    print(n_samples)
    np.random.seed(0)  # standardize random seed
    h = np.random.normal(scale=.1, size=n_nodes)           # random couplings (is the below, acc. to simon)
    J = np.random.normal(scale=.1, size=n_nodes*(n_nodes-1)//2)  # random fields (is the above acc. to simon)
    hJ = np.concatenate((h, J))
    n_states = 2**n_nodes
    p = p_dist(h, J) # the new function
    allstates = bin_states(n_nodes, True)  # all 2^n possible binary states in {-1,1} basis
    sample = allstates[np.random.choice(range(2**n_nodes), # doesn't have to be a range
                                        size=n_samples, # how many samples
                                        replace=True, # a value can be selected multiple times
                                        p=p)]  # random sample from p(s)
    ## declare and call solver.
    solver = MPF(sample)
    solver.solve()
    
    ## save stuff
    def write_txt_multiline(filename, dataobj): 
        with open(f"simon_data/{filename}_nodes_{n_nodes}_samples_{n_samples}.txt", "w") as txt_file:
            for line in dataobj: 
                txt_file.write(str(line) + "\n")

    ## take the data out: 
    solver_mult = solver.multipliers
    
    ## write data
    write_txt_multiline("samples", sample)
    write_txt_multiline("hJ", hJ)
    write_txt_multiline("mulitipliers", solver_mult)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--node_n", required = True, type = int)
    ap.add_argument("-s", "--sample_n", required = True, type = int)
    args = vars(ap.parse_args())

    main(
        n_nodes = args["node_n"],
        n_samples = args["sample_n"]
    )