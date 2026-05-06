from kafka import KafkaConsumer
from const import *
import sys

try:
    topic = sys.argv[1]
except:
    print('Topic not provided as command-line argument, using default')
    topic = TOPIC1

# Create consumer: Option 1 -- only consumes new events (comment out Option 2 below)
#consumer = KafkaConsumer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT])

# Create consumer: Option 2 -- consumes old events (comment out Option 1 above)
consumer = KafkaConsumer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT], auto_offset_reset='earliest')
  
consumer.subscribe([topic])
for msg in consumer:
    print (msg.value)
