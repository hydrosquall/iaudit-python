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

if len(sys.argv) > 1:
    confPath = os.path.join("workers", sys.argv[1], 'public-config.json')
    graphPath = os.path.join("workers", sys.argv[1], 'vulnerabilities.txt')
    config = keygen.getConfig(confPath)
    cutsetPath= os.path.join("workers", sys.argv[1], 'cutset.txt')

    with open(graphPath) as f:
        cutsetText="".join(line.rstrip() for line in f)

    cutsets = {
        'workerID' : config['workerID'],
        'cutsets' : list(iaudit.string_to_cutsets(cutsetText).cutsets)
    }

    numWorkers = config['numWorkers']
    seed = config['hashSeed']

    # use hash function to encrypt each dependency with murmurhash
    # then each message will be a long int
    cutsets['cutsets'] = [iaudit.hash_message(message, seed) for message in cutsets['cutsets']]

    # store cutset to disk
    keygen.setConfig( cutsets, cutsetPath)

    # lastly, make local worker key
    pvtConfig = keygen.generate_private_config(config, config['keyBits'], config['workerID'])
    pvtKey = keygen.make_private_key(config, pvtConfig)
    pubKey = pvtKey.publickey()

else:
    print "No worker specified"


HEADERS = {'Content-Type': 'application/json'}

app = Flask(__name__)

newCutsets = {}
payload = {}


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
    print "try to store"
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
@app.route("/pass", methods=['GET'])
def passCutsets():
    payload = keygen.getConfig(cutsetPath)
    passCutsets.counter += 1
    # print "{} pinged {} times".format(config['workerID'], passCutsets.counter)
    if passCutsets.counter < numWorkers:
        print "trying to store at {}".format(config['neighborHost'])
        requests.post("http://{}/store".format(config['neighborHost']), headers=HEADERS, json=payload)
    else:
        print "On last call, just give to master"
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

# twisted is bad, try flask?
# Twisted Implementation
# from twisted.internet import reactor, protocol

# numWorkers = config['numWorkers']

# # receiving server

# HOST, PORT = config['neighborHost'].split(":")
# PORT = int(PORT)

# class MyServer(protocol.Protocol):
#     def connectionMade(self):
#         print "{} server is up".format(config['workerID'])

#     def dataReceived(self, data):
#         print data
    
# class MyServerFactory(protocol.Factory):
#     protocol = MyServer

# getFactory = MyServerFactory()
# reactor.listenTCP(recvPORT, getFactory)

# class MyClient(protocol.Protocol):
#     def connectionMade(self):
#         print "{} connected!".format(config['workerID'])
#         # self.transport.write("a message from {}".format(config['workerID']))
#         # for i in range(numWorkers - 1):
#         #     self.transport.write("a message from {}".format(config['workerID']))

# class MyClientFactory(protocol.ClientFactory):
#     protocol = MyClient

# sendFactory = MyClientFactory()
# reactor.connectTCP(HOST, PORT, sendFactory)
# reactor.run()

# ZMQ Implementation

# HOST, PORT = .split(":")
# ZMQ won't worry because it's all 1 address....
# context = zmq.Context()

# #  Socket to talk to server
# print("Connecting to hello world server")
# sendSocket = context.socket(zmq.REQ)

# sendSocket.connect("tcp://{}".format(config['neighborHost']))

# #  Send to all neighbors
# for request in range(config['numWorkers'] - 1):

#     print("Sending request %s " % request)
#     socketSocket.send_json({'from': config['workerID']})

#     # then receive data from sibling

#     #  Get the stuff from your neighbor
#     message = recvSocket.recv_json()

#     print("%s received [ %s ]" % (config['workerID'], message))

# socket.close()
# context.term()