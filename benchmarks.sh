# Benchmark for 3 different sizes


# Put truncated bench files into worker directories
# 10 items
head sample_ftg/10k_demo/output1 -n 11 > workers/0/bench1.txt
head sample_ftg/10k_demo/output2 -n 11 > workers/1/bench1.txt
head sample_ftg/10k_demo/output3 -n 11 > workers/2/bench1.txt
echo "</cutsets>" >> workers/0/bench1.txt
echo "</cutsets>" >> workers/1/bench1.txt
echo "</cutsets>" >> workers/2/bench1.txt

# 100 items
head sample_ftg/10k_demo/output1 -n 101 > workers/0/bench2.txt
head sample_ftg/10k_demo/output2 -n 101 > workers/1/bench2.txt
head sample_ftg/10k_demo/output3 -n 101 > workers/2/bench2.txt
echo "</cutsets>" >> workers/0/bench2.txt
echo "</cutsets>" >> workers/1/bench2.txt
echo "</cutsets>" >> workers/2/bench2.txt

# 1000 items
head sample_ftg/10k_demo/output1 -n 1001 > workers/0/bench3.txt
head sample_ftg/10k_demo/output2 -n 1001 > workers/1/bench3.txt
head sample_ftg/10k_demo/output3 -n 1001 > workers/2/bench3.txt
echo "</cutsets>" >> workers/0/bench3.txt
echo "</cutsets>" >> workers/1/bench3.txt
echo "</cutsets>" >> workers/2/bench3.txt

# all items
cp sample_ftg/10k_demo/output1 workers/0/bench4.txt
cp sample_ftg/10k_demo/output2 workers/1/bench4.txt
cp sample_ftg/10k_demo/output3 workers/2/bench4.txt

# make one config file for 10, 100, 1000, 10,000 minhashed items
./demoTester.sh iaudit-master-minhash-benchmark-1.json
./demoTester.sh iaudit-master-minhash-benchmark-2.json
./demoTester.sh iaudit-master-minhash-benchmark-3.json

# make one config file for 10, 100, 1000 non-minhashed items
./demoTester.sh iaudit-master-nominhash-benchmark-1.json
./demoTester.sh iaudit-master-nominhash-benchmark-2.json
./demoTester.sh iaudit-master-nominhash-benchmark-3.json
