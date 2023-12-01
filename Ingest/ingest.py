from pykafka import KafkaClient
import random
    

def main():
    #first kafka host is for internal connections, second is for docker-networked connections
    # KAFKA_HOST = "localhost:9094" 
    KAFKA_HOST = "kafka_container:9093"
    client = KafkaClient(hosts = KAFKA_HOST)
    topic = client.topics["RandomNumber"]

    execution_counter = 0
    while execution_counter < 50:
        with topic.get_sync_producer() as producer:
            msg_encoded = str(random.randint(100,999)).encode("utf-8")
            producer.produce(msg_encoded)
            execution_counter += 1


if __name__ == "__main__":
    main()
