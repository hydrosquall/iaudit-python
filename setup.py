# This script places config files into each appropriate destination

import os
from iaudit import keygen
import itertools
import grequests
import random
import sys


if len(sys.argv) > 1:
    print "Reading custom input {}".format(str(sys.argv[1]))
    config = keygen.getConfig(str(sys.argv[1]) )
else:
    config = keygen.getConfig("iaudit-master.json")

pubConfig = keygen.generate_public_config(config['modBits'], config['keyBits'])
numWorkers = len(config['workers'])
pubConfig['masterHost'] = config['masterHost']  # IP:Port of master
pubConfig['numWorkers'] = numWorkers
pubConfig['hashSeed'] = config['hashSeed']
pubConfig['minHashPrime'] = config['minHashPrime']
pubConfig['isMinHash'] = config['isMinHash']

# Now we need to generate numMinHashes of minHash pairs
if config['isMinHash'] == 1:
    minHashes = set()
    while len(minHashes) < config['numMinHashes']:
        # 127 bits guarantees a and b will be small enough
        minHashes.add( (random.getrandbits(128) - 1 , random.getrandbits(128) -1 ))

    pubConfig['minHashes'] = list(minHashes)

# Generate public config files and distribute to each worker
cwd = os.getcwd()
for i, worker in enumerate(config['workers']):
    filepath = os.path.join(cwd, "workers", str(i), "public-config.json")
    workerConfig = dict(pubConfig)
    workerConfig['workerID'] = i
    workerConfig['workerHost'] = worker    # IP:Port of worker
    indexNeighbor = (i + 1) % numWorkers   # who to pass data to
    workerConfig['neighborHost'] = config['workers'][indexNeighbor]
    keygen.setConfig(workerConfig, filepath)
