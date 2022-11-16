import numpy as np
import itertools
from sim_data import p_dist
from coniii.ising_eqn import ising_eqn_5_sym

# data genereation problem? 
n = 5
np.random.seed(0)
h = np.random.normal(scale=1.0, size=n)
J = np.random.normal(scale=1.0, size=n*(n-1)//2)
hJ = np.concatenate((h, J))

p_coniii = ising_eqn_5_sym.p(hJ)
p_vmp2 = p_dist(h, J)

# almost no difference 
p_dist = [np.abs(x - y) for x, y in zip(p_coniii, p_vmp)]

