# Cameron Yick
# 1 worker per cloud provider
# After computing a local encryption key
import os
import sys
import json
from iaudit import keygen
import iaudit
import random

from flask import Flask
from flask import request
import requests

import numpy as np
import math

if len(sys.argv) > 1:
    confPath = os.path.join("workers", sys.argv[1], 'public-config.json')
    graphPath = os.path.join("workers", sys.argv[1], 'vulnerabilities.txt')
    config = keygen.getConfig(confPath)
    cutsetPath= os.path.join("workers", sys.argv[1], 'cutset.txt')

    with open(graphPath) as f:
        cutsetText="".join(line.rstrip() for line in f)

    numWorkers = config['numWorkers']
    seed = config['hashSeed']
    isMinHash = config['isMinHash']  # Are we using minHash method

    # Init config file
    cutsets = {
        'workerID' : config['workerID'],
    }

    cutsetList = iaudit.string_to_cutsets(cutsetText)

    if isMinHash == 1:
        # print "In Cutset"
        cutsets['cutsets'] = list(cutsetList.cutsetsItems)
    else:   # not minhash - want to have lots of things
        cutsets['cutsets'] = list(cutsetList.cutsets)

    # Convert the cutset text to 128-bit sequences
    murmurHashes = np.array([iaudit.hash_message(message, seed) 
                    for message in cutsets['cutsets']])

    transportHashes = []  # hashes to actually send around

    if isMinHash == 1:
        minHashParams  = config['minHashes']
        c              = config['minHashPrime']
        cFloatInverse  = 1.0 / c
        messageWeights = np.array([float(weight) for weight 
                          in cutsetList.cutsetsWeights])

        for a,b in minHashParams: # for each minhash function
            candidates = []


            # Vectorize for performance later with numpy
            # for message, weight in zip(murmurHashes, messageWeights):
            #     normalizedX = iaudit.minhash(message, a, b, c) * cFloatInverse
            #     testValue = -(math.log(normalizedX) / weight)
            #     candidates.append(testValue)         

            # then, use the murmurhash of the minimum candidate.
            transportHashes.append(murmurHashes[np.argmin(candidates)])  
    else:
        # use hash function to encrypt each dependency with murmurhash
        # then each message will be a long int
        # print "Not Min Hash"
        transportHashes = murmurHashes

    cutsets['cutsets'] = transportHashes
    print("Worker {}: {}".format(config['workerID'], len(transportHashes)))

    # store cutset to disk
    keygen.setConfig(cutsets, cutsetPath)

    # lastly, make local worker key
    pvtConfig = keygen.generate_private_config(config, config['keyBits'], config['workerID'])
    pvtKey = keygen.make_private_key(config, pvtConfig)
    pubKey = pvtKey.publickey()

else:
    print "No worker specified"


HEADERS = {'Content-Type': 'application/json'}
app = Flask(__name__)

# Shutdown method provided via pococo
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route("/store", methods=['POST'])
def storeCutsets():
    '''
        Store a cutset to disk to be processed on next cycle
    '''
    # print "try to store"
    newCutsets = request.get_json(force=True)
    # save cutset to disk
    keygen.setConfig( newCutsets, cutsetPath)
    return "OK"

@app.route('/process', methods=['GET'])
def processCutsets():
    '''
        What to do when you've been given a cutset. Wrapper for encrypt, permute
        , and send to neighbor
    '''

    cutsets = keygen.getConfig(cutsetPath)
    # Shuffle and encrypt
    # encrypt in place
    cutsets['cutsets'] = [pubKey.encrypt(message, None)[0] for message in cutsets['cutsets']]

    # shuffle in place
    random.shuffle(cutsets['cutsets'])

    # print cutsets
    # payload = cutsets
    keygen.setConfig(cutsets, cutsetPath)

    # print payload
    # Either relay data to next neighbor, or give to master
    # now that we're done, be OK with reading the new data on the next cycle.

    return "OK"

# break pass and swap so that operations are atomic
# make more secure by requiring authorization key to access route.
@app.route("/pass", methods=['GET'])
def passCutsets():
    payload = keygen.getConfig(cutsetPath)
    passCutsets.counter += 1
    # print "{} pinged {} times".format(config['workerID'], passCutsets.counter)
    if passCutsets.counter < numWorkers:
        # print "trying to store at {}".format(config['neighborHost'])
        requests.post("http://{}/store".format(config['neighborHost']), 
                      headers=HEADERS, json=payload)
    else:
        # print "On last call, just give to master"
        requests.post("http://{}/save".format(config['masterHost']), headers=HEADERS, json=payload)
    return "OK"

# @app.route("/swap", methods=["GET"])
# def swapCutsets():
#     cutsets = keygen.getConfig(cutsetPath)
#     return "OK"


# initialize counter on each node
# might be thrown off if bombarded with requests
passCutsets.counter = 0

recvHOST, recvPORT = config['workerHost'].split(':')                    
recvPORT = int(recvPORT) # master port  
if __name__ == '__main__':
    app.run(port=recvPORT, threaded=True)
