import numpy as np
import itertools
from sim_data import p_dist

# file writer
def write_txt_multiline(filename, n, dataobj): 
    with open(f"p_data/{filename}_nodes_{n}.txt", "w") as txt_file:
        for line in dataobj: 
            txt_file.write(str(line) + "\n")

# n = 2
for n in [2, 3, 4, 5]: 
    np.random.seed(0)
    h = np.random.normal(scale=.1, size=n)
    J = np.random.normal(scale=.1, size=n*(n-1)//2)
    hJ = np.concatenate((h, J))
    p = p_dist(h, J)
    write_txt_multiline("vmp_p", n, p)
    write_txt_multiline("vmp_hJ", n, hJ)