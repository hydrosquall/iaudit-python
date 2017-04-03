# This script makes each of the servers talk to each other.

import os
from iaudit import keygen
import itertools
import grequests
import random

config = keygen.getConfig("iaudit-master.json")
pubConfig = keygen.generate_public_config(config['modBits'], config['keyBits'])
numWorkers = len(config['workers'])
pubConfig['masterHost'] = config['masterHost']  # IP:Port of master
pubConfig['numWorkers'] = numWorkers
pubConfig['hashSeed'] = config['hashSeed']
pubConfig['minHashPrime'] = config['minHashPrime']
pubConfig['isMinHash'] = config['isMinHash']

# Now we need to generate numMinHashes of minHash pairs
minHashes = set()

while len(minHashes) < config['numMinHashes']:
    # 127 bits guarantees a and b will be small enough
    minHashes.add( (random.getrandbits(128) - 1 , random.getrandbits(128) -1 ))

pubConfig['minHashes'] = list(minHashes)


# # Generate public config files and distribute to each worker
# # Maybe these should be part of trigger, and not the server code.
cwd = os.getcwd()
for i, worker in enumerate(config['workers']):
    filepath = os.path.join(cwd, "workers", str(i), "public-config.json")
    workerConfig = dict(pubConfig)
    workerConfig['workerID'] = i
    workerConfig['workerHost'] = worker    # IP:Port of worker
    indexNeighbor = (i + 1) % numWorkers   # who to pass data to
    workerConfig['neighborHost'] = config['workers'][indexNeighbor]
    keygen.setConfig(workerConfig, filepath)


allServers = list(config['workers'])
allServers.append(config['masterHost'])

def exception_handler(request, exception):
    print "Request failed"

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
cutsets = []
for i in xrange(numWorkers):
    logPath = os.path.join(cwd, "master", str(i))
    cutsets.append(keygen.getConfig(logPath))

# convert each grouping to a set
sets = [set(cutset) for cutset in cutsets]

# all possible pairings of workers so intersection operator is usable later
# 2-way pairing is currently arbitrary
providerPairs = list(itertools.combinations(range(numWorkers), 2))

print("Computing {} Intersections".format(len(providerPairs)))
scores = []
for pair in providerPairs:
    lenIntersection = len(sets[pair[0]] & sets[pair[1]])

    if config['isMinHash'] == 1:
        lenTotal = config['numMinHashes']
    else:
        lenTotal = len(sets[pair[0]]) +  len(sets[pair[1]])

    print "{}: {}/{}".format(pair, lenIntersection, lenTotal)
    scores.append((pair, float(lenIntersection) / lenTotal))

scores.sort(key=lambda x: x[1]) # sort by second value

# use slicing here to control which of the top scores you return to user!
print scores

# shutdown each server
rs = (grequests.post("http://{}/shutdown".format(server)) for server in allServers)
# Run asynchronous requests
grequests.map(rs, exception_handler=exception_handler)
print "All done!"
