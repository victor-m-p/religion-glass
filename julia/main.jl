include("baseclass.jl")

using .dt # import module 

# main function
function main(m, n) 
    p = dt.Samp(
        m=m, 
        n=n) # instantiate instance of the class
    println(p.m)
    println(p.n)
    println(p.n_params)
    println(p.k)
end 

main(3, 2)