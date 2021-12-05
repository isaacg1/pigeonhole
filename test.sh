#/usr/bin/bash
echo "Clauses"
for i in {1..20}
    do
    for j in {2..9}
        do
        python3 prove-amo-general.py $i $j > testing/amo-$i-$j.drat
        echo -n `grep -c '^[-0-9]' testing/amo-$i-$j.drat`
        echo -n ' '
    done
    echo ''
done

echo "Verifying, 0 is success"
for i in {1..20}
    do
    python3 generate.py $i > testing/php-standard-$i.cnf
    for j in {2..9}
        do
        drat/drat-trim testing/php-standard-$i.cnf testing/amo-$i-$j.drat -b >/dev/null
        result=$?
        if [[ $result -gt 0 ]]
        then
            echo $result
            exit $result
        fi
        echo -n '.'
    done
    echo ''
done
echo $?
