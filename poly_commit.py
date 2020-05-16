from py_ecc.bn128.bn128_curve import multiply, add, G1, G2 , FQ, neg
from py_ecc.bn128.bn128_pairing import pairing
import pdb

from poly import eval


def powers_of_tau(_secret, depth):
    g_1 = [G1]
    g_2 = [G2, multiply(G2, _secret)]
    secret = _secret    
    for i in range(0,depth):
        g_1.append(multiply(G1,secret))
        secret = secret*_secret
    return(g_1, g_2)

def poly_commit(poly, g):
    res = None
    for i,x in enumerate(poly):
        # deal with negitive numbers
        if(x) < 0:
            x = x * -1
            res = add(res, neg(multiply(g[i], x)))
        else:
            res = add(res, multiply(g[i], x))
    return(res)



def test_poly_commit():

    p = [5,0,2,1]

    g1, g2 = powers_of_tau(1234, len(p))

    a = [293]
    a_commit = poly_commit(a, g1)
 

    p_commit = poly_commit(p, g1)
    q = [48,8,1]

    q_commit = poly_commit(q, g1)


    x = [0, 1]
    
    x_commit = poly_commit(x, g2)  


    z = [6]
    z_commit = poly_commit(z,g2)

    # evaluate the polynomials
    # p - a = q*(x-z)

    lhs = eval(p,z[0]) - eval(a,z[0]) 
    rhs =  eval(q,z[0]) * (eval(x,z[0]) - z[0])

    assert(lhs == rhs)


    lhs = pairing(G2, add(p_commit,neg(a_commit))) 
    rhs = pairing(add(x_commit,neg(z_commit)), q_commit)

    assert(lhs == rhs)

def test_mul():

    a = multiply(G1, secret_1) 
    a = multiply(a, secret_2)

    b = multiply(G1, secret_2)
    b = multiply(b, secret_1)

    ## its homomorphic
    assert(a == b)

def test_pairing():
    secret_1 = 1232
    secret_2 = 123123

    g_1 = multiply(G1,secret_1)

    g_2 = multiply(G2,secret_2)

    res = pairing(g_2, g_1)

    g_1 = multiply(G1,secret_2)

    g_2 = multiply(G2,secret_1)

    # we flip it and it still equals its homomorphic. 
    assert(res == pairing(g_2, g_1))
