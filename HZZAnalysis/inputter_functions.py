import infofile
import json

# CONSTANTS
lumi = 10

fraction = 0.1

tuple_path = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/" # web address

MeV = 0.001
GeV = 1.0


def extract_samples():
    """
    Extracts samples from the 'samples.json' file and returns them.
    
    Returns:
        dict: A dictionary containing the extracted samples.
    """
    with open('samples.json') as f:
        samples = json.load(f)
    return samples


def get_file_string(samples):
    """
    Returns a list of file names based on the given samples.

    Parameters:
    samples (dict): A dictionary containing sample information.

    Returns:
    messages: A list of file names and prefixes (messages to send to workers)

    """
    messages = [] # define empty list to hold messages to send to workers
    
    for s in samples: # loop over samples
        for val in samples[s]['list']: # loop over each file
            if s == 'data':
                prefix = "Data/"
            else:
                prefix = "MC/mc_"+str(infofile.infos[val]["DSID"])+"."
            
            message = prefix+" "+val
            messages.append(message) # append file message to list of messages

    return messages # return list of messages to send to workers
