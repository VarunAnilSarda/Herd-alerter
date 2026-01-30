# consumer.py
from kafka import KafkaConsumer

def main():
    consumer = KafkaConsumer(
        'test-topic',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id="my-group",
        value_deserializer=lambda x: x.decode('utf-8')  # just decode string, no JSON
    )

    print("🚀 Consumer is running... Waiting for messages.")
    
    try:
        for message in consumer:
            print(f"Received: {message.value}")
    except KeyboardInterrupt:
        print("\n❌ Stopped by user")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
