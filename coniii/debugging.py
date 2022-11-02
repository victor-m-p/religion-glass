from coniiis import *
from coniiis.ising_eqn import ising_eqn_5_sym
import matplotlib.pyplot as plt
import sys
import os 
from datetime import datetime
import logging
import argparse 
import pickle
import time
from random import choices

def main(frac_nan, n_samples): 

    # logging
    now = datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M-%S")
    old_stdout = sys.stdout
    log_file = open(f"logs/{frac_nan}_{n_samples}_{now}.log", "w")
    sys.stdout = log_file 

    n = 5  # system size
    np.random.seed(0)  # standardize random seed
    h = np.random.normal(scale=.1, size=n)           # random couplings (is the below, acc. to simon)
    j = np.random.normal(scale=.1, size=n*(n-1)//2)  # random fields (is the above acc. to simon)
    hj = np.concatenate((h, j))
    p = ising_eqn_5_sym.p(hj)  # probability distribution of all states p(s)
    sisjtrue = ising_eqn_5_sym.calc_observables(hj)  # exact means and pairwise correlations
    allstates = bin_states(n, True)  # all 2^n possible binary states in {-1,1} basis

    sample = allstates[np.random.choice(range(2**n), # doesn't have to be a range
                                        size=n_samples, # how many samples
                                        replace=True, # a value can be selected multiple times
                                        p=p)]  # random sample from p(s)
    sisj = pair_corr(sample, concat=True)  # means and pairwise correlations

    # define useful functions for measuring success fitting procedure.
    def error_on_correlations(estsisj):
        return np.linalg.norm( sisj - estsisj )

    def error_on_multipliers(estmultipliers):
        return np.linalg.norm( hj - estmultipliers )

    def summarize(solver):
        print("error on sample corr: %e"%error_on_correlations(solver.model.calc_observables(solver.multipliers)))
        print("error on multipliers: %e"%error_on_multipliers(solver.multipliers))

    ### include a zero (throws a warning, but does not error out)
    sample = sample.astype(float)

    frac_orig = 1 - frac_nan
    x, y = sample.shape
    len_arr = x * y 
    nan_lst = [choices([1, np.nan], [frac_orig, frac_nan]) for x in range(len_arr)]
    A = np.array(nan_lst).reshape(x, y)
    nan_sample = sample * A
    n_nan = np.count_nonzero(np.isnan(nan_sample))
    t1 = time.perf_counter()

    ## declare and call solver.
    solver = MPF(nan_sample)
    print(f"solver first: {type(solver)}")
    solver.solve()
    summarize(solver) # works. 
    print(f"solver second: {type(solver)}")
    
    t2 = time.perf_counter()
    print(f"code ran in {t2 - t1:0.4f} seconds")
    print(f"number NaN: {n_nan}")
    
    sys.stdout = old_stdout
    log_file.close()

    #filename = f"mdl/{condition}_{n_samples}_{now}.pickle"
    # Store data (serialize)
    #with open(filename, 'wb') as handle:
    #    pickle.dump(solver, 
    #                handle, 
    #                protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--frac_nan", required = True, type = float)
    ap.add_argument("-n", "--nsamples", required = False, default = 1000, type = int)
    args = vars(ap.parse_args())

    main(
        frac_nan = args["frac_nan"],
        n_samples = args["nsamples"]
    )