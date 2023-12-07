import pika

from worker_functions import read_file

# COMMUNICATION SETUP
# Input Queue
params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='toworkers')

# Output Queue
channel.queue_declare(queue='tooutput')


# CALLBACK FUNCTION
def callback(ch, method, properties, message):
    """
    Callback function that processes the received message and sends it to the outputter.

    Args:
        ch: The channel object.
        method: The method object.
        properties: The properties object.
        message: The received message.

    Returns:
        None
    """
    #channel.basic_ack(delivery_tag=method.delivery_tag)
    
    # processing the received message
    compressed_data = read_file(message)

    # sending processed data to outputter
    channel.basic_publish(exchange='', routing_key='tooutput', body=compressed_data)
    print("Processed and sent to outputter.")

# MAIN
channel.basic_consume(queue='toworkers', auto_ack=True, on_message_callback=callback)
print('Waiting for messages.')
channel.start_consuming()


