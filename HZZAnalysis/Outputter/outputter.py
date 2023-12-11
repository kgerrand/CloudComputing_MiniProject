import awkward as ak
import pika, json, gzip, time


# IMPORT FUNCTIONS
from outputter_functions import *


# VARIABLE SETUP
samples = extract_samples()

message_count = 0 # variable for the number of messages recieved
message_threshold = 0 # variable for the number of messages expected
for key in samples:
    message_threshold += len(samples[key]['list'])

full_data_dict = {} # dictionary to store all recieved data


# COMMUNICATION SETUP
# establishing connection to RabbitMQ and retrying if it fails
for n in range(10):
    try:
        params = pika.ConnectionParameters(host='rabbitmq')
        connection = pika.BlockingConnection(params)
        start = time.time()
        break
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ after {n+1} attempt(s). Retrying.")
        time.sleep(7)
channel = connection.channel()
channel.queue_declare(queue='data_rendering')


# Callback function
def callback(ch, method, properties, message):
    """
    Callback function that recieves data and adds it to full_data_dict.

    Parameters:
    ch (Channel): The channel object.
    method (Method): The method object.
    properties (Properties): The properties object.
    message (bytes): The received message.

    """
    global message_count

    # preparing recieved data for use
    decompressed_data = gzip.decompress(message)
    data_dict = json.loads(decompressed_data)

    # extracting data from data_dict
    name = data_dict.get('name', None)
    data = data_dict.get('data', None)

    data = ak.from_iter(data)

    print(f"Received {name}.")

    # adding data to full_data_dict (if it's not already there - in case of multiple workers/poor communication)
    if name in full_data_dict.keys():
        print(f"Duplicate {name} recieved. Discarding.")
    else:
        full_data_dict[name] = data

        message_count += 1
    
    # stopping the consumer when all messages have been recieved
    if message_count >= message_threshold:
        channel.stop_consuming()
        print("All samples received!")
    else:
        print(f"Received {message_count} processed dataset(s). Waiting for {message_threshold - message_count} more.")


# MAIN
channel.basic_consume(queue='data_rendering', auto_ack=True, on_message_callback=callback)
print(f'Waiting for data from workers. Expecting {message_threshold} sample(s).')
channel.start_consuming()
# closing the connection once all data is received
connection.close()

plotting_dict = prepare_to_plot(full_data_dict, samples)
plot_data(plotting_dict, samples)

end = time.time()
time_taken = end - start
print(f"Time taken: {time_taken:.1f} seconds.")