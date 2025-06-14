from flask import Flask, jsonify
from confluent_kafka import Consumer, KafkaException
import threading

# Flask app
app = Flask(__name__)

# Global store for consumed messages
consumed_messages = []

# Kafka consumer configuration
 conf = {'bootstrap.servers':  os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')}

# Topic name
topic = 'inc_alert_data'

def kafka_consumer():
    consumer = Consumer(conf)
    consumer.subscribe([topic])
    print(f"Subscribed to topic: {topic}")

    try:
        while True:
            msg = consumer.poll(1.0)  # timeout in seconds
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                message = msg.value().decode('utf-8')
                print(f"Received message: {message}")
                consumed_messages.append(message)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

# Start Kafka consumer in background thread
threading.Thread(target=kafka_consumer, daemon=True).start()

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(consumed_messages)

if __name__ == '__main__':
    app.run(port=8083, debug=True)
