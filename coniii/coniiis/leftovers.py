
### code starts here ###
# setup
n_nodes = 3
n_samples = 100
np.random.seed(0)  
n_rows = 2**n_nodes
Pout = np.zeros((n_rows))

# generate h, J
h = np.random.normal(scale=.1, size=n_nodes)           
J = np.random.normal(scale=.1, size=n_nodes*(n_nodes-1)//2) 
hJ = np.concatenate((h, J))

# put h, J into array
parameter_arr = np.repeat(hJ[np.newaxis, :], n_rows, axis=0)

# could probably be made much quicker
def keep_sign(x, condition):
        if condition == True: 
                return x
        elif condition == False: 
                return -x
        else: 
                return("Invalid argument")

# True/False for h
h_combinations = list(itertools.product([True, False], repeat = n_nodes))

# True/False for J 
J_list = []
for i in h_combinations: 
    J_line = list(itertools.combinations(i, 2))
    J_list.append(J_line)
    
J_combinations = []
for i in J_list: 
    J_line = [True if x == y else False for x, y in i]
    J_combinations.append(J_line)

# combine these two things
J_array = np.array(J_combinations)
h_array = np.array(h_combinations)
condition_arr = np.concatenate((h_array, J_array), axis = 1) # what if this was just +1 and -1

lst_rows = []
for row_param, row_condition in zip(parameter_arr, condition_arr): 
    flipped_row = [keep_sign(x, y) for x, y in zip(row_param, row_condition)]
    lst_rows.append(flipped_row)

flipped_arr = np.array(lst_rows)
summed_arr = np.sum(flipped_arr, axis = 1) # 8 states

## logsumexp
logsumexp_arr = fast_logsumexp(summed_arr)[0] # where is this function
logsumexp_arr

## last step
for num, ele in enumerate(list(summed_arr)):
    Pout[num] = np.exp(ele - logsumexp_arr)

## return stuff
Pout = Pout[::-1]

## return stuff
return(Pout) # and there it is ... 

#### check whether we get the same with their stuff ####
H = h
J = J
energyTerms = np.array([
    +H[0]+H[1]+H[2]+J[0]+J[1]+J[2], 
    +H[0]+H[1]-H[2]+J[0]-J[1]-J[2], 
    +H[0]-H[1]+H[2]-J[0]+J[1]-J[2], 
    +H[0]-H[1]-H[2]-J[0]-J[1]+J[2], 
    -H[0]+H[1]+H[2]-J[0]-J[1]+J[2], 
    -H[0]+H[1]-H[2]-J[0]+J[1]-J[2], 
    -H[0]-H[1]+H[2]+J[0]-J[1]-J[2], 
    -H[0]-H[1]-H[2]+J[0]+J[1]+J[2],])

# identical energyTerms # 
energyTerms
summed_arr

# logsumexp
logZ = fast_logsumexp(energyTerms)[0]
logZ
logsumexp_arr

# pout
sPout = np.zeros((n_rows))
sPout[0] = np.exp( +H[0]+H[1]+H[2]+J[0]+J[1]+J[2] - logZ )
sPout[1] = np.exp( +H[0]+H[1]-H[2]+J[0]-J[1]-J[2] - logZ )
sPout[2] = np.exp( +H[0]-H[1]+H[2]-J[0]+J[1]-J[2] - logZ )
sPout[3] = np.exp( +H[0]-H[1]-H[2]-J[0]-J[1]+J[2] - logZ )
sPout[4] = np.exp( -H[0]+H[1]+H[2]-J[0]-J[1]+J[2] - logZ )
sPout[5] = np.exp( -H[0]+H[1]-H[2]-J[0]+J[1]-J[2] - logZ )
sPout[6] = np.exp( -H[0]-H[1]+H[2]+J[0]-J[1]-J[2] - logZ )
sPout[7] = np.exp( -H[0]-H[1]-H[2]+J[0]+J[1]+J[2] - logZ )

