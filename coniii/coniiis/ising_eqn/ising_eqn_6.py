# MIT License
# 
# Copyright (c) 2019 Edward D. Lee, Bryan C. Daniels
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Equations for 6-spin Ising model.

# Written on 2019/09/19.
from numpy import zeros, exp, array, prod, isnan
from ..enumerate import fast_logsumexp

def calc_observables(params):
    """
    Give all parameters concatenated into one array from lowest to highest order.
    Returns all correlations.
    """
    Cout = zeros((21))
    H = params[0:6]
    J = params[6:21]
    energyTerms = array([    +0, +H[5]+0, +H[4]+0, +H[4]+H[5]+J[14], +H[3]+0, +H[3]+H[5]+J[13], +H[3]+H[4]+J[12], +H[3]+H[4]+H[5]+
    J[12]+J[13]+J[14], +H[2]+0, +H[2]+H[5]+J[11], +H[2]+H[4]+J[10], +H[2]+H[4]+H[5]+J[10]+J[11]+J[14], +
    H[2]+H[3]+J[9], +H[2]+H[3]+H[5]+J[9]+J[11]+J[13], +H[2]+H[3]+H[4]+J[9]+J[10]+J[12], +H[2]+H[3]+H[4]+
    H[5]+J[9]+J[10]+J[11]+J[12]+J[13]+J[14], +H[1]+0, +H[1]+H[5]+J[8], +H[1]+H[4]+J[7], +H[1]+H[4]+H[5]+
    J[7]+J[8]+J[14], +H[1]+H[3]+J[6], +H[1]+H[3]+H[5]+J[6]+J[8]+J[13], +H[1]+H[3]+H[4]+J[6]+J[7]+J[12], +
    H[1]+H[3]+H[4]+H[5]+J[6]+J[7]+J[8]+J[12]+J[13]+J[14], +H[1]+H[2]+J[5], +H[1]+H[2]+H[5]+J[5]+J[8]+J[11], +
    H[1]+H[2]+H[4]+J[5]+J[7]+J[10], +H[1]+H[2]+H[4]+H[5]+J[5]+J[7]+J[8]+J[10]+J[11]+J[14], +H[1]+H[2]+H[3]+
    J[5]+J[6]+J[9], +H[1]+H[2]+H[3]+H[5]+J[5]+J[6]+J[8]+J[9]+J[11]+J[13], +H[1]+H[2]+H[3]+H[4]+J[5]+J[6]+
    J[7]+J[9]+J[10]+J[12], +H[1]+H[2]+H[3]+H[4]+H[5]+J[5]+J[6]+J[7]+J[8]+J[9]+J[10]+J[11]+J[12]+J[13]+J[14], +
    H[0]+0, +H[0]+H[5]+J[4], +H[0]+H[4]+J[3], +H[0]+H[4]+H[5]+J[3]+J[4]+J[14], +H[0]+H[3]+J[2], +H[0]+H[3]+
    H[5]+J[2]+J[4]+J[13], +H[0]+H[3]+H[4]+J[2]+J[3]+J[12], +H[0]+H[3]+H[4]+H[5]+J[2]+J[3]+J[4]+J[12]+J[13]+
    J[14], +H[0]+H[2]+J[1], +H[0]+H[2]+H[5]+J[1]+J[4]+J[11], +H[0]+H[2]+H[4]+J[1]+J[3]+J[10], +H[0]+H[2]+
    H[4]+H[5]+J[1]+J[3]+J[4]+J[10]+J[11]+J[14], +H[0]+H[2]+H[3]+J[1]+J[2]+J[9], +H[0]+H[2]+H[3]+H[5]+J[1]+
    J[2]+J[4]+J[9]+J[11]+J[13], +H[0]+H[2]+H[3]+H[4]+J[1]+J[2]+J[3]+J[9]+J[10]+J[12], +H[0]+H[2]+H[3]+H[4]+
    H[5]+J[1]+J[2]+J[3]+J[4]+J[9]+J[10]+J[11]+J[12]+J[13]+J[14], +H[0]+H[1]+J[0], +H[0]+H[1]+H[5]+J[0]+J[4]+
    J[8], +H[0]+H[1]+H[4]+J[0]+J[3]+J[7], +H[0]+H[1]+H[4]+H[5]+J[0]+J[3]+J[4]+J[7]+J[8]+J[14], +H[0]+H[1]+
    H[3]+J[0]+J[2]+J[6], +H[0]+H[1]+H[3]+H[5]+J[0]+J[2]+J[4]+J[6]+J[8]+J[13], +H[0]+H[1]+H[3]+H[4]+J[0]+
    J[2]+J[3]+J[6]+J[7]+J[12], +H[0]+H[1]+H[3]+H[4]+H[5]+J[0]+J[2]+J[3]+J[4]+J[6]+J[7]+J[8]+J[12]+J[13]+
    J[14], +H[0]+H[1]+H[2]+J[0]+J[1]+J[5], +H[0]+H[1]+H[2]+H[5]+J[0]+J[1]+J[4]+J[5]+J[8]+J[11], +H[0]+H[1]+
    H[2]+H[4]+J[0]+J[1]+J[3]+J[5]+J[7]+J[10], +H[0]+H[1]+H[2]+H[4]+H[5]+J[0]+J[1]+J[3]+J[4]+J[5]+J[7]+J[8]+
    J[10]+J[11]+J[14], +H[0]+H[1]+H[2]+H[3]+J[0]+J[1]+J[2]+J[5]+J[6]+J[9], +H[0]+H[1]+H[2]+H[3]+H[5]+J[0]+
    J[1]+J[2]+J[4]+J[5]+J[6]+J[8]+J[9]+J[11]+J[13], +H[0]+H[1]+H[2]+H[3]+H[4]+J[0]+J[1]+J[2]+J[3]+J[5]+J[6]+
    J[7]+J[9]+J[10]+J[12], +H[0]+H[1]+H[2]+H[3]+H[4]+H[5]+J[0]+J[1]+J[2]+J[3]+J[4]+J[5]+J[6]+J[7]+J[8]+J[9]+
            J[10]+J[11]+J[12]+J[13]+J[14],])
    logZ = fast_logsumexp(energyTerms)[0]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,
 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    Cout[0] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    Cout[1] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,
 0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
    Cout[2] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,
 1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1])
    Cout[3] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,
 0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1])
    Cout[4] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,
 1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])
    Cout[5] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    Cout[6] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
    Cout[7] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
 1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1])
    Cout[8] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,
 0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1])
    Cout[9] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,
 1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])
    Cout[10] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
    Cout[11] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1])
    Cout[12] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1])
    Cout[13] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])
    Cout[14] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,
 0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1])
    Cout[15] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,
 0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1])
    Cout[16] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,
 0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1])
    Cout[17] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,
 0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1])
    Cout[18] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,
 1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1])
    Cout[19] = exp( num[0] - logZ ) * num[1]
    num = fast_logsumexp(energyTerms, [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,
 0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1])
    Cout[20] = exp( num[0] - logZ ) * num[1]
    Cout[isnan(Cout)] = 0.
    return(Cout)

