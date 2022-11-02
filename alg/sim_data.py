import numpy as np
import itertools 

# taken from enumerate
def fast_logsumexp(X, coeffs=None):
    """Simplified version of logsumexp to do correlation calculation in Ising equation
    files. Scipy's logsumexp can be around 10x slower in comparison.
    
    Parameters
    ----------
    X : ndarray
        Terms inside logs.
    coeffs : ndarray
        Factors in front of exponentials. 

    Returns
    -------
    float
        Value of magnitude of quantity inside log (the sum of exponentials).
    float
        Sign.
    """

    Xmx = max(X)
    if coeffs is None:
        y = np.exp(X-Xmx).sum()
    else:
        y = np.exp(X-Xmx).dot(coeffs)

    if y<0:
        return np.log(np.abs(y))+Xmx, -1.
    return np.log(y)+Xmx, 1.

# could probably be made much quicker
def keep_sign(x, condition):
        if condition == True: 
                return x
        elif condition == False: 
                return -x
        else: 
                return("Invalid argument")

# the main function
def p_dist(h, J):
    # setup 
    n_nodes = len(h)
    n_rows = 2**n_nodes
    Pout = np.zeros((n_rows))
    
    ## hJ
    hJ = np.concatenate((h, J))
    
    ## put h, J into array
    parameter_arr = np.repeat(hJ[np.newaxis, :], n_rows, axis=0)

    ## True/False for h
    h_combinations = list(itertools.product([True, False], repeat = n_nodes))

    ## True/False for J 
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
    summed_arr = np.sum(flipped_arr, axis = 1) 
    
    ## logsumexp
    logsumexp_arr = fast_logsumexp(summed_arr)[0] # where is this function
    logsumexp_arr

    ## last step
    for num, ele in enumerate(list(summed_arr)):
        Pout[num] = np.exp(ele - logsumexp_arr)

    ## return stuff
    return Pout[::-1]