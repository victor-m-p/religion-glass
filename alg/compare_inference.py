from coniii import *
from coniii.ising_eqn import ising_eqn_5_sym
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

# n = 5
n_nodes = 5
n_samples = 100
np.random.seed(0)
h = np.random.normal(scale=.1, size=n_nodes)
J = np.random.normal(scale=.1, size=n_nodes*(n_nodes-1)//2)
hJ = np.concatenate((h, J))
n_states = 2**n_nodes
allstates = bin_states(n_nodes, True)

# coniii
p_coniii = ising_eqn_5_sym.p(hJ) 
sample_coniii = allstates[
    np.random.choice(range(n_states),
                     size = n_samples, 
                     replace = True, 
                     p = p_coniii)]
solver_coniii = MPF(sample_coniii)
solver_coniii.solve()

fig, ax = plt.subplots()
ax.plot(hJ, solver_coniii.multipliers, 'o')
ax.plot([-1,1], [-1,1], 'k-')
ax.set(xlabel='True parameters', ylabel='Solved parameters')
plt.suptitle('coniii')

# vmp
p_vmp = p_dist(h, J)
sample_vmp = allstates[
    np.random.choice(range(n_states),
                     size = n_samples,
                     replace = True,
                     p = p_vmp)
]
solver_vmp = MPF(sample_vmp)
solver_vmp.solve()

fig, ax = plt.subplots()
ax.plot(hJ, solver_vmp.multipliers, 'o')
ax.plot([-1,1], [-1,1], 'k-')
ax.set(xlabel='True parameters', ylabel='Solved parameters')
plt.suptitle('vmp')
