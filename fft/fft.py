#!/usr/bin/env sage -python

import pdb 
from ethsnarks.numbertheory import inverse_mod

from py_ecc.bn128.bn128_field_elements import FQ as GF

from ethsnarks import field

p = field.FQ(field.SNARK_SCALAR_FIELD).n


def roots_of_unity(order):
     a = field.FQ(5)
     p = field.FQ(field.SNARK_SCALAR_FIELD)
     return [a**(i*(p-1)/order) for i in range(order)]

def eval(coef, x, p, step_size = 1, start_power = 0 ):
    res = []
    power = x**start_power
    for i in coef:
        res.append((i * power))
        power = (power * x**step_size)
    return(sum(res) % p )


def test_eval():
    assert(eval([3,0,1], 0, 5) == 3)
    assert(eval([3,0,1], 1, 5) == 4)
    assert(eval([3,0,1], 2, 5) == 2)

def find_sub_group(p):
    pdb.set_trace()

def sub_group(p, g):
    domain = [1]
    g_ = g
    while (g_ != 1):
        g_ = g_*g % p
        domain.append(g_)

def fft(p, domain, poly):

    if len(poly) == 1 : 
        return(poly)

    p_even = poly[::2]
    p_odd = poly[1::2]
    domain_positive = domain[::2]

    L = fft(p,domain_positive,p_even)

    R = fft(p,domain_positive,p_odd)

    p_x = []
    p_x_minus_1 = [] 

    for i, (x , y) in enumerate(zip(L,R)): 

        
        y_times_root = y*domain[i].n

        p_x.append((x + y_times_root) % p)
        p_x_minus_1.append((x - y_times_root) % p)

    result = [str(x) + str(y) for x, y in zip(p_x, p_x_minus_1)]

    return(p_x + p_x_minus_1)

def ifft(p, domain, evaluation):
    vals = fft(p, domain, evaluation)

    return([x * inverse_mod(len(vals), p) % p for x in [vals[0]] + vals[1:][::-1]])

def fft_div(poly1, poly2):
    domain = roots_of_unity(4)
    print(max(len(poly1), len(poly2)))
    print(domain)
    poly1_fs = fft(p,domain, poly1)
    poly2_fs = fft(p,domain, poly2)
    res = []
    for x,y in zip(poly1_fs, poly2_fs):
        x = field.FQ(x)
        y = field.FQ(y)
        res.append((x/y).n)
    res = ifft(p,domain,res)
    return(res)

def test_mul_poly():
    # (x + 1) **2
    a = [1,1,0,0,0,0,0,0]
    b = [1,1,0,0,0,0,0,0]
    domain = [1,85,148,111,336,252,189,226]
    p = 337 

    a_fft = fft(p, domain, a)
    b_fft = fft(p, domain, b) 
    c = [a*b for a, b in zip (a_fft, b_fft)]


 
    res = ifft(p, domain, c)
    assert(res == [1, 2, 1, 0, 0, 0, 0, 0])

def test_mul():
    a = [3,5,2,1,0,0,0,0]
    b = [5,9,8,1,0,0,0,0]
    domain = [1, 85,148,111,336,252,189,226]
    p = 337 

    a_fft = fft(p, domain, a)
    b_fft = fft(p, domain, b)

    a_b_fft = [a*b for a, b in zip (a_fft, b_fft)]
    res = ifft(p, domain, a_b_fft)
    for i,x in enumerate(res):    
        res[i] = x % 10 
        if(int(x /10) != 0):
            res[i+1] += int(x / 10)


    assert(res == [5, 3, 4, 4, 7, 3, 2, 0])

def test_fft():
    p = 337
    domain = [1, 85,148,111,336,252,189,226]
    poly = [3,1,4,1,5,9,2,6]
    result = []

    p_x = fft(p, domain, poly)

    for x in domain: 
        result.append(eval(poly, x, p, 1, 0))

   
    assert(p_x == result)

def test_ifft():
    p = 337
    domain = [1, 85,148,111,336,252,189,226]
    poly = [3,1,4,1,5,9,2,6]
    result = []

    p_x = fft(p, domain, poly)

    result = ifft(p, domain, p_x)
 
    assert(result == poly)

def test_constant_add():
    a = [1,1,0,0,0,0,0,0]
    b = [1,1,0,0,0,0,0,0]
    domain = [1,85,148,111,336,252,189,226]
    p = 337

    constant = 330

    a_fft = fft(p, domain, a)
    b_fft = fft(p, domain, b)
    c = [a*b for a, b in zip (a_fft, b_fft)]

    c = [a + constant for a in c]

    res = ifft(p, domain, c)

    assert(res == [331, 2, 1, 0, 0, 0, 0, 0])

def test_poly_add():
    a = [1,1,0,0,0,0,0,0]
    b = [1,1,0,0,0,0,0,0]
    domain = [1,85,148,111,336,252,189,226]
    p = 337


    a_fft = fft(p, domain, a)
    b_fft = fft(p, domain, b)
    c = [a*b for a, b in zip (a_fft, b_fft)]

    c = [a + b for a, b in zip(c, a_fft)]

    res = ifft(p, domain, c)

    assert(res == [2, 3, 1, 0, 0, 0, 0, 0])

def test_degree_reduction():
    a = [1,0,0,0,0,0,0,1]
    b = [0,1,0,0,0,0,0,0]
    domain = [1,85,148,111,336,252,189,226]
    p = 337

    constant = 330

    a_fft = fft(p, domain, a)
    b_fft = fft(p, domain, b)
    c = [a*b for a, b in zip (a_fft, b_fft)]



    res = ifft(p, domain, c)

    assert(res == [1, 1, 0, 0, 0, 0, 0, 0])




if __name__ == "__main__":

    test_fft()
    test_ifft()
    test_mul()
    test_mul_poly()
    test_constant_add()
    test_poly_add()
    test_degree_reduction()
