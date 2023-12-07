import pika

# IMPORT FUNCTIONS
from functions import get_file_names

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

# communication setup
params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='messages')

# determine file strings to send (includes sample name and prefix for url)
data = get_file_names(samples)

# sends file strings to worker(s)
for message in data:
    channel.basic_publish(exchange='',
    routing_key='messages',
    body=message)
    print(f" [x] Sent {message}")

print(" [x] Sent all messages")