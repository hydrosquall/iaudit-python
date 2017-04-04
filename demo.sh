
# Demo usage 
# first clean master logs

# # Clean logs
rm -f master/* 
DATE="$(date +%m_%d_%Y__%H_%M_%S)"

echo "Launching Servers"
OUTFILE1=results/$DATE-min.txt

python setup.py iaudit-master-minhash.json
(python worker.py 0)&
(python worker.py 1)&
(python worker.py 2)&
(python master.py)&

echo "Waiting for servers to initialize"
sleep 6 

echo "Compute cardinality scores"
time python trigger.py iaudit-master-minhash.json > $OUTFILE1

# Debugging
echo "Node 0" >> $OUTFILE1
cat workers/0/vulnerabilities.txt >> $OUTFILE1
echo "Node 1" >> $OUTFILE1
cat workers/1/vulnerabilities.txt >> $OUTFILE1
echo "Node 2" >> $OUTFILE1
cat workers/2/vulnerabilities.txt >> $OUTFILE1

sleep 2

# run a second time
echo "Launching Servers Second Time"
OUTFILE2=results/$DATE-nomin.txt

python setup.py iaudit-master.json
(python worker.py 0)&
(python worker.py 1)&
(python worker.py 2)&
(python master.py)&

echo "Waiting for servers to initialize"
sleep 6 

echo "Compute cardinality scores"
time python trigger.py iaudit-master.json > $OUTFILE2

# Debugging
echo "Node 0" >> $OUTFILE2
cat workers/0/vulnerabilities.txt >> $OUTFILE2
echo "Node 1" >> $OUTFILE2
cat workers/1/vulnerabilities.txt >> $OUTFILE2
echo "Node 2" >> $OUTFILE2
cat workers/2/vulnerabilities.txt >> $OUTFILE2
