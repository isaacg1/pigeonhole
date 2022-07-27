#/usr/bin/bash

mkdir testing

echo "Clauses"
for i in {1..100}
    do
    python3 prove-amo-general.py $i 3 > testing/amo-$i-3.drat
    echo -n $i `grep -c '^[-0-9]' testing/amo-$i-3.drat`
    python3 generate.py $i > testing/php-standard-$i.cnf
    /usr/bin/time -f "\t%E real,\t%U user,\t%S sys" drat/drat-trim testing/php-standard-$i.cnf testing/amo-$i-3.drat -b >/dev/null
    result=$?
    if [[ $result -gt 0 ]]
    then
        echo $result
        exit $result
    fi
done
