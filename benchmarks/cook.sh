#!/bin/bash
# A bash script to iteratively run Cook's PHP proof generator with different inputs
# The generator can be accessed here: https://github.com/rebryant/pgbdd/blob/master/benchmarks/pigeon-cook.py

# Change the relative path to pigeon-cook.py if needed
rpath=../../pgbdd/benchmarks/pigeon-cook.py

# Remove previous benckmark results
rm -f cook-added-clauses.txt

for (( n = $1; n <= $2; n = n + 1)) 
do  
    python3 $rpath -n $n -r cook-cnf/cook-${n} | tee -a cook-added-clauses.txt
    rm -f cook-cnf/cook-${n}.lrat
done
