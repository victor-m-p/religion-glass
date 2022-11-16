using Statistics 
using Random

# n params, s samples, v scaling of params 
n = 5 # i (outer loop)
s = 100 # j (inner loop)
v = 1 

# generate true params 
x = randn(Float64, n) # with mean 0 and sd 1 
x = x*v # looks different, but says same type 

# generate fake data based on params 
# our version is deterministic
# not sure what Simon is doing actually (unfortunately)
n = 3
s = 5
obs = Array{Float64}(undef, s, n)
for [ for i in n, for j in s]



for i in 
rand()