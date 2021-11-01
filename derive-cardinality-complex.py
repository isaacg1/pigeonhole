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
    num_birds = n+1
    num_holes = n
    for j in range(1, num_holes+1):
        for i in range(0, num_birds):
            x_ij = i * num_holes + j
            q_ij = num_holes * num_birds + i * num_holes + j
            if i == 0:
                # Skip: q_ij is equivalent to x_ij
                continue
            if i == 1:
                # q_m1j is q_0j is x_0j
                q_mij = (i-1) * num_holes + j
            else:
                # q_mij is q_{i-1}j
                q_mij = num_holes * num_birds + (i-1) * num_holes + j
            if i < num_birds - 1:
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


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Call with command line arg: n == num holes")
    else:
        n = int(sys.argv[1])
        derive_cardinality(n)

