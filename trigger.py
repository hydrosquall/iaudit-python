# This script makes each of the servers talk to each other.
# 
import os
from iaudit import keygen
import itertools

import grequests

import os
from iaudit import keygen

config = keygen.getConfig("iaudit-master.json")
pubConfig = keygen.generate_public_config(config['modBits'], config['keyBits'])
numWorkers = len(config['workers'])
pubConfig['masterHost'] = config['masterHost']  # IP:Port of master
pubConfig['numWorkers'] = numWorkers
pubConfig['hashSeed'] = config['hashSeed']

# Generate public config files and distribute to each worker
# Maybe these should be part of trigger, and not the server code.
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
        print "i {} | {}".format(i, operation)
        rs = (grequests.get("http://{}/{}".format(u, operation)) for u in config['workers'])
        # wait for each thing to finish
        grequests.map(rs, exception_handler=exception_handler)

    print "Complete round {}".format(i)

# now, check the intersections
cutsets = []
for i in xrange(numWorkers):
    logPath = os.path.join(cwd, "master", str(i))
    cutsets.append(keygen.getConfig(logPath))

# convert each grouping to a set
sets = [set(cutset) for cutset in cutsets]


providerPairs = list(itertools.combinations(range(numWorkers), 2))

for pair in providerPairs:
    print pair
    intersection = sets[pair[0]] & sets[pair[1]]
    print len(intersection)

# shutdown each server
rs = (grequests.post("http://{}/shutdown".format(server)) for server in allServers)
# wait for each thing to finish
grequests.map(rs, exception_handler=exception_handler)
print "All done!"

