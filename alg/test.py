import numpy as np 
x = np.zeros([2, 2])

filename = "test"
N = 5
C = 3
S = 2
def write_txt_multiline(filename, dataobj): 
    with open(f"sim_data/{filename}_nodes_{N}_samples_{C}_scale_{S}.txt", "w") as txt_file:
        for line in dataobj: 
            print(line)
            #txt_file.write(str(line) + "\n")
write_txt_multiline(filename, x)
x[0][0] = -1
x[1][0] = 1
np.savetxt("test.txt", x.astype(int), fmt="%i")