
# Demo usage 
# first clean master logs

# # Clean logs
rm -f master/* 
DATE="$(date +%H_%M_%S)"

echo "Launching Servers"
(python worker.py 0)&
(python worker.py 1)&
(python worker.py 2)&
(python master.py)&

echo "Waiting for servers to initialize"
sleep 6 

echo "Compute cardinality scores"
python trigger.py > results/min_$DATE.txt

# Debugging
echo "Node 1" >> results/min_$DATE.txt
cat workers/0/vulnerabilities.txt >> results/min_$DATE.txt
echo "Node 2" >> results/min_$DATE.txt
cat workers/1/vulnerabilities.txt >> results/min_$DATE.txt
echo "Node 3" >> results/min_$DATE.txt
cat workers/2/vulnerabilities.txt >> results/min_$DATE.txt

sleep 2

# run a second time
echo "Launching Servers Second Time"
(python worker.py 0)&
(python worker.py 1)&
(python worker.py 2)&
(python master.py)&

echo "Waiting for servers to initialize"
sleep 6 

echo "Compute cardinality scores"
python trigger.py iaudit-master-minhash.json > results/nomin_$DATE.txt

# Debugging
echo "Node 1" >> results/nomin_$DATE.txt
cat workers/0/vulnerabilities.txt >> results/nomin_$DATE.txt
echo "Node 2" >> results/nomin_$DATE.txt
cat workers/1/vulnerabilities.txt >> results/nomin_$DATE.txt
echo "Node 3" >> results/nomin_$DATE.txt
cat workers/2/vulnerabilities.txt >> results/nomin_$DATE.txt
