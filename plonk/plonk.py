from .poly import gen_poly
from .constraint import is_satisfied
from .copy_constraint import copy_constraint_simple
import pdb


def verify_naieve(Ql, Qr, Qm, Qo, Qc, a, b, c, witness_y, perm_a, perm_b, perm_c):
    # make sure constarints + witness is statisfied
    assert is_satisfied(Ql, Qr, Qm, Qo, Qc, a, b, c) == True

    # original polynomial

    Xcoef_a = [0, 1]
    Xcoef_b = [len(a), 1]
    Xcoef_c = [2 * len(a), 1]

    # todo: replace with random

    v1 = hash(str(a + b + c))
    v2 = hash(str(c + a + b))

    a_poly = gen_poly(range(0, len(a)), a)
    b_poly = gen_poly(range(0, len(a)), b)
    c_poly = gen_poly(range(0, len(a)), c)
    eval_domain = range(0, len(a) * 3)

    x, Y, Px_a, rlc = copy_constraint_simple(range(0, len(a)), Xcoef_a, a_poly, v1, v2)
    x, Y, Px_b, rlc = copy_constraint_simple(range(0, len(a)), Xcoef_b, b_poly, v1, v2)
    x, Y, Px_c, rlc = copy_constraint_simple(range(0, len(a)), Xcoef_c, c_poly, v1, v2)

    # calcualte permutated polynomial
    x_1, Y_1, Px_a_prime, rlc_1 = copy_constraint_simple(
        range(0, len(a)), perm_a, a_poly, v1, v2
    )
    x_1, Y_1, Px_b_prime, rlc_1 = copy_constraint_simple(
        range(0, len(a)), perm_b, b_poly, v1, v2
    )
    x_1, Y_1, Px_c_prime, rlc_1 = copy_constraint_simple(
        range(0, len(a)), perm_c, c_poly, v1, v2
    )

    assert (
        Px_a[-1] * Px_b[-1] * Px_c[-1]
        == Px_a_prime[-1] * Px_b_prime[-1] * Px_c_prime[-1]
    )
    assert (
        Px_a[0]
        == Px_b[0]
        == Px_c[0]
        == Px_a_prime[0]
        == Px_b_prime[0]
        == Px_c_prime[0]
        == 1
    )
    # todo public input check


def create_proof(a, b, c):
    domain = range(0, len(a) * 3)
    poly = gen_poly(domain, a + b + c)

    return (a, b, c, poly)
