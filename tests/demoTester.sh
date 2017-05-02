
# Demo usage for performance benchmarks
# first clean master logs

# # Clean logs
rm -f master/* 
DATE="$(date +%m_%d_%Y__%H_%M_%S)"

echo "Launching Servers"
OUTFILE1=results/$DATE-min.txt

python setup.py $1
(python worker.py 0)&
(python worker.py 1)&
(python worker.py 2)&
(python master.py)&

echo "Waiting for servers to initialize"
sleep 200

echo "Compute cardinality scores with 30 minhashes"
time python trigger.py $1 > $OUTFILE1


# sleep 2

# run a second time
# echo "Launching Servers Second Time Without Minhash"
# OUTFILE2=results/$DATE-nomin.txt

# python setup.py iaudit-master.json
# (python worker.py 0)&
# (python worker.py 1)&
# (python worker.py 2)&
# (python master.py)&

# echo "Waiting for servers to initialize"
# sleep 5

# echo "Compute cardinality scores"
# time python trigger.py iaudit-master.json > $OUTFILE2
