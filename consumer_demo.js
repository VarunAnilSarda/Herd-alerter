const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'demo-consumer',
  brokers: ['localhost:9092']
});

const consumer = kafka.consumer({ groupId: 'demo-group' });

const runConsumer = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'test-topic', fromBeginning: true });

  console.log("🚀 Consumer is running... Waiting for messages.");

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      console.log(`📥 Received message: ${message.value.toString()}`);
    }
  });
};

runConsumer().catch(console.error);
