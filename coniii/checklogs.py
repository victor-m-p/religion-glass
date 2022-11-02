import numpy as np 
import matplotlib.pyplot as plt
import os 
import re

## all the files
dir_list = os.listdir("logs")

## regex patterns
p_int = "\d+"
p_float = "\d+.\d+"
p_sci = "\d+.\d+e-\d+"

nan_list = []
time_list = []
mult_list = []
corr_list = []

## read data
for x in dir_list: 
    print(x)
    f = open(f"logs/{x}")
    y = list(f)
    nan_list.append(re.findall(p_int, y[-1:][0])[0])
    time_list.append(re.findall(p_float, y[-2:][0])[0])
    mult_list.append(re.findall(p_sci, y[-4:][0])[0])
    corr_list.append(re.findall(p_sci, y[-5:][0])[0])

## clean it 
nan_list = [int(x) for x in nan_list]
time_list = [float(x) for x in time_list]
mult_list = [float(x) for x in mult_list]
corr_list = [float(x) for x in corr_list]

## basic plots
plt.scatter(nan_list, time_list) # time up
plt.xlabel("number NA (out of 1000)")
plt.ylabel("time (seconds)")
plt.suptitle("number NA vs. time (5 x 1000)")
plt.savefig("figs/nan_time.jpeg")

plt.scatter(nan_list, mult_list) # error up
plt.xlabel("number NA (out of 1000)")
plt.ylabel("multiplier error")
plt.suptitle("number NA vs multiplier error")
plt.savefig("figs/nan_mult.jpeg")

plt.scatter(nan_list, corr_list) # error up
plt.xlabel("number NA (out of 1000)")
plt.ylabel("correlation error")
plt.suptitle("number NA vs correlation error")
plt.savefig("figs/nan_corr.jpeg")