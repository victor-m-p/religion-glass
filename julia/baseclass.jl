#module dt
#export add1

# nb: could probably get more specific on Int, Float (i.e. Int32...?)
mutable struct Samp 
    length::Real
    width::Real 
    height::Real
    #m::Int 
    #n::Int
    #n_params::Int = m * n 
    #k::Float64 = 0
    
    function Samp()
        new(1, 1, 1) # default values 
    end 

    function Samp(l::Real, w::Real, h::Real) # constructor 
        if l < 0 || w < 0 || h < 0
            error("cannot have negative values for lengths")
        elseif w < l 
            error("cannot have shorted width than length")
        else 
            new(l, w, h)
        end 

    end  
end 

mutable struct Circle 
    radius::Real
end 

# this does what we'll want 
function Circle_const(s::Samp)
    s.length = s.length+1
end 

# 
function main()
    p = Samp()
    println(p.length)
    Circle_const(p)
    println(p.length) # this does exactly what we need 
end 

main()
#function add1(s::Samp)
#    x = s.m + 1 
#end 

#end # global end 