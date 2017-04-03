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

if __name__ == "__main__":
    app.run(host=recvHOST, port=recvPORT)
