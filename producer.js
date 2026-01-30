const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-producer',
  brokers: ['localhost:9092']
});

const producer = kafka.producer();

const run = async () => {
  await producer.connect();
  const messages = [
    { value: 'Hello Kafka' },
    { value: 'This is a test message' },
    { value: 'Another message' }
  ];
  await producer.send({
    topic: 'test-topic',
    messages: messages
  });
  console.log('Messages sent successfully');
  await producer.disconnect();
};

run().catch(console.error);