def p(params):
    """
    Give all parameters concatenated into one array from lowest to highest order.
    Returns probabilities of all configurations.
    """
    Cout = zeros((21))
    H = params[0:6]
    J = params[6:21]
    H = params[0:6]
    J = params[6:21]
    Pout = zeros((64))
    energyTerms = array([    +0, +H[5]+0, +H[4]+0, +H[4]+H[5]+J[14], +H[3]+0, +H[3]+H[5]+J[13], +H[3]+H[4]+J[12], +H[3]+H[4]+H[5]+
    J[12]+J[13]+J[14], +H[2]+0, +H[2]+H[5]+J[11], +H[2]+H[4]+J[10], +H[2]+H[4]+H[5]+J[10]+J[11]+J[14], +
    H[2]+H[3]+J[9], +H[2]+H[3]+H[5]+J[9]+J[11]+J[13], +H[2]+H[3]+H[4]+J[9]+J[10]+J[12], +H[2]+H[3]+H[4]+
    H[5]+J[9]+J[10]+J[11]+J[12]+J[13]+J[14], +H[1]+0, +H[1]+H[5]+J[8], +H[1]+H[4]+J[7], +H[1]+H[4]+H[5]+
    J[7]+J[8]+J[14], +H[1]+H[3]+J[6], +H[1]+H[3]+H[5]+J[6]+J[8]+J[13], +H[1]+H[3]+H[4]+J[6]+J[7]+J[12], +
    H[1]+H[3]+H[4]+H[5]+J[6]+J[7]+J[8]+J[12]+J[13]+J[14], +H[1]+H[2]+J[5], +H[1]+H[2]+H[5]+J[5]+J[8]+J[11], +
    H[1]+H[2]+H[4]+J[5]+J[7]+J[10], +H[1]+H[2]+H[4]+H[5]+J[5]+J[7]+J[8]+J[10]+J[11]+J[14], +H[1]+H[2]+H[3]+
    J[5]+J[6]+J[9], +H[1]+H[2]+H[3]+H[5]+J[5]+J[6]+J[8]+J[9]+J[11]+J[13], +H[1]+H[2]+H[3]+H[4]+J[5]+J[6]+
    J[7]+J[9]+J[10]+J[12], +H[1]+H[2]+H[3]+H[4]+H[5]+J[5]+J[6]+J[7]+J[8]+J[9]+J[10]+J[11]+J[12]+J[13]+J[14], +
    H[0]+0, +H[0]+H[5]+J[4], +H[0]+H[4]+J[3], +H[0]+H[4]+H[5]+J[3]+J[4]+J[14], +H[0]+H[3]+J[2], +H[0]+H[3]+
    H[5]+J[2]+J[4]+J[13], +H[0]+H[3]+H[4]+J[2]+J[3]+J[12], +H[0]+H[3]+H[4]+H[5]+J[2]+J[3]+J[4]+J[12]+J[13]+
    J[14], +H[0]+H[2]+J[1], +H[0]+H[2]+H[5]+J[1]+J[4]+J[11], +H[0]+H[2]+H[4]+J[1]+J[3]+J[10], +H[0]+H[2]+
    H[4]+H[5]+J[1]+J[3]+J[4]+J[10]+J[11]+J[14], +H[0]+H[2]+H[3]+J[1]+J[2]+J[9], +H[0]+H[2]+H[3]+H[5]+J[1]+
    J[2]+J[4]+J[9]+J[11]+J[13], +H[0]+H[2]+H[3]+H[4]+J[1]+J[2]+J[3]+J[9]+J[10]+J[12], +H[0]+H[2]+H[3]+H[4]+
    H[5]+J[1]+J[2]+J[3]+J[4]+J[9]+J[10]+J[11]+J[12]+J[13]+J[14], +H[0]+H[1]+J[0], +H[0]+H[1]+H[5]+J[0]+J[4]+
    J[8], +H[0]+H[1]+H[4]+J[0]+J[3]+J[7], +H[0]+H[1]+H[4]+H[5]+J[0]+J[3]+J[4]+J[7]+J[8]+J[14], +H[0]+H[1]+
    H[3]+J[0]+J[2]+J[6], +H[0]+H[1]+H[3]+H[5]+J[0]+J[2]+J[4]+J[6]+J[8]+J[13], +H[0]+H[1]+H[3]+H[4]+J[0]+
    J[2]+J[3]+J[6]+J[7]+J[12], +H[0]+H[1]+H[3]+H[4]+H[5]+J[0]+J[2]+J[3]+J[4]+J[6]+J[7]+J[8]+J[12]+J[13]+
    J[14], +H[0]+H[1]+H[2]+J[0]+J[1]+J[5], +H[0]+H[1]+H[2]+H[5]+J[0]+J[1]+J[4]+J[5]+J[8]+J[11], +H[0]+H[1]+
    H[2]+H[4]+J[0]+J[1]+J[3]+J[5]+J[7]+J[10], +H[0]+H[1]+H[2]+H[4]+H[5]+J[0]+J[1]+J[3]+J[4]+J[5]+J[7]+J[8]+
    J[10]+J[11]+J[14], +H[0]+H[1]+H[2]+H[3]+J[0]+J[1]+J[2]+J[5]+J[6]+J[9], +H[0]+H[1]+H[2]+H[3]+H[5]+J[0]+
    J[1]+J[2]+J[4]+J[5]+J[6]+J[8]+J[9]+J[11]+J[13], +H[0]+H[1]+H[2]+H[3]+H[4]+J[0]+J[1]+J[2]+J[3]+J[5]+J[6]+
    J[7]+J[9]+J[10]+J[12], +H[0]+H[1]+H[2]+H[3]+H[4]+H[5]+J[0]+J[1]+J[2]+J[3]+J[4]+J[5]+J[6]+J[7]+J[8]+J[9]+
            J[10]+J[11]+J[12]+J[13]+J[14],])
    logZ = fast_logsumexp(energyTerms)[0]
    Pout[0] = exp( +0 - logZ )
    Pout[1] = exp( +H[5]+0 - logZ )
    Pout[2] = exp( +H[4]+0 - logZ )
    Pout[3] = exp( +H[4]+H[5]+J[14] - logZ )
    Pout[4] = exp( +H[3]+0 - logZ )
    Pout[5] = exp( +H[3]+H[5]+J[13] - logZ )
    Pout[6] = exp( +H[3]+H[4]+J[12] - logZ )
    Pout[7] = exp( +H[3]+H[4]+H[5]+J[12]+J[13]+J[14] - logZ )
    Pout[8] = exp( +H[2]+0 - logZ )
    Pout[9] = exp( +H[2]+H[5]+J[11] - logZ )
    Pout[10] = exp( +H[2]+H[4]+J[10] - logZ )
    Pout[11] = exp( +H[2]+H[4]+H[5]+J[10]+J[11]+J[14] - logZ )
    Pout[12] = exp( +H[2]+H[3]+J[9] - logZ )
    Pout[13] = exp( +H[2]+H[3]+H[5]+J[9]+J[11]+J[13] - logZ )
    Pout[14] = exp( +H[2]+H[3]+H[4]+J[9]+J[10]+J[12] - logZ )
    Pout[15] = exp( +H[2]+H[3]+H[4]+H[5]+J[9]+J[10]+J[11]+J[12]+J[13]+J[14] - logZ )
    Pout[16] = exp( +H[1]+0 - logZ )
    Pout[17] = exp( +H[1]+H[5]+J[8] - logZ )
    Pout[18] = exp( +H[1]+H[4]+J[7] - logZ )
    Pout[19] = exp( +H[1]+H[4]+H[5]+J[7]+J[8]+J[14] - logZ )
    Pout[20] = exp( +H[1]+H[3]+J[6] - logZ )
    Pout[21] = exp( +H[1]+H[3]+H[5]+J[6]+J[8]+J[13] - logZ )
    Pout[22] = exp( +H[1]+H[3]+H[4]+J[6]+J[7]+J[12] - logZ )
    Pout[23] = exp( +H[1]+H[3]+H[4]+H[5]+J[6]+J[7]+J[8]+J[12]+J[13]+J[14] - logZ )
    Pout[24] = exp( +H[1]+H[2]+J[5] - logZ )
    Pout[25] = exp( +H[1]+H[2]+H[5]+J[5]+J[8]+J[11] - logZ )
    Pout[26] = exp( +H[1]+H[2]+H[4]+J[5]+J[7]+J[10] - logZ )
    Pout[27] = exp( +H[1]+H[2]+H[4]+H[5]+J[5]+J[7]+J[8]+J[10]+J[11]+J[14] - logZ )
    Pout[28] = exp( +H[1]+H[2]+H[3]+J[5]+J[6]+J[9] - logZ )
    Pout[29] = exp( +H[1]+H[2]+H[3]+H[5]+J[5]+J[6]+J[8]+J[9]+J[11]+J[13] - logZ )
    Pout[30] = exp( +H[1]+H[2]+H[3]+H[4]+J[5]+J[6]+J[7]+J[9]+J[10]+J[12] - logZ )
    Pout[31] = exp( +H[1]+H[2]+H[3]+H[4]+H[5]+J[5]+J[6]+J[7]+J[8]+J[9]+J[10]+J[11]+J[12]+J[13]+J[14] - logZ )
    Pout[32] = exp( +H[0]+0 - logZ )
    Pout[33] = exp( +H[0]+H[5]+J[4] - logZ )
    Pout[34] = exp( +H[0]+H[4]+J[3] - logZ )
    Pout[35] = exp( +H[0]+H[4]+H[5]+J[3]+J[4]+J[14] - logZ )
    Pout[36] = exp( +H[0]+H[3]+J[2] - logZ )
    Pout[37] = exp( +H[0]+H[3]+H[5]+J[2]+J[4]+J[13] - logZ )
    Pout[38] = exp( +H[0]+H[3]+H[4]+J[2]+J[3]+J[12] - logZ )
    Pout[39] = exp( +H[0]+H[3]+H[4]+H[5]+J[2]+J[3]+J[4]+J[12]+J[13]+J[14] - logZ )
    Pout[40] = exp( +H[0]+H[2]+J[1] - logZ )
    Pout[41] = exp( +H[0]+H[2]+H[5]+J[1]+J[4]+J[11] - logZ )
    Pout[42] = exp( +H[0]+H[2]+H[4]+J[1]+J[3]+J[10] - logZ )
    Pout[43] = exp( +H[0]+H[2]+H[4]+H[5]+J[1]+J[3]+J[4]+J[10]+J[11]+J[14] - logZ )
    Pout[44] = exp( +H[0]+H[2]+H[3]+J[1]+J[2]+J[9] - logZ )
    Pout[45] = exp( +H[0]+H[2]+H[3]+H[5]+J[1]+J[2]+J[4]+J[9]+J[11]+J[13] - logZ )
    Pout[46] = exp( +H[0]+H[2]+H[3]+H[4]+J[1]+J[2]+J[3]+J[9]+J[10]+J[12] - logZ )
    Pout[47] = exp( +H[0]+H[2]+H[3]+H[4]+H[5]+J[1]+J[2]+J[3]+J[4]+J[9]+J[10]+J[11]+J[12]+J[13]+J[14] - logZ )
    Pout[48] = exp( +H[0]+H[1]+J[0] - logZ )
    Pout[49] = exp( +H[0]+H[1]+H[5]+J[0]+J[4]+J[8] - logZ )
    Pout[50] = exp( +H[0]+H[1]+H[4]+J[0]+J[3]+J[7] - logZ )
    Pout[51] = exp( +H[0]+H[1]+H[4]+H[5]+J[0]+J[3]+J[4]+J[7]+J[8]+J[14] - logZ )
    Pout[52] = exp( +H[0]+H[1]+H[3]+J[0]+J[2]+J[6] - logZ )
    Pout[53] = exp( +H[0]+H[1]+H[3]+H[5]+J[0]+J[2]+J[4]+J[6]+J[8]+J[13] - logZ )
    Pout[54] = exp( +H[0]+H[1]+H[3]+H[4]+J[0]+J[2]+J[3]+J[6]+J[7]+J[12] - logZ )
    Pout[55] = exp( +H[0]+H[1]+H[3]+H[4]+H[5]+J[0]+J[2]+J[3]+J[4]+J[6]+J[7]+J[8]+J[12]+J[13]+J[14] - logZ )
    Pout[56] = exp( +H[0]+H[1]+H[2]+J[0]+J[1]+J[5] - logZ )
    Pout[57] = exp( +H[0]+H[1]+H[2]+H[5]+J[0]+J[1]+J[4]+J[5]+J[8]+J[11] - logZ )
    Pout[58] = exp( +H[0]+H[1]+H[2]+H[4]+J[0]+J[1]+J[3]+J[5]+J[7]+J[10] - logZ )
    Pout[59] = exp( +H[0]+H[1]+H[2]+H[4]+H[5]+J[0]+J[1]+J[3]+J[4]+J[5]+J[7]+J[8]+J[10]+J[11]+J[14] - logZ )
    Pout[60] = exp( +H[0]+H[1]+H[2]+H[3]+J[0]+J[1]+J[2]+J[5]+J[6]+J[9] - logZ )
    Pout[61] = exp( +H[0]+H[1]+H[2]+H[3]+H[5]+J[0]+J[1]+J[2]+J[4]+J[5]+J[6]+J[8]+J[9]+J[11]+J[13] - logZ )
    Pout[62] = exp( +H[0]+H[1]+H[2]+H[3]+H[4]+J[0]+J[1]+J[2]+J[3]+J[5]+J[6]+J[7]+J[9]+J[10]+J[12] - logZ )
    Pout[63] = exp( +H[0]+H[1]+H[2]+H[3]+H[4]+H[5]+J[0]+J[1]+J[2]+J[3]+J[4]+J[5]+J[6]+J[7]+J[8]+J[9]+J[10]+J[11]+J[12]+J[13]+J[14] - logZ )

    return(Pout)
