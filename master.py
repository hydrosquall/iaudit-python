# master.py
# Cameron Yick
# central controller for the iaudit

# Spin up a server for receiving payloads 
from flask import Flask
from flask_script import Manager, Server
from flask import request
import requests

from iaudit import keygen
import os

cwd = os.getcwd()

# for asynchronous calls
app = Flask(__name__)

# Shutdown via pococo
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


# # modified from http://stackoverflow.com/questions/27465533/run-code-after-flask-application-has-started
@app.route('/save', methods=['POST'])
def intersectCutsets():
    '''
        Write each inbound collection to disk
    '''
    response = request.get_json(force=True)
    workerID = response['workerID']
    print "Heard from {}".format(workerID)
    filepath = os.path.join(cwd, 'master', str(workerID))
    if response:
        keygen.setConfig(response['cutsets'], filepath)
        print "Store Success"
    else:
        print "Store Failed"

    return "OK"

config = keygen.getConfig("iaudit-master.json")
recvHOST, recvPORT = config['masterHost'].split(':')                    
recvPORT = int(recvPORT) # master port  

# Remeber to add the command to your Manager instance
# manager.add_command('runserver', CustomServer())
if __name__ == "__main__":
    app.run(host=recvHOST, port=recvPORT)


# from twisted.internet import reactor, protocol
# recvHOST, recvPORT = config['masterHost'].split(':')                    
# recvPORT = int(recvPORT) # master port  

# class MyServer(protocol.Protocol):
#   def connectionMade(self):
#     print "masterconnected!"
#     print "In master server"
    

# class MyServerFactory(protocol.Factory):
#     protocol = MyServer

# factory = MyServerFactory()
# reactor.listenTCP(recvPORT, factory)
# reactor.run()

# context = zmq.Context()
# socket = context.socket(zmq.REP)
# socket.bind("tcp://*:{}".format(PORT))

# nReceived = 0
# while nReceived < numWorkers:
#     #  Wait for next request from client
#     message = socket.recv()
#     print("Received request: %s" % message)
#     nReceived += 1

#     #  Do some 'work'
#     time.sleep(1)
#     #  Send reply back to client
#     socket.send_json({'hello': "world"})

# socket.close()
# context.term()

# use sockets or http?
# http://www.binarytides.com/python-socket-programming-tutorial/
# import socket                                 
# import sys                                    
                                              
                                              
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print 'Socket created'                        
                                              
# try:                                          
#     s.bind((HOST, PORT))                      
# except socket.error , msg:                    
#     print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#     sys.exit()                                
                                              
# print 'Socket bind complete'                  
                                              
# s.listen(5) # how many connect requests allowed  to be queued

# print 'Socket now listening'                  
           
# nReceived = 0

# data = {}

# #now keep talking with the client             
# while True:                                      
#     #wait to accept a connection - blocking call 
#     conn, addr = s.accept() 

#     nReceived  += 1                  
#     print 'Connected with ' + addr[0] + ':' +  str(addr[1])                         
#     data = conn.recv(1024)                    
#     reply = 'Received...' + data   
#     # print reply                 
#     if nReceived == numWorkers:
#         break
#     else:
#         continue
                
# print("Cleaning up!")                                       
# conn.close()                                  
# s.close()                               
# pvtConfigs = [iauditConfig.generate_private_config(pubConfig, config['keyBits']
#              , seed) for seed in range(2)]
