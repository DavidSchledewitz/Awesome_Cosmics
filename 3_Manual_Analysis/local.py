import matplotlib.pyplot as plt
import numpy as np
import json
import os

file = 'example.json'
output = "muon_data.py"

# Create Event Structure
hit_data = []
event_no = 0

with open(file) as json_file:
    data = json.load(json_file);

# Event loop
for event in data:

    # Don't write events that are empty
    if len(event) == 0:
        print("Event {} empty, skipped".format(event_no))
        continue

    # Create a dictionary for each event
    hit_data.append({})

    # Create an entry for each plane
    for plane in range(7):
        hit_data[event_no][plane] = {}
        hit_data[event_no][plane]["X"] = []
        hit_data[event_no][plane]["Y"] = []

    # Read out pixel by pixel
    for obj in event:

        # Find out which plane
        plane = int(obj["m_detectorID"].split("_")[1])
        hit_data[event_no][plane]["X"].append(int(obj["m_column"]))
        hit_data[event_no][plane]["Y"].append(int(obj["m_row"]))
    
    event_no+=1

# For each empty plane, substract one from 7
for event in range(len(hit_data)):

    total_planes = 7

    for plane in range(7):
        if not hit_data[event][plane]["X"]:
            hit_data[event][plane]["X"].append(-1)
            hit_data[event][plane]["Y"].append(-1)
            total_planes -= 1

    hit_data[event]["number_of_planes"] = total_planes

with open(output, 'w') as f:
    f.write("hit_data = ")
    f.write("%s" % hit_data)
