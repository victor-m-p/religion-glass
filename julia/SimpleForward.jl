# https://www.youtube.com/watch?v=DfKKTE9XU0Q&t=322s
using Base 

# basic struct class for dual number
struct DualNumber{T}
    real::T;
    dual::T;
end 

# overflow multiplication 
# in the real part we have normal multiplication 
# in the derivative part we have the rule 
Base.:*(x::DualNumber, y::DualNumber) = DualNumber(x.real * y.real, x.real * y.dual + x.dual * x.real)

function pushforward(f, primal::Real, tangent::Real)
    input = DualNumber(primal, tangent)
    output = f(input)
    primal_out = output.real 
    tangent_out = output.dual 
    return primal_out, tangent_out 
end 

function derivative(f, x::Real)
    v = one(x)
    _, df_dx = pushforward(f, x, v)
    return df_dx
end 

# define function
f(x) = x * x

# point at evaluation
x_point = 3 

# get derivative 
derivative(f, x_point)

## the idea is that we have taught it how to do derivatives now 
## so we do not have to specify the derivatives manually 
## how are the derivatives specified in Simon code?
## yes, so there we specify both 
### (a) the function to minimize k 
### (b) the way to get the derivative of k 
### here, the plan would be to only specify how to minimize k and let it figure it out 

# more complicated case 
