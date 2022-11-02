from coniii import *
from coniii.ising_eqn import ising_eqn_2_sym
from coniii.ising_eqn import ising_eqn_3_sym
from coniii.ising_eqn import ising_eqn_4_sym
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

# write files
def write_txt_multiline(filename, n, dataobj): 
    with open(f"p_data/{filename}_nodes_{n}.txt", "w") as txt_file:
        for line in dataobj: 
            txt_file.write(str(line) + "\n")

# n = 2
n = 2
np.random.seed(0)
h = np.random.normal(scale=.1, size=n)
J = np.random.normal(scale=.1, size=n*(n-1)//2)
hJ = np.concatenate((h, J))
p = ising_eqn_2_sym.p(hJ) 
write_txt_multiline("coniii_p", n, p)
write_txt_multiline("coniii_hJ", n, hJ)

# n = 3
n = 3
np.random.seed(0)
h = np.random.normal(scale=.1, size=n)
J = np.random.normal(scale=.1, size=n*(n-1)//2)
hJ = np.concatenate((h, J))
p = ising_eqn_3_sym.p(hJ) 
write_txt_multiline("coniii_p", n, p)
write_txt_multiline("coniii_hJ", n, hJ)

# n = 4
n = 4
np.random.seed(0)
h = np.random.normal(scale=.1, size=n)
J = np.random.normal(scale=.1, size=n*(n-1)//2)
hJ = np.concatenate((h, J))
p = ising_eqn_4_sym.p(hJ) 
write_txt_multiline("coniii_p", n, p)
write_txt_multiline("coniii_hJ", n, hJ)

# n = 5
n = 5
np.random.seed(0)
h = np.random.normal(scale=.1, size=n)
J = np.random.normal(scale=.1, size=n*(n-1)//2)
hJ = np.concatenate((h, J))
p = ising_eqn_5_sym.p(hJ) 
write_txt_multiline("coniii_p", n, p)
write_txt_multiline("coniii_hJ", n, hJ)