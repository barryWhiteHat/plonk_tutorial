import pdb

from poly_commit import test_poly_commit, test_pairing, test_mul

from poly import *
from constraint import * 
from copy_constraint import *
from sample_problem import *
from plonk import * 
# evaluate polynomial
# coef are coefficients
# x is the evaluation point
#polynmial looks like coef[0] + coef[1].x + coef[2].x**2

DEBUG = False

def test_addition():
    # constraints
    Ql = []
    Qr = []
    Qm = []
    Qo = []
    Qc = []

    Ql, Qr, Qm, Qo, Qc = add_add_constarint(Ql, Qr, Qm, Qo, Qc)

    # witness
    a = [0]
    b = [1]
    c = [1]

    assert ( is_satisfied(Ql, Qr, Qm, Qo, Qc, a, b, c) == True)


def test_mul():

    # constraints
    Ql = []
    Qr = []
    Qm = []
    Qo = []
    Qc = []

    Ql, Qr, Qm, Qo, Qc = add_mul_constarint(Ql, Qr, Qm, Qo, Qc)

    # witness
    a = [1]
    b = [1]
    c = [1]

    assert ( is_satisfied(Ql, Qr, Qm, Qo, Qc, a, b, c) == True)

def test_constant_mul():

    # constraints
    Ql = [0]
    Qr = [0]
    Qm = [1]
    Qo = [0]
    Qc = [-10]

    # witness
    a = [10]
    b = [1]
    c = [10]

    assert ( is_satisfied(Ql, Qr, Qm, Qo, Qc, a, b, c) == True)


def test_constant_add():
    # constraints
    Ql = [1]
    Qr = [1]
    Qm = [0]
    Qo = [0]
    Qc = [-10]

    # witness
    a = [10]
    b = [0]
    c = [10]

    assert ( is_satisfied(Ql, Qr, Qm, Qo, Qc, a, b, c) == True)

def test_eval():
    x = [1]
    assert(eval([1,1,1],2) == 7)
    assert(eval([-2, 7, -5, 1], 0) == -2)
    assert(eval([-2, 7, -5, 1], 1) == 1)
    assert(eval([-2, 7, -5, 1], 2) == 0)
    assert(eval([-2, 7, -5, 1], 3) == 1)

def test_copy_constraint_simple():
    Ycoef = [-2 , 7, -5 , 1]
    eval_domain = [0, 1, 2, 3]
    #y =     0 + 1x
    Xcoef = [0, 1]

    v1 = 3
    v2 = 2

    x, Y , Px_1, rlc = copy_constraint_simple(eval_domain, Xcoef, Ycoef, v1, v2)

   
    copies = [0,3,2,1]

    Xcoef = find_permutation(copies, eval_domain)


    eval_domain = [0, 1, 2, 3]

    x, Y , Px, rlc = copy_constraint_simple(eval_domain, Xcoef, Ycoef, v1, v2)

    assert(Px_1[4] == Px[4])

def test_setup_prove_verify():
    Ql, Qr, Qm, Qo, Qc, perm_a, perm_b , perm_c, copy_constraints = setup()
    a,b,c = gen_witness(3)
    assert(is_satisfied(Ql,Qr,Qm,Qo,Qc,a,b,c))

    x, x , x , poly = create_proof(a, b , c)
    
    verify_naieve(Ql, Qr, Qm, Qo, Qc, a, b, c, poly, perm_a, perm_b, perm_c)

def test_polynomial_division():
    poly = [5 - 293, 0, 2, 1]
    q = [-6 , 1]

    for i in range (0,1000):
        if eval(poly, i) == 293:
            print(i)
            break

    flag, result = polynomial_division(poly, q)
    assert(flag)
    assert(result ==  [1.0, 8.0, 48.0])

def test_permutation():


    # from copy_constraint import find_permutation
    # from test import test_permutation
    # from poly import eval

    witness = [3, 9, 27, 1, 1, 30, 3, 3, 3, 5, 35, 5, 9, 27, 30, 5, 35, 35] 
    eval_domain = [i for i in range(0,len(witness))]
    witness_x_1 = find_permutation(eval_domain, eval_domain)

    witness_y = find_permutation(witness, eval_domain)


    for i, val in enumerate(witness):
        assert(val == eval(witness_y, i))

if __name__ == "__main__":
    test_permutation()
    test_addition()
    test_mul()
    test_constant_mul()
    test_constant_add()
    test_eval()
    test_copy_constraint_simple()
    test_setup_prove_verify()
    test_polynomial_division()
    test_pairing()
    test_poly_commit()
