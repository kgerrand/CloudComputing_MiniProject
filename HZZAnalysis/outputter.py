import uproot # for reading .root files
import awkward as ak # to represent nested data in columnar format
import vector # for 4-momentum calculations
import time # to measure time to analyse
import numpy as np # for numerical calculations such as histogramming
import matplotlib.pyplot as plt # for plotting
from matplotlib.ticker import AutoMinorLocator # for minor ticks

import pika
import json
import gzip

import infofile # local file containing cross-sections, sums of weights, dataset IDs

# IMPORT FUNCTIONS
from functions import plot_data

# SAMPLES
samples = {

    'data': {
        'list' : ['data_A','data_B','data_C','data_D'],
    },

    r'Background $Z,t\bar{t}$' : { # Z + ttbar
        'list' : ['Zee','Zmumu','ttbar_lep'],
        'color' : "#6b59d3" # purple
    },

    r'Background $ZZ^*$' : { # ZZ
        'list' : ['llll'],
        'color' : "#ff0000" # red
    },

    r'Signal ($m_H$ = 125 GeV)' : { # H -> ZZ -> llll
        'list' : ['ggH125_ZZ4lep','VBFH125_ZZ4lep','WH125_ZZ4lep','ZH125_ZZ4lep'],
        'color' : "#00cdff" # light blue
    },

}

message_count = 0
message_threshold = 12


# creating dictionary to add recieved arrays to, referenced by their name
full_data_dict = {}

def callback(ch, method, properties, message):

    global message_count

    print("recieved")

    decompressed_data = gzip.decompress(message)
    #data_dict = decompressed_data.decode('utf-8')
    data_dict = json.loads(decompressed_data)

    name = data_dict.get('name', None)
    data = data_dict.get('data', None)

    data = ak.from_iter(data)

    full_data_dict[name] = data
    print(name)

    print("slay")

    message_count += 1

    if message_count >= message_threshold:
        channel.stop_consuming()
        print("All messages recieved.")


params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='output')

channel.basic_consume(queue='output', auto_ack=True, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


def prepare_to_plot(full_data_dict):
    sorted_dict = {}

    for s in samples:
        frames = []
        for key in full_data_dict:
            if key in samples[s]['list']:
                frames.append(full_data_dict[key])
        
        sorted_dict[s] = ak.concatenate(frames)

    return sorted_dict

print(full_data_dict.keys())
plotting_dict = prepare_to_plot(full_data_dict)
plot_data(plotting_dict)
'''
data_to_plot = {}
n = 1

for s in samples:
    print(n)
    data_to_plot[s] = ak.concatenate(frames)
    n+=1

plot_data(data_to_plot, samples)
'''


# recieve awkward array from worker(s)
# add to list
# when list is length we expect, concatenate
# plot concatenated data


#plot_data(data, samples)


