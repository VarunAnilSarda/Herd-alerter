from faust import App

app = App('faust_app', broker='kafka://localhost:9092')

topic = app.topic('test-topic', value_type=str)  # Accept plain text

@app.agent(topic)
async def process(messages):
    async for message in messages:
        print(message)  # Prints plain text messages
