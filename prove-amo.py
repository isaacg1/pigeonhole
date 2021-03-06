# Derive O(n^2) encoding based on AMO(x1, ..., xn) <=> AMO(x1, x2, x3, y) and AMO(not(y), x4, ..., xn)
# Allow different lengths and positions of y.

# Plan to derive with just blocked clause addition and resolution.

# Consider n+1 birds and n holes
# x_ab represents bird a in hole b.

# Input encoding:
# Each bird is in at least one hole
# OR(x_i1, x_i2, ..., x_in), for all 1 <= i <= n+1.
# At most one bird in hole k (AMO(x_1k, x_2k, ..., x_{n+1}k)) encoded by:
# For all i, j birds, hole k,
# not(x_ik) or not(x_jk)

# Desired output encoding:
# Auxiliary variables y.
# Encoding:
# AMO(x_1k, x_2k, x_3k, y) and AMO(not(y), x_4k, ..., x_{n+1}k)


def derive_amo(n):
    num_birds = n + 1
    num_holes = n

    # cnf = CNF()
    cnf = []

    for j in range(1, num_holes + 1):  # [1, n]
        v = []
        for i in range(num_birds):
            x_ij = i * num_holes + j
            v.append(x_ij)
        l = 0
        print("c start iter {}".format(j))
        while len(v) > 1:
            if len(v) > 3:
                y_lj = num_holes * num_birds + l * num_holes + j
                print("c l={} j={} y_lj={}".format(l, j, y_lj))
                front = v[:3] + [y_lj]
                v = v[3:]
                # cnf.extend(CardEnc.atmost(front, encoding=EncType.pairwise))
                for index_1 in range(len(front)):
                    for index_2 in range(index_1 + 1, len(front)):
                        if index_1 > 0 or l == 0:
                            if index_2 < 3:
                                print(
                                    "c Skip {} {} because both are original vars".format(
                                        front[index_1], front[index_2]
                                    )
                                )
                                continue
                        # cnf.append([-front[i], -front[j]])
                        print("c {} {}".format(index_2, index_1))
                        print("c {}".format(front))
                        print("{} {} 0".format(-front[index_2], -front[index_1]))
                # Positive constraint
                print("c Positive constraint")
                print("{} {} {} {} 0".format(front[3], front[0], front[1], front[2]))
                v.insert(0, -y_lj)
            else:
                print("c final clauses of iter {}".format(j))
                for index_1 in range(len(v)):
                    for index_2 in range(index_1 + 1, len(v)):
                        if index_1 > 0 or l == 0:
                            print(
                                "c Skip {} {} because both are original vars".format(
                                    v[index_1], v[index_2]
                                )
                            )
                            continue
                        # cnf.append([-v[i], -v[j]])
                        print("{} {} 0".format(-v[index_1], -v[index_2]))
                v = []
            l += 1


# Prove amo constraints.
# AMO constraints are defined as:
# AMO(x_1k, x_2k, x_3k, y) and AMO(not(y), x_4k, ..., x_{n+1}k)
# where x_ab represents bird a in hole b

# Plan:
# think of x_ij as x_ijn: the bird placement on iteration n.
# Also, y_j -> y_jn
# Define x_ij{n-1} to be x_{i+1}jn or (x_{i+1}nn and x_1jn)
#     Contrast to Cook: x_ij{n-1} <=> x_ijn or (x_inn and x_{n+1}jn)
# Basically, shift all the bird positions down by one.
# Use i=0 as the bird to be removed
# It's first in the q ordering, so it's easier to propagate.
# The standard removal choice fails because q doesn't know about the last x,
# So we can't prove the q_ijn -> q_ij{n-1} step.


