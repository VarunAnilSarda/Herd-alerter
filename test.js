const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
});

const producer = kafka.producer();
const consumer = kafka.consumer({ groupId: 'test-group' });

const run = async () => {
  // Producer
  await producer.connect();
  await producer.send({
    topic: 'test-topic',
    messages: [
      { value: 'Hello Kafka' },
      { value: 'This is a test message' },
      { value: 'Another message' }
    ]
  });
  console.log('Messages sent');

  // Consumer
  await consumer.connect();
  await consumer.subscribe({ topic: 'test-topic', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ message }) => {
      console.log(`Received: ${message.value.toString()}`);
    }
  });
};

run().catch(console.error);
