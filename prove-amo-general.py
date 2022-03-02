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


def recurse_amo(n, n_prev, m, is_lrat, delete=False):
    def print_clause(clause, clause_num, lrat_proof):
        clause_str = " ".join(str(var) for var in clause)
        if is_lrat:
            proof_str = " ".join(str(clause) for clause in lrat_proof)
            print("{} {} 0 {} 0".format(clause_num, clause_str, proof_str))
        else:
            if delete:
                print("d {} 0".format(clause_str))
            else:
                print("{} 0".format(clause_str))

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

    standard_clauses = (
        num_holes_orig * num_birds_orig * (num_birds_orig - 1) // 2 + num_birds_orig
    )
    proof_clauses_base_prev = sum(
        num_holes_i * (num_holes_i + 1) * 15 // 2 + num_holes_i + 1
        for num_holes_i in range(num_holes_prev + 1, num_holes_orig + 1)
    )
    proof_clauses_base_curr = (
        proof_clauses_base_prev + num_holes_prev * num_birds_prev * 15 // 2
    )
    +num_birds_prev
    if is_lrat:
        print("c Clauses {}-{}".format(proof_clauses_base_curr,
            proof_clauses_base_curr + num_holes_curr * num_birds_curr * 15 // 2
            +num_birds_curr))
    current_clause = proof_clauses_base_curr
    for j in range(1, num_holes_curr + 1):

        v = []

        x_0jpk = base_var_prev + 0 * num_holes_prev + j
        for i in range(0, num_birds_curr):
            x_ijk = base_var_curr + i * num_holes_curr + j
            # First, introduce the new x var.
            print("c Introduce x({}, {}, {})".format(i, j, n_prev - 1))

            # Define x_ijk = x_ij(k+1) or (x_i(k+1)(k+1) and x_(k+1)j(k+1))
            x_ijpk = base_var_prev + i * num_holes_prev + j
            x_ipkpk = base_var_prev + i * num_holes_prev + num_holes_prev
            x_pkjpk = base_var_prev + num_holes_prev * num_holes_prev + j

            if i < num_birds_curr - 1:
                current_clause += 1
                print_clause([-x_ijk, x_ijpk, x_ipkpk], current_clause, [])
                current_clause += 1
                print_clause([-x_ijk, x_ijpk, x_pkjpk], current_clause, [])
            else:
                print("c Can skip negated x_ijk for i == k")
            current_clause += 1
            print_clause([x_ijk, -x_ijpk], current_clause, [])
            current_clause += 1
            print_clause([x_ijk, -x_ipkpk, -x_pkjpk], current_clause, [])


            v.append(x_ijk)

        l = 0
        while len(v) > 1:
            if len(v) > m + 1:
                y_ljk = (
                    base_var_curr
                    + num_holes_curr * num_birds_curr
                    + l * num_holes_curr
                    + j
                )
                print("c l={} j={} y_lj={}".format(l, j, y_ljk))
                front = v[:m] + [y_ljk]
                v = v[m:]
                # cnf.extend(CardEnc.atmost(front, encoding=EncType.pairwise))
                for index_1 in range(len(front)):
                    for index_2 in range(index_1 + 1, len(front)):
                        print("c {} {}".format(index_2, index_1))
                        print("c {}".format(front))
                        current_clause += 1
                        print_clause([-front[index_2], -front[index_1]], current_clause, [])
                # Positive constraint
                pos_clause = [front[m]] + front[:-1]
                current_clause += 1
                print_clause(pos_clause, current_clause, [])
                v.insert(0, -y_ljk)
            else:
                print("c final clauses of iter {}".format(j))
                for index_1 in range(len(v)):
                    for index_2 in range(index_1 + 1, len(v)):
                        current_clause += 1
                        print_clause([-v[index_2], -v[index_1]], current_clause, [])
                v = []
            l += 1

    for i in range(0, num_birds_curr):
        # Each bird is still in a hole
        hole_vars = []
        for j in range(1, num_holes_curr + 1):
            x_ijk = base_var_curr + i * num_holes_curr + j
            hole_vars.append(x_ijk)
        print("c Bird {} in a hole on iter {}".format(i, n_prev - 1))
        current_clause += 1
        print_clause(hole_vars, current_clause, [])


def delete_original(n):
    num_birds = n + 1
    num_holes = n
    print("c Delete original")
    # i is hole, j is bird1, k is bird2. Each pair of birds is not in the same hole.
    for i in range(1, num_holes + 1):
        for j in range(0, num_birds):
            if j < (num_birds - 1):  # should not go over the bounds
                for k in range(j + 1, num_birds):
                    var_j = j * num_holes + i
                    var_k = k * num_holes + i
                    print("d -{} -{} 0".format(var_j, var_k))


# End-to-end proof
def full_proof(n, m, is_lrat, is_optimized):
    low_range = 7 if is_optimized else 1
    for n_i in range(n, low_range, -1):
        recurse_amo(n, n_i, m, is_lrat)
        if is_lrat:
            continue
        if n_i < n:
            recurse_amo(n, n_i+1, m, is_lrat, delete=True)
            pass
        else:
            delete_original(n)
            pass
    if not is_optimized:
        print("c Complete")
        print("0")
    if is_optimized:
        unoffset_filename = "trimmed-7.drat"
        offset = n * (n+1) * 2 - 8 * 9 * 2
        num_birds_orig = n + 1
        num_holes_orig = n
        num_birds_prev = 8 + 1
        num_holes_prev = 8
        num_birds_curr = num_birds_prev - 1
        num_holes_curr = num_holes_prev - 1
        base_var_prev = sum(
            2 * num_holes_i * (num_holes_i + 1)
            for num_holes_i in range(num_holes_prev + 1, num_holes_orig + 1)
        )
        base_var_curr = base_var_prev + 2 * num_holes_prev * num_birds_prev
        offset = base_var_curr - 144
        print("c", offset)

        with open(unoffset_filename) as f:
            for line in f:
                fields = line.split()
                for field in fields:
                    if field and field[0] in '-0123456789':
                        int_field = int(field)
                        if int_field != 0:
                            if int_field < 0:
                                int_field -= offset
                            else:
                                int_field += offset
                            print(int_field, end=" ")
                            continue
                    print(field, end=" ")
                print()



if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Call with command line arg: n == num holes, m == size of front clauses,\
 --lrat to output LRAT instead"
        )
    else:
        n = int(sys.argv[1])
        m = int(sys.argv[2])
        is_lrat = "--lrat" in sys.argv
        is_optimized = "--optimized" in sys.argv
        if n <= 7 and is_optimized:
            print("Optimization not enabled for n <= 7 - use kissat/cadical + drat-trim directly.")
        else:
            full_proof(n, m, is_lrat, is_optimized)
