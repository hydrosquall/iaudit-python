# This script runs on the master node, and is responsible for coordinating
# all of the other nodes.

import os
from iaudit import keygen
import itertools
import grequests
import sys

def exception_handler(request, exception):
    print "Request failed"

if len(sys.argv) > 1:
    print "Reading custom input {}".format(str(sys.argv[1]))
    config = keygen.getConfig(str(sys.argv[1]) )
else:
    config = keygen.getConfig("iaudit-master.json")

numWorkers = len(config['workers'])

allServers = list(config['workers'])
allServers.append(config['masterHost'])

# Have each worker process its local batch, and send to neighbor.
for i in xrange(numWorkers):
    # Set of asynchronous requests
    for operation in ['process', 'pass']:
        # print "i {} | {}".format(i, operation)
        rs = (grequests.get("http://{}/{}".format(u, operation)) for u in config['workers'])
        # wait for each thing to finish
        grequests.map(rs, exception_handler=exception_handler)
    # print "Complete round {}".format(i)

# now, check the intersections
cwd = os.getcwd()
cutsets = []
for i in xrange(numWorkers):
    logPath = os.path.join(cwd, "master", str(i))
    cutsets.append(keygen.getConfig(logPath))

# convert each grouping to a set
sets = [set(cutset) for cutset in cutsets]

# all possible pairings of workers so intersection operator is usable later
# 2-way pairing is currently arbitrary, could become 3 way if needed
providerPairs = list(itertools.combinations(range(numWorkers), 2))

print("Computing {} Intersections".format(len(providerPairs))),
if config['isMinHash'] == 1:
    print("WITH minHash")
    print("(Pair) : # overlapping / # of minhash functions")
else:
    print("WITHOUT minHash")
    print("(Pair) : # overlapping / length of set union")

scores = []
for pair in providerPairs:
    lenIntersection = float(len(sets[pair[0]] & sets[pair[1]]))

    if config['isMinHash'] == 1:
        lenTotal = config['numMinHashes']
    else:
        lenTotal = len(sets[pair[0]]) + len(sets[pair[1]])

    print "{}: {}/{}".format(pair, lenIntersection, lenTotal)
    scores.append((pair, lenIntersection / lenTotal))

scores.sort(key=lambda x: x[1]) # sort by second value
# use slicing here to control which of the top scores you return to user!
# Print rankings
print "Rankings: "
for i, score in enumerate(scores):
    print "{}: {}   {}".format(i, score[0], score[1])

# shutdown each server
rs = (grequests.post("http://{}/shutdown".format(server)) for server in allServers)
# Run asynchronous requests
grequests.map(rs, exception_handler=exception_handler)
# print "All done!"
