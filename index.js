const { Kafka } = require('kafkajs');

// Kafka connection
const kafka = new Kafka({
  clientId: 'herd-alerter-app',
  brokers: ['localhost:9092'], // matches your Docker Kafka container
});

const producer = kafka.producer();
const consumer = kafka.consumer({ groupId: 'herd-alerter-group' });

const run = async () => {
  try {
    // Connect producer & consumer
    await producer.connect();
    console.log('Producer connected');
    await consumer.connect();
    console.log('Consumer connected');

    // Subscribe to topic
    await consumer.subscribe({ topic: 'herd-alert-topic', fromBeginning: true });

    // Consume messages
    consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        console.log(`Received message: ${message.value.toString()}`);
      },
    });

    // Send test message
    await producer.send({
      topic: 'herd-alert-topic',
      messages: [{ value: 'Hello from herd-alerter backend!' }],
    });

    console.log('Test message sent');
  } catch (error) {
    console.error('Error in Kafka setup:', error);
  }
};

run();
