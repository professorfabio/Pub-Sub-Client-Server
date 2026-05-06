from kafka import KafkaConsumer
from kafka import KafkaProducer
from const import *
import sys

consumer = KafkaConsumer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT], auto_offset_reset='earliest')
#consumer = KafkaConsumer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT])

producer = KafkaProducer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT])


consumer.subscribe([TOPIC1])
for msg in consumer:
    print (msg.value)
    txt = 'My message for ' + TOPIC2
    producer.send(TOPIC2, value=txt.encode())
    producer.flush()
