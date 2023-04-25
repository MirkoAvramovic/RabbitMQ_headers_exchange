import pika
from pika.exchange_type import ExchangeType

def on_message_received(ch, method, properties, body):
    print(f"Received new message: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange="headersexchange", exchange_type=ExchangeType.headers)

channel.queue_declare(queue='letterbox')

'''
When the x-match is set to 'any': the message of the producer will be consumed if ANY argument the producer
publishes in basic properties match with ANY argument in bind_args, 
When the x-match is set to 'all': the message will only be consumed if all arguments of basic properties of
producer match with all bind arguments of consumer.
'''

bind_args = {
    'x-match': 'any', 
    'name': 'mire',
    'age': '30'
}

channel.queue_bind('letterbox', 'headersexchange', arguments=bind_args)

channel.basic_consume(queue='letterbox', auto_ack=True, 
                      on_message_callback=on_message_received)

print("Starting Consuming")

channel.start_consuming()