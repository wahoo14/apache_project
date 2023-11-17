import roslibpy
from pykafka import KafkaClient
import json

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



def callback(msg):
    #first kafka host is for internal connections, second is for docker-networked connections
    # KAFKA_HOST = "localhost:9094" 
    KAFKA_HOST = "kafka_container:9093"
    print("KAFKA_HOST = "+KAFKA_HOST)
    client = KafkaClient(hosts = KAFKA_HOST)
    topic = client.topics["LazerScan"]
    print("4")
    with topic.get_sync_producer() as producer:
        msg_encoded = json.dumps(msg).encode("utf-8")
        print("5")
        producer.produce(msg_encoded)
        print("6")

def main():
    ros = roslibpy.Ros(host='192.168.1.131', port=9090)
    ros.run()
    print("1")
    #first kafka host is for internal connections, second is for docker-networked connections
    # KAFKA_HOST = "localhost:9094" 
    KAFKA_HOST = "kafka_container:9093"
    client = KafkaClient(hosts = KAFKA_HOST)
    topic = client.topics["LazerScan"]

    listener = roslibpy.Topic(ros, '/scan', 'sensor_msgs/LaserScan')
    print("2")
    with topic.get_sync_producer() as producer:
        print("3")
        listener.subscribe(callback)
        # data_encoded = str(callback_data).encode("utf-8")
        # producer.produce(data_encoded)
        

    # consumer_defined(topic)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        ros.terminate()

if __name__ == "__main__":
    main()
    # test_consumer()
