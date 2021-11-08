def derive_amo(n):
    num_birds = n+1
    num_holes = n

    #cnf = CNF()
    cnf = []

    for j in range(1, num_holes+1): # [1, n]
        v = []
        for i in range(num_birds):
            x_ij = i* num_holes + j
            v.append(x_ij)
        l = 0
        print("c start iter {}".format(j))
        while len(v) > 1:
            if len(v) > 3:
                y_lj = num_holes * num_birds + l * num_holes + j
                print("c l={} j={} y_lj={}".format(l, j, y_lj))
                front = v[:3] + [y_lj]
                v = v[3:]
                #cnf.extend(CardEnc.atmost(front, encoding=EncType.pairwise))
                for index_1 in range(len(front)):
                    for index_2 in range(index_1+1, len(front)):
                        #cnf.append([-front[i], -front[j]])
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
                    for index_2 in range(index_1+1, len(v)):
                        #cnf.append([-v[i], -v[j]])
                        print("{} {} 0".format(-v[index_1], -v[index_2]))
                v = []
            l += 1

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
    print("c Recurse cardinality from {} to {}".format(n_prev, n_prev - 1))
    print(
        "c Vars {}-{}".format(
            base_var_curr, base_var_curr + 2 * num_holes_curr * num_birds_curr
        )
    )
    for j in range(1, num_holes_curr + 1):
        x_0jpk = base_var_prev + 0 * num_holes_prev + j
        v = []
        for i in range(num_birds_curr):
            x_ijk = base_var_curr + i * num_holes_curr + j
            x_pijpk = base_var_prev + (i + 1) * num_holes_prev + j
            x_pipkpk = base_var_prev + (i + 1) * num_holes_prev + num_holes_prev

            # First, introduce the new x var.
            print("c Introduce x({}, {}, {})={}".format(i, j, n_prev - 1, x_ijk))
            # x_ijk <=> x_pijpk or (x_pipkpk and x_0jpk)

            # x_ijk -> x_pijpk V x_pipkpk
            print("-{} {} {} 0".format(x_ijk, x_pijpk, x_pipkpk))
            # x_ijk -> x_pijpk V x_0jpk
            print("-{} {} {} 0".format(x_ijk, x_pijpk, x_0jpk))
            # x_pijpk -> x_ijk
            print("{} -{} 0".format(x_ijk, x_pijpk))
            # x_pipkpk /\ x_0jpk -> x_ijk
            print("{} -{} -{} 0".format(x_ijk, x_pipkpk, x_0jpk))
            v.append(x_ijk)
        print("c start introducing ys iter {} {}".format(n_prev, j))
        l = 0
        while len(v) > 1:
            if len(v) > 3:
                y_ljk = base_var_curr + num_holes_curr * num_birds_curr + l * num_holes_curr + j
                print("c l={} j={} y_lj={}".format(l, j, y_lj))
                front = v[:3] + [y_lj]
                v = v[3:]
                for index_1 in range(len(front)):
                    for index_2 in range(index_1+1, len(front)):
                        print("{} {} 0".format(-front[index_2], -front[index_1]))
                print("{} {} {} {} 0".format(front[3], front[0], front[1], front[2]))
                v.insert(0, -y_ljk)
            else:
                print("c final clauses of iter {} {}".format(n_prev, j))
                for index_1 in range(len(v)):
                    for index_2 in range(index_1+1, len(v)):
                        if index_1 == 0:
                            print("c Hint: case analysis on x_0jpk")
                            print("{} {} {} 0".format(x_0jpk, -v[index_1], -v[index_2]))
                        print("{} {} 0".format(-v[index_1], -v[index_2]))
                v = []
            l += 1
    for i in range(0, num_birds_curr):
        hole_vars = []
        for j in range(1, num_holes_curr + 1):
            x_ijk = base_var_curr + i * num_holes_curr + j
            hole_vars.append(x_ijk)
        clause_str = " ".join(str(var) for var in hole_vars)
        print("c Bird {} in a hole on iter {}".format(i, n_prev -1))
        print("{} 0".format(clause_str))

def full_proof(n):
    derive_amo(n)
    for n_i in range(n, 1, -1):
        recurse_amo(n, n_i)
    print("c Complete")
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Call with command line arg: n == num holes")
    else:
        n = int(sys.argv[1])
        full_proof(n)

