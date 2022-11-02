# https://github.com/eltrompetero/coniii/blob/py3/ipynb/usage_guide.ipynb
from coniii import * 
from coniii.ising_eqn import ising_eqn_5_sym
import matplotlib.pyplot as plt

# Generate example data set.
n = 5  # system size
np.random.seed(0)  # standardize random seed
h = np.random.normal(scale=.1, size=n)           # random couplings (is the below, acc. to Simon)
J = np.random.normal(scale=.1, size=n*(n-1)//2)  # random fields (is the above acc. to Simon)
hJ = np.concatenate((h, J))
p = ising_eqn_5_sym.p(hJ)  # probability distribution of all states p(s)
sisjTrue = ising_eqn_5_sym.calc_observables(hJ)  # exact means and pairwise correlations

allstates = bin_states(n, True)  # all 2^n possible binary states in {-1,1} basis
sample = allstates[np.random.choice(range(2**n), # doesn't have to be a range
                                    size=1000, # how many samples
                                    replace=True, # a value can be selected multiple times
                                    p=p)]  # random sample from p(s)
sisj = pair_corr(sample, concat=True)  # means and pairwise correlations

# Define useful functions for measuring success fitting procedure.
def error_on_correlations(estSisj):
    return np.linalg.norm( sisj - estSisj )

def error_on_multipliers(estMultipliers):
    return np.linalg.norm( hJ - estMultipliers )

def summarize(solver):
    print("Error on sample corr: %E"%error_on_correlations(solver.model.calc_observables(solver.multipliers)))
    print("Error on multipliers: %E"%error_on_multipliers(solver.multipliers))

# Declare and call solver.
solver = Enumerate(sample) # this is were we need to find magic
solver.solve()
summarize(solver)

# Plot comparison of model results with the data.
fig,ax = plt.subplots(figsize=(10.5,4), ncols=2)
ax[0].plot(sisj, solver.model.calc_observables(solver.multipliers), 'o')
ax[0].plot([-1,1], [-1,1], 'k-')
ax[0].set(xlabel='Measured correlations', ylabel='Predicted correlations')

ax[1].plot(hJ, solver.multipliers, 'o')
ax[1].plot([-1,1], [-1,1], 'k-')
ax[1].set(xlabel='True parameters', ylabel='Solved parameters')

fig.subplots_adjust(wspace=.5)

### go through manually ###
## solvers
X = (sample+1)//2 # (1000, 5)
params = X
### calc_obs (2, sym.)
H = params[0:2] # (2, 5)
J = params[2:3] # (1, 5)
#### fast_logsumexp()
energyTerms = np.array([+H[0]+H[1]+J[0], +H[0]-H[1]-J[0], -H[0]+H[1]-J[0], -H[0]-H[1]+J[0],]) # has to be np
Xmx = np.max(energyTerms) # does not work
y = np.exp(X-Xmx).sum() # if coeffs is None
test_1 = np.log(np.abs(y))+Xmx, -1
test_2 = np.log(y)+Xmx, 1
## take the first value
    

### calc_obs (utils)
n = samples.shape[1]
obs = np.zeros((samples.shape[0], n+n*(n-1)//2))
