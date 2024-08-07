import asyncio
import aio_pika

async def send_message(message_body: str):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@localhost"
    )
    
    async with connection:
        channel = await connection.channel()
        
        queue = await channel.declare_queue("queue_test_receipt",durable=True)
        
        message = aio_pika.Message(
            body=message_body.encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await channel.default_exchange.publish(
            message, routing_key=queue.name
        )
        
        print(f'sent message')
        
message = "Hello mundo"

asyncio.run(send_message(message))