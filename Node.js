// stream_processor.js
const { Kafka } = require("kafkajs");

const kafka = new Kafka({
  clientId: "stream-processor",
  brokers: ["localhost:9092"], // adjust if docker-compose broker is different
});

const consumer = kafka.consumer({ groupId: "stream-processor-group" });
const producer = kafka.producer();

async function run() {
  await consumer.connect();
  await producer.connect();

  await consumer.subscribe({ topic: "herd-events", fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const event = JSON.parse(message.value.toString());

      // Example: filter only "alert" type events
      if (event.type === "ALERT") {
        const processed = {
          id: event.id,
          herdSize: event.herdSize,
          riskLevel: event.herdSize > 50 ? "HIGH" : "LOW",
          timestamp: Date.now(),
        };

        // publish processed data
        await producer.send({
          topic: "processed-events",
          messages: [{ value: JSON.stringify(processed) }],
        });

        console.log("Processed:", processed);
      }
    },
  });
}

run().catch(console.error);
