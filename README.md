# An example that combines the pub-sub and client-server interaction paradigms

## Overall architecture:
```
(1) publisher → (2) subscriber/publisher → (3) subscriber/web service ↔ (4) client
```
1. Publisher produces events on first topic
2. Subscriber/Publisher consumes and processes events of first topic, produces events on second topic
3. Subscriber/Web Service consumes events of second topic, stores event data locally for consumption via a simple RESTful API
4. Client sends requests to the RESTful API to get event data in various forms (latest, k latest, aveage etc.)

## Installation instructions (Kafka etc.)

### Follow these steps to run a Kafka broker on a server (with at least 2GB of RAM, such as AWS instance type t3-small):

- Open a command-line interface (shell) on the server

#### If not done yet, install JDK and download + configure KafkaInstall and configure Apache Kafka (on the machine mentioned above):

##### Install JDK (assuming Ubuntu Linux)
```
sudo apt update
```
```
sudo apt install default-jdk
```
##### Install and configure Apache Kafka. For more detailed instructions, see Kafka's Quickstart page: https://kafka.apache.org/quickstart
- Download and uncompress Kafka  
```
wget https://dlcdn.apache.org/kafka/4.2.0/kafka_2.13-4.2.0.tgz
```
```
tar -xzf kafka_2.13-4.2.0.tgz
```

- Basic configuration of Kafka (for remote access to the broker)
```
cd kafka_2.13-4.2.0/
```

**Enable remote access to the broker:** Edit the file **config/server.properties** (in the kafka directory) in order to change the line starting with **advertised_listeners**, replacing (only) the first occurrence of **localhost** with the **IP address** of the machine where the Broker will run. It is recommended to use a fixed public IP address for this machine. That line should look like this (replacing the IP address, obviously):

advertised.listeners=PLAINTEXT://32.195.37.234:9092,CONTROLLER://localhost:9093

##### Run the Kafka broker (either each time you start the server machine or put the following commands on a startup script): 
- Create the metadata files with the configuration
```
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
```
```
bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties
```

- Once configured, run the following command to actually start the broker
```
bin/kafka-server-start.sh config/server.properties
```

#### For the clients (do this on all the machines where publishers and subscribers will run):

##### Install the Kafka Python client

```
sudo apt update
sudo apt install python3-pip
sudo apt install python3-venv
python3 -m venv myvenv
source myvenv/bin/activate
pip3 install kafka-python
```

### Now run each process (publisher, publisher/subscriber, and consumer/server) on a separate machine
