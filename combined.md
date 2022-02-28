# Steps to obtain combined (amo-3 and kissat) DRAT proofs
1. change line 175 in `prove-amo-general.py` to 
```
for n_i in range(8, 7, -1):
```
2. use line 181 and comment out line 180 in `prove-amo-general.py`
3. change file path in `test-trim.sh` and execute
```
bash test-trim.sh i_min i_max 3 3
```
4. change line 175 in `prove-amo-general.py` to 
```
for n_i in range(n, 7, -1):
```
5. use line 180 and comment out 181 in `prove-amo-general.py`
6. change file path in `test-trim.sh` and execute
```
bash test-combine.sh i_min i_max 3 3 v d
```