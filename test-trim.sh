#!/bin/bash
# bash test-trim.sh i_min i_max j_min j_max
# i in [1, inf)
# j in [2, 9]
for (( i = $1; i <= $2; i++))
    do
    for (( j = $3; j <= $4; j++))
        do
        python3 prove-amo-general.py $i $j > testing/amo-$i-$j-at-7.cnf
        # get rid of comments
        sed -i '' '/^c/d' testing/amo-$i-$j-at-7.cnf
        # for i = 8, it cannot have deletion info
        if [ $i == 8 ]; then
            sed -i '' '/^d/d' testing/amo-$i-$j-at-7.cnf
        fi

        num_vars=$(grep -Eo '[0-9]+' testing/amo-$i-$j-at-7.cnf | sort -rn | head -n 1)
        num_clauses=$(grep -c '^[-0-9]' testing/amo-$i-$j-at-7.cnf)

        echo "p cnf $num_vars $num_clauses" | cat - testing/amo-$i-$j-at-7.cnf > /tmp/out && mv /tmp/out testing/amo-$i-$j-at-7.cnf


        ./../kissat/build/kissat --no-binary testing/amo-$i-$j-at-7.cnf testing/kissat-amo-$i-$j-at-7.drat

        ../drat-trim/drat-trim testing/amo-$i-$j-at-7.cnf testing/kissat-amo-$i-$j-at-7.drat -O -l testing/trimmed-amo-$i-$j-at-7.drat

    done
    echo ''
done