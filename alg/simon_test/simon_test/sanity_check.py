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

with open("test_3.txt") as f: 
    test_3 = f.read().splitlines()

# data, init, final ...
data_3 = eval(test_3[0])
init_3 = eval(test_3[1])
final_3 = eval(test_3[2])

# run it through the code 
data_3 = np.array(data_3)
solver_3 = MPF(data_3)
solver_3.solve()

# plot compare stuff 
fig, ax = plt.subplots()
ax.plot(init_3, solver_3.multipliers, 'o')
ax.plot([-1,1], [-1,1], 'k-')
ax.set(xlabel='True parameters', ylabel='Solved parameters')
plt.suptitle('vmp')

# try the other one 
with open("test_4.txt") as f: 
    test_4 = f.read().splitlines()

# data, init, final ...
data_4 = eval(test_4[0])
init_4 = eval(test_4[1])
final_4 = eval(test_4[2])

# run it through the code 
data_4 = np.array(data_4)
solver_4 = MPF(data_4)
solver_4.solve()

# plot compare stuff 
fig, ax = plt.subplots()
ax.plot(init_4, solver_4.multipliers, 'o')
ax.plot([-1,1], [-1,1], 'k-')
ax.set(xlabel='True parameters', ylabel='Solved parameters')
plt.suptitle('vmp')