def recurse_amo(n, n_prev):
    num_birds_orig = n + 1
    num_holes_orig = n
    num_birds_prev = n_prev + 1
    num_holes_prev = n_prev
    num_birds_curr = num_birds_prev - 1
    num_holes_curr = num_holes_prev - 1
    base_var_prev = sum(
        2 * num_holes_i * (num_holes_i + 1)
        for num_holes_i in range(num_holes_prev + 1, num_holes_orig + 1)
    )
    base_var_curr = base_var_prev + 2 * num_holes_prev * num_birds_prev
    print("c Recurse amo from {} to {}".format(n_prev, n_prev - 1))
    print(
        "c Vars {}-{}".format(
            base_var_curr, base_var_curr + 2 * num_holes_curr * num_birds_curr
        )
    )

    cnf = []

    for j in range(1, num_holes_curr + 1):

        v = []

        x_0jpk = base_var_prev + 0 * num_holes_prev + j
        for i in range(0, num_birds_curr):
            x_ijk = base_var_curr + i * num_holes_curr + j
            x_pijpk = base_var_prev + (i + 1) * num_holes_prev + j
            x_pipkpk = base_var_prev + (i + 1) * num_holes_prev + num_holes_prev

            # First, introduce the new x var.
            print("c Introduce x({}, {}, {})".format(i, j, n_prev - 1))
            # x_ijk <=> x_ijpk or (x_ipkpk and x_pkjpk)

            # x_ijk -> x_pijpk V x_pipkpk
            print("-{} {} {} 0".format(x_ijk, x_pijpk, x_pipkpk))
            # x_ijk -> x_pijpk V x_0jpk
            print("-{} {} {} 0".format(x_ijk, x_pijpk, x_0jpk))
            # x_pijpk -> x_ijk
            print("{} -{} 0".format(x_ijk, x_pijpk))
            # x_pipkpk /\ x_0jpk -> x_ijk
            print("{} -{} -{} 0".format(x_ijk, x_pipkpk, x_0jpk))

            v.append(x_ijk)

        l = 0
        print("c start iter {}".format(j))
        while len(v) > 1:
            if len(v) > 3:
                y_ljk = (
                    base_var_curr
                    + num_holes_curr * num_birds_curr
                    + l * num_holes_curr
                    + j
                )
                print("c l={} j={} y_lj={}".format(l, j, y_ljk))
                front = v[:3] + [y_ljk]
                v = v[3:]
                # cnf.extend(CardEnc.atmost(front, encoding=EncType.pairwise))
                for index_1 in range(len(front)):
                    for index_2 in range(index_1 + 1, len(front)):
                        # cnf.append([-front[i], -front[j]])
                        print("c {} {}".format(index_2, index_1))
                        print("c {}".format(front))
                        print("{} {} 0".format(-front[index_2], -front[index_1]))
                # Positive constraint
                print("c Positive constraint")
                print("{} {} {} {} 0".format(front[3], front[0], front[1], front[2]))
                v.insert(0, -y_ljk)
            else:
                print("c final clauses of iter {}".format(j))
                for index_1 in range(len(v)):
                    for index_2 in range(index_1 + 1, len(v)):
                        if index_1 == 0:  # bridging the gap
                            print("{} {} {} 0".format(x_0jpk, -v[index_1], -v[index_2]))
                        print("{} {} 0".format(-v[index_1], -v[index_2]))
                v = []
            l += 1

        # # write to file
        # # cnf.to_file('amo.drat')

        # # print to terminal
        # for c in cnf.clauses:
        #   print(" ".join(str(e) for e in c) + " 0")

    for i in range(0, num_birds_curr):
        # Each bird is still in a hole
        hole_vars = []
        for j in range(1, num_holes_curr + 1):
            x_ijk = base_var_curr + i * num_holes_curr + j
            hole_vars.append(x_ijk)
        clause_str = " ".join(str(var) for var in hole_vars)
        print("c Bird {} in a hole on iter {}".format(i, n_prev - 1))
        print("{} 0".format(clause_str))


# Q: why some deleted clauses does not exist in the original formula
def delete_original(n):
    num_birds = n + 1
    num_holes = n
    print("c Delete original")
    # i is hole, j is bird1, k is bird2. Each pair of birds is not in the same hole.
    for i in range(1, num_holes + 1):
        for j in range(0, num_birds):
            for k in range(j + 1, num_birds):  # should not go over the bounds
                var_j = j * num_holes + i
                var_k = k * num_holes + i
                print("d -{} -{} 0".format(var_j, var_k))


