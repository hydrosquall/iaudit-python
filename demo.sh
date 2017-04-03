
# Demo usage 
# first clean master logs

# # Clean logs
rm -f master/* 

# Launch servers
echo "Launching Servers"
(python worker.py 0)&
(python worker.py 1)&
(python worker.py 2)&
(python master.py)&

echo "Waiting for servers to initialize"
sleep 6 

echo "Compute cardinality scores"
python trigger.py > master/intersection.txt