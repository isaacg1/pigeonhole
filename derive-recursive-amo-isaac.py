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

def derive_recursive(n):
    num_birds = n+1
    num_holes = n

    #cnf = CNF()
    cnf = []

    for j in range(1, num_holes+1): # [1, n]
        v = []
        for i in range(num_holes):
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
            
        """
			# for each j, there is y_j
			y_j = num_holes * num_birds + j
			
			# (x_1j, x_2j, x_3j, y_j)
			x_1j = 0 * num_holes + j
			x_2j = 1 * num_holes + j
			x_3j = 2 * num_holes + j

			amo1 = CardEnc.atmost([x_1j, x_2j, x_3j, y_j], encoding=EncType.pairwise)
			for c in amo1.clauses: 
				cnf.append(c)

			# (not(y_j), x_4j, ..., x_{n+1}j)
			v = [-(y_j)] 
			for i in range(3, num_birds): # [3, n]
				x_ij = i * num_holes + j 
				v.append(x_ij)
				
			amo2 = CardEnc.atmost(v, encoding=EncType.pairwise)
			for c in amo2.clauses: 
				cnf.append(c)
                """

	# write to file
	# cnf.to_file('amo.drat')

	# print to terminal
    #for c in cnf:#.clauses:
    #    print(" ".join(str(e) for e in c) + " 0")


if __name__ == '__main__':
    import sys
#    from pysat.formula import CNF
#    from pysat.card import *
    if len(sys.argv) < 2:
        print("Call with command line arg: n == num holes")
    else:
        n = int(sys.argv[1])
        derive_recursive(n)



