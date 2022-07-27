#!/bin/bash
# bash test-kissat.sh i_min i_max (d)elete/(n)o
# i in [1, inf)

rm -f kissat-results.txt

for (( i = $1; i <= $2; i++))
    do
    python3 derive-recursive-amo.py $i > testing/amo-$i.cnf

    num_vars=$(grep -Eo '[0-9]+' testing/amo-$i.cnf | sort -rn | head -n 1)
    num_clauses=$(grep -c '^[-0-9]' testing/amo-$i.cnf)

    echo "p cnf $num_vars $num_clauses" | cat - testing/amo-$i.cnf > /tmp/out && mv /tmp/out testing/amo-$i.cnf
    
    ./../kissat/build/kissat --no-binary testing/amo-$i.cnf testing/kissat-$i.drat

    lines=$(grep -c '^[-0-9]' testing/kissat-$i.drat)
    echo $(( $lines - 1 )) >> kissat-results.txt

    if [ $3 == d ]; then
        rm -f testing/kissat-$i.drat
    fi 
done