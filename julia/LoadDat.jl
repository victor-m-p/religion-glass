using DelimitedFiles

# crazy that this just works params
p_true = readdlm("religion-glass/julia/sim_data/hJ_nodes_3_samples_100_scale_0.1.txt", Float64)
samp = readdlm("religion-glass/julia/sim_data/samples_nodes_3_samples_100_scale_0.1.txt", Int64)

# now we can do stuff with it 
