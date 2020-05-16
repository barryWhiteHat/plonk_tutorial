
from poly import * 

def copy_constraint_simple(eval_domain, Xcoef, Ycoef, v1, v2) : 
    Px = [1]
    Y = []
    rlc = []
    x = []
    import pdb

    for i in range(0,len(eval_domain)):
        x.append(eval(Xcoef , eval_domain[i]))
        try:
            Y.append(eval(Ycoef, x[i]))
        except:
            pdb.set_trace()
        rlc.append(v1 + x[i] + v2*Y[i])
        Px.append(Px[i] * (v1 + x[i] + v2*Y[i]))

    return(x, Y, Px, rlc)

def find_permutation(copies, eval_domain):

    perm = lagrange(eval_domain,copies)
    perm = [float(x) for x in reversed(perm.coefficients)]
    return(perm)

