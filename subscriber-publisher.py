from kafka import KafkaConsumer
from kafka import KafkaProducer
from const import *
import sys

try:
    topic1 = sys.argv[1]
    topic2 = sys.argv[2]
except:
    print ('Topic 1 and Topic 2 not provided as command-line arguments, using default')
    topic1 = TOPIC1
    topic2 = TOPIC2

# Consume old events (published before I started); switch the two lines below if this behavior is not desired
consumer = KafkaConsumer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT], auto_offset_reset='earliest')
#consumer = KafkaConsumer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT])

producer = KafkaProducer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT])

consumer.subscribe([topic1])
i = 0
for msg in consumer:
    print (msg.value)
    txt = 'My ' + str(i++) + ' message for ' + topic2
    producer.send(topic2, value=txt.encode())
    producer.flush()
