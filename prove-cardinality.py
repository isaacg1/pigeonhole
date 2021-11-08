# Derive the formula where we have auxiliary variables representing
# "a bird with index <= i is in hole j"
# Plan to derive with just blocked clause addition and resolution.

# x_ab represents bird a in hole b.

# Input encoding:
# At most one bird in hole k encoded by:
# For all i, j birds, k hole,
# not(x_ik) or not(x_jk)

# Desired output encoding:
# Auxiliary variables q_ab.
# q_ab represents "a bird with index <= a is in hole b".
# Encoding:
# For all i birds, j hole,
# not(q_ij) or q_{i-1}j or x_ij
# not(q_{i-1}j) or q_ij
# not(x_ij) or q_ij
# not(q_{i-1}j) or not(x_ij)

# q_ij encoded as num_holes * num_birds + i * num_holes + j
# ranges from num_holes * num_birds + 1 to 2 * num_holes * num_birds


def derive_cardinality(n):
    num_birds = n + 1
    num_holes = n
    print("c Derive cardinality constraints from standard.")
    print("c Vars {}-{}".format(num_holes * num_birds, 2 * num_holes * num_birds))
    for j in range(1, num_holes + 1):
        for i in range(0, num_birds):
            x_ij = i * num_holes + j
            q_ij = num_holes * num_birds + i * num_holes + j
            if i == 0:
                # Special case: q_ij is equivalent to x_ij
                # Add q_ij by extension. Both clauses are blocked on q_ij.
                # q_ij -> x_ij
                print("-{} {} 0".format(q_ij, x_ij))
                # x_ij -> q_ij
                print("{} -{} 0".format(q_ij, x_ij))
            else:
                # q_mij is q_{i-1}j
                q_mij = num_holes * num_birds + (i - 1) * num_holes + j
                # First, add q_ij by extension.
                # q_ij <=> x_ij or q_mij
                # All clauses are blocked on q_ij
                # q_ij -> x_ij or q_mij
                print("-{} {} {} 0".format(q_ij, x_ij, q_mij))
                # x_ij -> q_ij
                print("{} -{} 0".format(q_ij, x_ij))
                # q_mij -> q_ij
                print("{} -{} 0".format(q_ij, q_mij))

                # Second, derive constraint via RAT - drat-trim says it works.
                print("-{} -{} 0".format(q_mij, x_ij))


# Prove cardinality constraints.
# Cardinality constraints are defined as:

# x_ij represents bird i in hole j.
# q_ij represents a bird <=i in hole j.
# Constraints:
# x_ij -> q_ij
# q_{i-1}j -> q_ij
# q_ij -> x_ij or q_{i-1}j
# not (x_ij and q_{i-1}j)

# Plan: think of x_ij as x_ijn: the bird placement on iteration n.
# Likewise, q_ijn.
# Define x_ij{n-1} to be x_{i+1}jn or (x_{i+1}nn and x_0jn)
#     Contrast to Cook: x_ij{n-1} <=> x_ijn or (x_inn and x_{n+1}jn)
# Basically, shift all the bird positions down by one.
# Use i=0 as the bird to be removed
# It's first in the q ordering, so it's easier to propagate.
# The standard removal choice fails because q doesn't know about the last x,
# So we can't prove the q_ijn -> q_ij{n-1} step.


def recurse_cardinality(n, n_prev):
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
    print("c Recurse cardinality from {} to {}".format(n_prev, n_prev - 1))
    print(
        "c Vars {}-{}".format(
            base_var_curr, base_var_curr + 2 * num_holes_curr * num_birds_curr
        )
    )
    for j in range(1, num_holes_curr + 1):
        x_0jpk = base_var_prev + 0 * num_holes_prev + j
        for i in range(0, num_birds_curr):
            x_ijk = base_var_curr + i * num_holes_curr + j
            x_pijpk = base_var_prev + (i + 1) * num_holes_prev + j
            x_pipkpk = base_var_prev + (i + 1) * num_holes_prev + num_holes_prev

            # First, introduce the new x var.
            print("c Introduce x({}, {}, {})".format(i, j, n_prev - 1))
            # x_ijk <=> x_pijpk or (x_pipkpk and x_0jpk)

            # x_ijk -> x_pijpk V x_pipkpk
            print("-{} {} {} 0".format(x_ijk, x_pijpk, x_pipkpk))
            # x_ijk -> x_pijpk V x_0jpk
            print("-{} {} {} 0".format(x_ijk, x_pijpk, x_0jpk))
            # x_pijpk -> x_ijk
            print("{} -{} 0".format(x_ijk, x_pijpk))
            # x_pipkpk /\ x_0jpk -> x_ijk
            print("{} -{} -{} 0".format(x_ijk, x_pipkpk, x_0jpk))

            # Second, introduce the new q var, just as before.
            print("c Introduce q({}, {}, {})".format(i, j, n_prev - 1))
            q_ijk = (
                base_var_curr + num_holes_curr * num_birds_curr + i * num_holes_curr + j
            )
            if i == 0:
                # Special case: identical to x_ijk
                print("-{} {} 0".format(q_ijk, x_ijk))
                print("{} -{} 0".format(q_ijk, x_ijk))
            else:
                q_mijk = (
                    base_var_curr
                    + num_holes_curr * num_birds_curr
                    + (i - 1) * num_holes_curr
                    + j
                )
                # q_ij -> x_ij or q_mij
                print("-{} {} {} 0".format(q_ijk, x_ijk, q_mijk))
                # x_ij -> q_ij
                print("{} -{} 0".format(q_ijk, x_ijk))
                # q_mij -> q_ij
                print("{} -{} 0".format(q_ijk, q_mijk))

                # We're trying to prove:
                # not q_mijk or not x_ijk
                # Why should it be true?
                # If not x_0jpk,
                # then x_ijk = x_pijpk,
                # and q_mijk = q_ijpk,
                # so transfer.
                print("{} -{} -{} 0".format(x_0jpk, q_mijk, x_ijk))
                # If x_0jpk,
                # then not x_pijpk
                # and x_ijk = x_pipkpk
                # and q_mijk = q_ipkpk
                # so transfer
                print("-{} -{} 0".format(q_mijk, x_ijk))
    for i in range(0, num_birds_curr):
        # Each bird is still in a hole
        hole_vars = []
        for j in range(1, num_holes_curr + 1):
            x_ijk = base_var_curr + i * num_holes_curr + j
            hole_vars.append(x_ijk)
        clause_str = " ".join(str(var) for var in hole_vars)
        print("c Bird {} in a hole on iter {}".format(i, n_prev -1))
        print("{} 0".format(clause_str))

