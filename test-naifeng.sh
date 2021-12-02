#!/bin/bash
# bash test-naifeng.sh i_min i_max j_min j_max (v)erify (d)elete
# i in [1, inf)
# j in [2, 9]
echo "Clauses"
for (( i = $1; i <= $2; i++))
    do
    for (( j = $3; j <= $4; j++))
        do
        python3 prove-amo-general.py $i $j > testing/amo-$i-$j.drat
        echo -n `grep -c '^[-0-9]' testing/amo-$i-$j.drat`
        echo -n ' '
        if [ $5 != v ] && [ $6 == d ]; then
            rm -f testing/amo-$i-$j.drat
        fi 
    done
    echo ''
done

if [ $5 == v ]; then
    echo "Verifying, 0 is success"
    for (( i = $1; i <= $2; i++))
        do
        python3 generate.py $i > testing/php-standard-$i.cnf
        for (( j = $3; j <= $4; j++))
            do
            ../drat-trim/drat-trim testing/php-standard-$i.cnf testing/amo-$i-$j.drat -b >/dev/null
            echo -n '.'
            if [ $6 == d ]; then
                rm -f testing/amo-$i-$j.drat
            fi 
        done
        echo ''
    done
    echo $?
fi