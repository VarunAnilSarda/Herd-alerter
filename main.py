from kafka import KafkaProducer, KafkaConsumer
import threading
import time

# Kafka configuration
BROKER = 'localhost:9092'
TOPIC = 'herd-alert-topic'

# Create producer
producer = KafkaProducer(bootstrap_servers=BROKER)

# Create consumer with a unique group_id
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    auto_offset_reset='earliest',
    group_id='herd-alerter-group-1',
    consumer_timeout_ms=1000
)

# Function to continuously produce messages
def produce_messages():
    count = 1
    while True:
        message = f"Herd alert message {count}"
        producer.send(TOPIC, message.encode('utf-8'))
        producer.flush()
        print(f"[Producer] Sent: {message}")
        count += 1
        time.sleep(3)  # send message every 3 seconds

# Function to continuously consume messages
def consume_messages():
    print("[Consumer] Starting consumer...")
    while True:
        for message in consumer:
            print(f"[Consumer] Received: {message.value.decode('utf-8')}")

# Run producer and consumer in separate threads
if __name__ == "__main__":
    producer_thread = threading.Thread(target=produce_messages)
    consumer_thread = threading.Thread(target=consume_messages)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
