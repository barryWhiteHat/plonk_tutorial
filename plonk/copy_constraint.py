from .poly import polynomial_eval


def copy_constraint_simple(eval_domain, Xcoef, Ycoef, v1, v2):
    Px = [1]
    Y = []
    rlc = []
    x = []

    for i in range(0, len(eval_domain)):
        x.append(polynomial_eval(Xcoef, eval_domain[i]))
        Y.append(polynomial_eval(Ycoef, x[i]))

        rlc.append(v1 + x[i] + v2 * Y[i])
        Px.append(Px[i] * (v1 + x[i] + v2 * Y[i]))

    return (x, Y, Px, rlc)


def find_permutation(wires):
    # This function takes an array "wires" of arbitrary values and returns an
    # array with shuffles the indices of "wires" for repeating values
    size = len(wires)
    permutation = [i for i in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            if wires[i] == wires[j]:
                permutation[i], permutation[j] = permutation[j], permutation[i]
                break
    return permutation
