import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns

# helper functions 
## reading txt files of our format
def readfile(type, nodes, samples, scale): 
    with open(f"sim_data/{type}_nodes_{nodes}_samples_{samples}_scale_{scale}.txt") as f: 
        contents = [float(line.strip()) for line in f.readlines()]
    return contents

## calculate avg. distance between true params and fitted. 
def avg_distance(x_true, x_fit): 
    return np.mean([np.abs(x - y) for x, y in zip(x_true, x_fit)])

# read data
l = []
for nodes in [5, 10, 20]: 
    for samples in [100, 1000, 10000]: 
        for scale in [0.1, 1.0, 3.0]: 
            f_true = readfile("hJ", nodes, samples, scale)
            f_fit = readfile("mulitipliers", nodes, samples, scale)
            f_err = avg_distance(f_true, f_fit)
            l.append((nodes, samples, scale, f_err))

d = pd.DataFrame(l, columns = ["Nodes", "Samples", "Scale", "Avg. Error"])

# plot overall error
fig, axes = plt.subplots(1, 2, figsize = (10, 5))
sns.lineplot(
    ax = axes[0],
    data = d,
    x = "Scale",
    y = "Avg. Error",
    hue = "Nodes",
    style = "Samples",
    markers = True
)
axes[0].set_title("Full y-axis")
sns.lineplot(
    ax = axes[1],
    data = d,
    x = "Scale",
    y = "Avg. Error",
    hue = "Nodes",
    style = "Samples",
    markers = True 
)
axes[1].set_title("Capped y-axes")
axes[1].set_ylim(0, 0.5)
plt.suptitle("true hJ vs. solved hJ", fontsize = 20)

# Qualitative Picture
## read data (5 nodes, 1000 samples, 1.0 scale)
f_true = readfile("hJ", 5, 1000, 1.0)
f_fit = readfile("mulitipliers", 5, 1000, 1.0)

## plot it 
fig, ax = plt.subplots(1, 2, figsize = (10, 5))
ax[0].plot(f_true, f_fit, 'o')
ax[0].plot([-30,30], [-30,30], 'k-')
ax[0].set(
    xlabel='True parameters', 
    ylabel='Solved parameters')
ax[0].set_title('same x, y axes')

ax[1].plot(f_true, f_fit, 'o')
ax[1].plot([-5,5], [-30,30], 'k-')
ax[1].set(
    xlabel='True parameters', 
    ylabel='Solved parameters')
ax[1].set_title('modified true axis')
plt.suptitle('true hJ vs. solved hJ', fontsize = 20)