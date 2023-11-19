import roslibpy
from pykafka import KafkaClient
import json
import time

#used to kill the script after 5 iterations
execution_counter = 0

def callback(msg):
    #first kafka host is for internal connections, second is for docker-networked connections
    # KAFKA_HOST = "localhost:9094" 
    KAFKA_HOST = "kafka_container:9093"
    client = KafkaClient(hosts = KAFKA_HOST)
    topic = client.topics["LazerScan"]

    global execution_counter
    execution_counter+=1
    print("Execution counter: " + str(execution_counter))

    with topic.get_sync_producer() as producer:
        msg_encoded = json.dumps(msg).encode("utf-8")
        producer.produce(msg_encoded)
        print(msg)
    

def main():
    ros = roslibpy.Ros(host='192.168.1.131', port=9090)
    ros.run()
    print(str(ros.is_connected))

    #sleep added because the consume docker image takes longer to start up
    time.sleep(7)
    print("sleeping for 7 seconds")

    listener = roslibpy.Topic(ros, '/scan', 'sensor_msgs/LaserScan')
    listener.subscribe(callback)

    global execution_counter
    try:
        while execution_counter <= 5:
            pass
    except KeyboardInterrupt:
        ros.terminate()



"""
Below is deprecated code left behind for future reference.
A productionized version could delete it.
"""

def consumer_defined(topic):
    """
    DEPRECATED
    """
    consumer = topic.get_simple_consumer(consumer_group="mygroup",reset_offset_on_start=True)
    consumer.commit_offsets()
    for message in consumer:
        if message is not None:
            print(message.offset, message.value)

def main_original():
    """
    DEPRECATED
    """
    # ros = roslibpy.Ros(host='192.168.1.131', port=9090)
    # ros.run()

    # KAFKA_HOST = "localhost:9094" <-for external connections
    KAFKA_HOST = "kafka_container:9093"
    print("KAFKA_HOST = "+KAFKA_HOST)
    client = KafkaClient(hosts = KAFKA_HOST)
    topic = client.topics["LazerScan"]

    # listener = roslibpy.Topic(ros, '/scan', 'sensor_msgs/LaserScan')
    
    with topic.get_sync_producer() as producer:
        # listener.subscribe(lambda message: print('Heard talking: ' + str(message)))
        for i in range(10):
            message = "Test message " + str(i)
            encoded_message = message.encode("utf-8")
            producer.produce(encoded_message)

    consumer_defined(topic)

    # try:
    #     while True:
    #         pass
    # except KeyboardInterrupt:
    #     ros.terminate()

def test_consumer():
    """
    DEPRECATED
    """
    KAFKA_HOST = "0.0.0.0:9093" 
    client = KafkaClient(hosts = KAFKA_HOST)
    topic = client.topics["LazerScan"]
    consumer_defined(topic)

"""
End deprecated code
"""


if __name__ == "__main__":
    main()
