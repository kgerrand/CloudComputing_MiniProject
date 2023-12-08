import pika, time
from inputter_functions import *

# COMMUNICATION SETUP
# establishing connection to RabbitMQ and retrying if it fails
for n in range(10):
    try:
        params = pika.ConnectionParameters(host='rabbitmq')
        connection = pika.BlockingConnection(params)
        break
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ after {n+1} attempt(s). Retrying.")
        time.sleep(7)
channel = connection.channel()
channel.queue_declare(queue='data_processing')


# MAIN
# extracting samples from samples.json and from that determining file strings to send
# (includes sample name and prefix for url)
samples = extract_samples()
filestrings = get_file_string(samples)

# sends file strings to worker(s)
for string in filestrings:
    channel.basic_publish(exchange='',
    routing_key='data_processing',
    body=string)
    print(f"Sent {string}")

print("Sent all messages!")

# closing the connection once all messages have been sent
connection.close()