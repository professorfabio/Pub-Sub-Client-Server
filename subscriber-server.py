from kafka import KafkaConsumer

from flask import Flask
from flask import jsonify
from flask import request
from flask import abort

from const import *

import sys
import threading


###------ Subscriber (consumer) Part ------
def startConsumer():
    try:
        topic = sys.argv[1]
    except:
        print('Topic not provided as command-line argument, using default')
        topic = TOPIC2
    
    # Create consumer: Option 1 -- only consumes new events (comment out Option 2 below)
    #consumer = KafkaConsumer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT])

    # Create consumer: Option 2 -- consumes old events (comment out Option 1 above)
    consumer = KafkaConsumer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT], auto_offset_reset='earliest')
  
    consumer.subscribe([topic])
    for msg in consumer:
        print (msg.value)
        
        # Append the event data (value) to the event database:
        eventDB.append(msg.value)

###------------ Server Part ---------------

# Instantiate the web services server
app = Flask(__name__)

# List to store event data (could be a database)
eventDB = []

# Endpoint to consume all event data:
@app.route('/eventdata', methods=['GET'])
def getAllEventData():
    return jsonify({'AllEventData':eventDB})

# Endpoint to consume the latest event data:
@app.route('/eventdata/latest', methods=['GET'])
def getLatestEventData():
    lastElement = eventDB[len(eventDB)-1]
    return jsonify({'LastEventData':lastElment})

# Endpoint to consume the n-th event data:
@app.route('/eventdata/<index>', methods=['GET'])
def getNthEventData(index):
    eventData = None
    try:
        eventData = eventDB[index]
    except:
        eventData = 'Does not exist'
        
    return jsonify({'NthEventData':eventData})
                                          
if __name__ == '__main__':
    # Create a new thread to run the subscriber (consumer):
    t = threading.Thread(target=startConsumer, args=())
    t.start()

    # And run the service on the main thread:
    app.run(host='0.0.0.0', port=const.SERVICE_PORT)

    t.join()