# It's good practice to have a small working set,
# by deleting clauses once you're done.
def delete_original(n):
    num_birds = n+1
    num_holes = n
    print("c Delete original")
    # i is hole, j is bird1, k is bird2. Each pair of birds is not in the same hole.
    for i in range(1, num_holes+1):
        for j in range(0, num_birds):
            for k in range(j+1, num_birds):
                var_j = j * num_holes + i
                var_k = k * num_holes + i
                print("d -{} -{} 0".format(var_j, var_k))

def delete_derive(n):
    num_birds = n + 1
    num_holes = n
    print("c Delete derive")
    for j in range(1, num_holes + 1):
        for i in range(0, num_birds):
            x_ij = i * num_holes + j
            q_ij = num_holes * num_birds + i * num_holes + j
            if i == 0:
                print("d -{} {} 0".format(q_ij, x_ij))
                print("d {} -{} 0".format(q_ij, x_ij))
            else:
                q_mij = num_holes * num_birds + (i - 1) * num_holes + j
                print("d -{} {} {} 0".format(q_ij, x_ij, q_mij))
                print("d {} -{} 0".format(q_ij, x_ij))
                print("d {} -{} 0".format(q_ij, q_mij))

                print("d -{} -{} 0".format(q_mij, x_ij))
    # From generate
    for i in range(0, num_birds):
        vars_in_clause = []
        for j in range(1, num_holes + 1):
            vars_in_clause.append(i * num_holes + j)
        clause_str = ' '.join(str(v) for v in vars_in_clause)
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
    print("c Delete clauses generated on {}".format(n_prev))
    for j in range(1, num_holes_curr + 1):
        x_0jpk = base_var_prev + 0 * num_holes_prev + j
        for i in range(0, num_birds_curr):
            x_ijk = base_var_curr + i * num_holes_curr + j
            x_pijpk = base_var_prev + (i + 1) * num_holes_prev + j
            x_pipkpk = base_var_prev + (i + 1) * num_holes_prev + num_holes_prev
            print("d -{} {} {} 0".format(x_ijk, x_pijpk, x_pipkpk))
            print("d -{} {} {} 0".format(x_ijk, x_pijpk, x_0jpk))
            print("d {} -{} 0".format(x_ijk, x_pijpk))
            print("d {} -{} -{} 0".format(x_ijk, x_pipkpk, x_0jpk))

            q_ijk = (
                base_var_curr + num_holes_curr * num_birds_curr + i * num_holes_curr + j
            )
            if i == 0:
                print("d -{} {} 0".format(q_ijk, x_ijk))
                print("d {} -{} 0".format(q_ijk, x_ijk))
            else:
                q_mijk = (
                    base_var_curr
                    + num_holes_curr * num_birds_curr
                    + (i - 1) * num_holes_curr
                    + j
                )
                print("d -{} {} {} 0".format(q_ijk, x_ijk, q_mijk))
                print("d {} -{} 0".format(q_ijk, x_ijk))
                print("d {} -{} 0".format(q_ijk, q_mijk))

                print("d {} -{} -{} 0".format(x_0jpk, q_mijk, x_ijk))
                print("d -{} -{} 0".format(q_mijk, x_ijk))
    for i in range(0, num_birds_curr):
        hole_vars = []
        for j in range(1, num_holes_curr + 1):
            x_ijk = base_var_curr + i * num_holes_curr + j
            hole_vars.append(x_ijk)
        clause_str = " ".join(str(var) for var in hole_vars)
        print("d {} 0".format(clause_str))
    

# End-to-end proof
def full_proof(n):
    derive_cardinality(n)
    delete_original(n)
    for n_i in range(n, 1, -1):
        recurse_cardinality(n, n_i)
        if n_i < n:
            delete_recursive(n, n_i+1)
        else:
            delete_derive(n)
    # I believe we can just finish at this point
    print("c Complete")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Call with command line arg: n == num holes")
    else:
        n = int(sys.argv[1])
        full_proof(n)
