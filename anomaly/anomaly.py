from confluent_kafka import Consumer
import os


KAFKA_BROKER = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
conf = {
    'bootstrap.servers': KAFKA_BROKER  ,
    'group.id': 'consumer_anomaly_group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
}

consumer = Consumer(conf)

consumer.subscribe(['raw_data_topic'])
print("Consumer Start")
try:
    while True:
        print("in loop")
        msg = consumer.poll(1.0)
        if msg is None:
            print("in msg None")
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        print(f"Received message: {msg.value().decode('utf-8')} from {msg.topic()}")
finally:
    print("in finally")
    consumer.close()