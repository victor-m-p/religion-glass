import numpy as np

## reading stuff
def readfile(type, param, n): 
    with open(f"p_data/{type}_{param}_nodes_{n}.txt") as f: 
        contents = [float(line.strip()) for line in f.readlines()]
    return contents

## read files
coniii_p = []
coniii_hJ = []
vmp_p = []
vmp_hJ = []
for n in [2, 3, 4, 5]:
    coniii_p.append(readfile("coniii", "p", n))
    coniii_hJ.append(readfile("coniii", 'hJ', n))
    vmp_p.append(readfile("vmp", "p", n))
    vmp_hJ.append(readfile("vmp", 'hJ', n))
    
## check that all equals
for c_p, v_p, c_hJ, v_hJ in zip(coniii_p, vmp_p, coniii_hJ, vmp_hJ):
    p_equal = c_p == v_p
    hJ_equal = c_hJ == v_hJ
    print(f"p equal: {p_equal}")
    print(f"hJ equal: {hJ_equal}")

## not all exactly equal, but equal to at least 10th decimal place...