def delete_derive(n):
    num_birds = n + 1
    num_holes = n
    # cnf = CNF()
    cnf = []
    for j in range(1, num_holes + 1):  # [1, n]
        v = []
        for i in range(num_birds):
            x_ij = i * num_holes + j
            v.append(x_ij)
        l = 0
        while len(v) > 1:
            if len(v) > 3:
                y_lj = num_holes * num_birds + l * num_holes + j
                front = v[:3] + [y_lj]
                v = v[3:]
                for index_1 in range(len(front)):
                    for index_2 in range(index_1 + 1, len(front)):
                        print("d {} {} 0".format(-front[index_2], -front[index_1]))
                # Positive constraint
                print("d {} {} {} {} 0".format(front[3], front[0], front[1], front[2]))
                v.insert(0, -y_lj)
            else:
                for index_1 in range(len(v)):
                    for index_2 in range(index_1 + 1, len(v)):
                        print("d {} {} 0".format(-v[index_1], -v[index_2]))
                v = []
            l += 1
    # From generate
    for i in range(0, num_birds):
        vars_in_clause = []
        for j in range(1, num_holes + 1):
            vars_in_clause.append(i * num_holes + j)
        clause_str = " ".join(str(v) for v in vars_in_clause)
        print("d {} 0".format(clause_str))


def delete_recursive(n, n_prev):
    num_birds_orig = n + 1
    num_holes_orig = n
    num_birds_prev = n_prev + 1
    num_holes_prev = n_prev
    num_birds_curr = num_birds_prev - 1
    num_holes_curr = num_holes_prev - 1
    base_var_prev = sum(
        2 * num_holes_i * (num_holes_i + 1)
        for num_holes_i in range(num_holes_prev + 1, num_holes_orig + 1)
    )
    base_var_curr = base_var_prev + 2 * num_holes_prev * num_birds_prev
    cnf = []
    for j in range(1, num_holes_curr + 1):
        v = []
        x_0jpk = base_var_prev + 0 * num_holes_prev + j
        for i in range(0, num_birds_curr):
            x_ijk = base_var_curr + i * num_holes_curr + j
            x_pijpk = base_var_prev + (i + 1) * num_holes_prev + j
            x_pipkpk = base_var_prev + (i + 1) * num_holes_prev + num_holes_prev

            print("d -{} {} {} 0".format(x_ijk, x_pijpk, x_pipkpk))
            print("d -{} {} {} 0".format(x_ijk, x_pijpk, x_0jpk))
            print("d {} -{} 0".format(x_ijk, x_pijpk))
            print("d {} -{} -{} 0".format(x_ijk, x_pipkpk, x_0jpk))

            v.append(x_ijk)

        l = 0
        while len(v) > 1:
            if len(v) > 3:
                y_ljk = (
                    base_var_curr
                    + num_holes_curr * num_birds_curr
                    + l * num_holes_curr
                    + j
                )
                front = v[:3] + [y_ljk]
                v = v[3:]
                for index_1 in range(len(front)):
                    for index_2 in range(index_1 + 1, len(front)):
                        print("d {} {} 0".format(-front[index_2], -front[index_1]))
                print("d {} {} {} {} 0".format(front[3], front[0], front[1], front[2]))
                v.insert(0, -y_ljk)
            else:
                for index_1 in range(len(v)):
                    for index_2 in range(index_1 + 1, len(v)):
                        if index_1 == 0:  # bridging the gap
                            print(
                                "d {} {} {} 0".format(x_0jpk, -v[index_1], -v[index_2])
                            )
                        print("d {} {} 0".format(-v[index_1], -v[index_2]))
                v = []
            l += 1


# End-to-end proof
def full_proof(n):
    derive_amo(n)
    #delete_original(n)
    for n_i in range(n, 1, -1):
        recurse_amo(n, n_i)
        if n_i < n:
            delete_recursive(n, n_i + 1)
        else:
            delete_derive(n)
    print("c Complete")


# End-to-end proof
# def full_proof(n):
#   derive_amo(n)
#   for n_i in range(n, 1, -1):
#       recurse_amo(n, n_i)
#   print("c Complete")

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print("Call with command line arg: n == num holes")
    else:
        n = int(sys.argv[1])
        full_proof(n)
