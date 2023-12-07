import uproot
import awkward as ak 
import vector
import json
import gzip
import sys

sys.path.append('../') # add parent directory to path to import infofile
import infofile

# CONSTANTS
fraction = 0.1
lumi = 10
MeV = 0.001

tuple_path = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/" # web address

# FUNCTIONS
def read_file(string):
    """
    Reads a file and performs data processing on the contents.

    Args:
        string (bytes): An input string containing information to extract the file url

    Returns:
        bytes: The compressed and serialized data.

    """    
    string = string.decode('utf-8')
    prefix = string.split()[0] # get prefix from message
    sample = string.split()[1] # get sample name from message

    # define file name to open
    path = tuple_path+prefix+sample+".4lep.root"

    print("Processing: "+sample) # print which sample is being processed
    data_all = [] # define empty list to hold all data for this sample
    
    # open the tree called mini using a context manager (will automatically close files/resources)
    with uproot.open(path + ":mini") as tree:
        numevents = tree.num_entries # number of events
        if 'data' not in sample: xsec_weight = get_xsec_weight(sample) # get cross-section weight
        for data in tree.iterate(['lep_pt','lep_eta','lep_phi',
                                  'lep_E','lep_charge','lep_type', 
                                  # add more variables here if you make cuts on them 
                                  'mcWeight','scaleFactor_PILEUP',
                                  'scaleFactor_ELE','scaleFactor_MUON',
                                  'scaleFactor_LepTRIGGER'], # variables to calculate Monte Carlo weight
                                 library="ak", # choose output type as awkward array
                                 entry_stop=numevents*fraction): # process up to numevents*fraction

            if 'data' not in sample: # only do this for Monte Carlo simulation files
                # multiply all Monte Carlo weights and scale factors together to give total weight
                data['totalWeight'] = calc_weight(xsec_weight, data)

            # cut on lepton charge using the function cut_lep_charge defined above
            data = data[~cut_lep_charge(data.lep_charge)]

            # cut on lepton type using the function cut_lep_type defined above
            data = data[~cut_lep_type(data.lep_type)]

            # calculation of 4-lepton invariant mass using the function calc_mllll defined above
            data['mllll'] = calc_mllll(data.lep_pt, data.lep_eta, data.lep_phi, data.lep_E)
            
            data_all.append(data) # append array from this batch
    

    # return array containing events passing all cuts   
    data = ak.concatenate(data_all) 
    
    # serialise the data (for easier transfer)
    serialised_data = ak.to_list(data) 

    # sending as a dictionary to allow for sample name to be sent with the data
    data_dict = {"name": sample, "data": serialised_data}
    
    # compressing the data to reduce the size of the message
    json_dict = json.dumps(data_dict)
    compressed_data = gzip.compress(json_dict.encode('utf-8'))

    return compressed_data


def calc_weight(xsec_weight, events):
    """
    Calculates the total weight for each event.
    Called in read_file().

    Args:
        xsec_weight (float): The cross-section weight.
        events (awkward.array): The events data.

    Returns:
        awkward.array: The total weight for each event.

    """
    return (
        xsec_weight
        * events.mcWeight
        * events.scaleFactor_PILEUP
        * events.scaleFactor_ELE
        * events.scaleFactor_MUON 
        * events.scaleFactor_LepTRIGGER
    )


def get_xsec_weight(sample):
    """
    Calculates the cross-section weight for a given sample.
    Called in read_file().

    Args:
        sample (str): The sample name.

    Returns:
        float: The cross-section weight.

    """
    info = infofile.infos[sample] # open infofile
    xsec_weight = (lumi*1000*info["xsec"])/(info["sumw"]*info["red_eff"]) #*1000 to go from fb-1 to pb-1
    return xsec_weight # return cross-section weight


def calc_mllll(lep_pt, lep_eta, lep_phi, lep_E):
    """
    Calculates the 4-lepton invariant mass.
    Called in read_file().

    Args:
        lep_pt (awkward.array)
        lep_eta (awkward.array)
        lep_phi (awkward.array)
        lep_E (awkward.array)

    Returns:
        awkward.array: The 4-lepton invariant mass.

    """
    # construct awkward 4-vector array
    p4 = vector.zip({"pt": lep_pt, "eta": lep_eta, "phi": lep_phi, "E": lep_E})
    # calculate invariant mass of first 4 leptons
    # [:, i] selects the i-th lepton in each event
    # .M calculates the invariant mass
    return (p4[:, 0] + p4[:, 1] + p4[:, 2] + p4[:, 3]).M * MeV


def cut_lep_charge(lep_charge):
    """
    Cuts on the lepton charge.
    Called in read_file().

    Args:
        lep_charge (awkward.array): The charge of the leptons.

    Returns:
        awkward.array: A boolean array indicating whether the lepton charge passes the cut.

    """
    # throw away when sum of lepton charges is not equal to 0
    # first lepton in each event is [:, 0], 2nd lepton is [:, 1] etc
    return lep_charge[:, 0] + lep_charge[:, 1] + lep_charge[:, 2] + lep_charge[:, 3] != 0


def cut_lep_type(lep_type):
    """
    Cuts on the lepton type.
    Called in read_file().

    Args:
        lep_type (awkward.array): The type of the leptons.

    Returns:
        awkward.array: A boolean array indicating whether the lepton type passes the cut.

    """
    # for an electron lep_type is 11
    # for a muon lep_type is 13
    # throw away when none of eeee, mumumumu, eemumu
    sum_lep_type = lep_type[:, 0] + lep_type[:, 1] + lep_type[:, 2] + lep_type[:, 3]
    return (sum_lep_type != 44) & (sum_lep_type != 48) & (sum_lep_type != 52)
