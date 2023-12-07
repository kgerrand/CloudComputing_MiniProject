import pika
import json
import zlib

# IMPORT FUNCTIONS
from functions import *

# function for recieving file strings, reading data and sending to outputter
def callback(ch, method, properties, message):
    # recieve data from inputter
    # channel.basic_ack(delivery_tag=method.delivery_tag)
    
    # process data
    compressed_data=read_file(message)
    print(type(compressed_data))
    print("Data processed")

    # send data to outputter
    channel.basic_publish(exchange='',routing_key='output',body=compressed_data)
    print("sent")

# communication setup

# input queue
params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='messages')

channel.basic_consume(queue='messages', auto_ack=True, on_message_callback=callback)


# output queue
channel.queue_declare(queue='output')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


