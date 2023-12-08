import pika, time

from worker_functions import read_file

# COMMUNICATION SETUP
# establishing connection to RabbitMQ and retrying if it fails
for n in range(10):
    try:
        params = pika.ConnectionParameters(host='rabbitmq', heartbeat=600)
        connection = pika.BlockingConnection(params)
        break
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ after {n+1} attempt(s). Retrying.")
        time.sleep(7)
channel = connection.channel()

# Input Queue
channel.queue_declare(queue='data_processing')

# Output Queue
channel.queue_declare(queue='data_rendering')

# Limiting the number of unacknowledged messages on a channel to 1
channel.basic_qos(prefetch_count=1)


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
    # acknowledging the message
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Received {message} from inputter.")
    
    # processing the received message
    compressed_data = read_file(message)

    # sending processed data to outputter
    ch.basic_publish(exchange='', routing_key='data_rendering', body=compressed_data)
    print("Data processed and sent to outputter.")

# MAIN
channel.basic_consume(queue='data_processing', auto_ack=False, on_message_callback=callback)
print('Waiting for messages.')
channel.start_consuming()


