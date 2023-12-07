import pika
from inputter_functions import *

# communication setup - input queue
params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='toworkers')


# extracting samples from samples.json and from that determining file strings to send
# (includes sample name and prefix for url)
samples = extract_samples()
filestrings = get_file_string(samples)

# sends file strings to worker(s)
for string in filestrings:
    channel.basic_publish(exchange='',
    routing_key='toworkers',
    body=string)
    print(f"Sent {string}")

print("Sent all messages!")