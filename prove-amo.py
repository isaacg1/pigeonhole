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
	print("c Derive cardinality constraints from standard.")

	cnf = CNF()

	# TODO: apply direct encoding for num_birds <= 3
	if num_birds <= 3:
		print("not yet")
	else:
		for j in range(1, num_holes+1): # [1, n]
			# for each j, there is y_j
			y_j = num_holes * num_birds + j
			
			# (x_1j, x_2j, x_3j, y_j)
			# TODO: test how many vars in the amo1 gives the best result
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

	# write to file
	# cnf.to_file('amo.drat')

	# print to terminal
	for c in cnf.clauses:
		print(" ".join(str(e) for e in c) + " 0")

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
		num_holes_i * (num_holes_i + 2) 
		for num_holes_i in range(num_holes_prev + 1, num_holes_orig + 1)
	)
	base_var_curr = base_var_prev + 2 * num_holes_prev * num_birds_prev
	print("c Recurse amo from {} to {}".format(n_prev, n_prev - 1))
	print(
		"c Vars {}-{}".format(
			base_var_curr, base_var_curr + 2 * num_holes_curr * num_birds_curr
		)
	)

	cnf = CNF()

	for j in range(1, num_holes_curr + 1):
		# Q: why do we need this?
		# x_0jpk = base_var_prev + 0 * num_holes_prev + j
		# for i in range(0, num_birds_curr):
		#     x_ijk = base_var_curr + i * num_holes_curr + j
		#     x_pijpk = base_var_prev + (i + 1) * num_holes_prev + j
		#     x_pipkpk = base_var_prev + (i + 1) * num_holes_prev + num_holes_prev

		#     # First, introduce the new x var.
		#     print("c Introduce x({}, {}, {})".format(i, j, n_prev - 1))
		#     # x_ijk <=> x_ijpk or (x_ipkpk and x_pkjpk)

		#     # x_ijk -> x_pijpk V x_pipkpk
		#     print("-{} {} {} 0".format(x_ijk, x_pijpk, x_pipkpk))
		#     # x_ijk -> x_pijpk V x_0jpk
		#     print("-{} {} {} 0".format(x_ijk, x_pijpk, x_0jpk))
		#     # x_pijpk -> x_ijk
		#     print("{} -{} 0".format(x_ijk, x_pijpk))
		#     # x_pipkpk /\ x_0jpk -> x_ijk
		#     print("{} -{} -{} 0".format(x_ijk, x_pipkpk, x_0jpk))

		y_jk = (
			base_var_curr + num_holes_curr * num_birds_curr + j
		)

		# (x_1jk, x_2jk, x_3jk, y_jk)
		x_1jk = base_var_curr + 0 * num_holes_curr + j
		x_2jk = base_var_curr + 1 * num_holes_curr + j
		x_3jk = base_var_curr + 2 * num_holes_curr + j

		alo = [x_1jk, x_2jk, x_3jk]

		amo1 = CardEnc.atmost([x_1jk, x_2jk, x_3jk, y_jk], encoding=EncType.pairwise)
		for c in amo1.clauses: 
			cnf.append(c)

		# (not(y_j), x_4j, ..., x_{n+1}j)
		v = [-(y_jk)] 
		for i in range(3, num_birds_curr): # [3, n]
			x_ijk = base_var_curr + i * num_holes_curr + j 
			v.append(x_ijk)
			alo.append(x_ijk)
			
		amo2 = CardEnc.atmost(v, encoding=EncType.pairwise)
		for c in amo2.clauses: 
			cnf.append(c)

		# Each bird is in ALO hole
		c.append(alo)

		# write to file
		# cnf.to_file('amo.drat')

		# print to terminal
		for c in cnf.clauses:
			print(" ".join(str(e) for e in c) + " 0")

	# for i in range(0, num_birds_curr):
	# 	# Each bird is still in a hole
	# 	hole_vars = []
	# 	for j in range(1, num_holes_curr + 1):
	# 		x_ijk = base_var_curr + i * num_holes_curr + j
	# 		hole_vars.append(x_ijk)
	# 	clause_str = " ".join(str(var) for var in hole_vars)
	# 	print("c Bird {} in a hole on iter {}".format(i, n_prev -1))
	# 	print("{} 0".format(clause_str))

# # End-to-end proof
# def full_proof(n):
#     derive_amo(n)
#     delete_original(n)
#     for n_i in range(n, 1, -1):
#         recurse_cardinality(n, n_i)
#         if n_i < n:
#             delete_recursive(n, n_i+1)
#         else:
#             delete_derive(n)
#     print("c Complete")

# End-to-end proof
def full_proof(n):
	derive_amo(n)
	for n_i in range(n, 1, -1):
		recurse_amo(n, n_i)
	# I believe we can just finish at this point
	print("c Complete")

if __name__ == "__main__":
	
	import sys
	from pysat.formula import CNF
	from pysat.card import *

	if len(sys.argv) < 2:
		print("Call with command line arg: n == num holes")
	else:
		n = int(sys.argv[1])
		full_proof(n)