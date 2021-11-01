# Generate the standard encoding
# Should be identical to https://github.com/marijnheule/encode/blob/master/php.c

def php_standard(n):
    # size == num_birds
    num_birds = n+1
    num_holes = n
    # Var x_{ij} means bird i in hole j
    # Birds range from 0 to num_birds - 1, inclusive
    # Holes range from 1 to num_holes, inclusive
    # x_{ij} encoded as i * num_holes + j, which ranges from 1 to num_holes * num_birds
    num_vars = num_birds * num_holes
    # Two kinds of clauses:
    # Each bird is in a hole, num_birds many clauses
    # For each hole, for each pair of birds,
    # Not both birds in the hole.
    num_clauses = num_birds + num_holes * num_birds * (num_birds - 1) // 2

    print("p cnf {} {}".format(num_vars, num_clauses))

    # i is bird, j is hole. Each bird in at least one hole.
    for i in range(0, num_birds):
        vars_in_clause = []
        for j in range(1, num_holes + 1):
            vars_in_clause.append(i * num_holes + j)
        clause_str = ' '.join(str(v) for v in vars_in_clause)
        print("{} 0".format(clause_str))

    # i is hole, j is bird1, k is bird2. Each pair of birds is not in the same hole.
    for i in range(1, num_holes+1):
        for j in range(0, num_birds):
            for k in range(j+1, num_birds):
                var_j = j * num_holes + i
                var_k = k * num_holes + i
                print("-{} -{} 0".format(var_j, var_k))
        

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Call with command line arg: n == num holes")
    else:
        n = int(sys.argv[1])
        php_standard(n)
