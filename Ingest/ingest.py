import roslibpy
from pykafka import KafkaClient


def callback(msg):
    print(msg)

def consumer_defined(topic):
    consumer = topic.get_simple_consumer(consumer_group="mygroup",reset_offset_on_start=True)
    consumer.commit_offsets()
    for message in consumer:
        if message is not None:
            print(message.offset, message.value)

def main():
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
    KAFKA_HOST = "0.0.0.0:9093" 
    client = KafkaClient(hosts = KAFKA_HOST)
    topic = client.topics["LazerScan"]
    consumer_defined(topic)

if __name__ == "__main__":
    main()
    # test_consumer()
