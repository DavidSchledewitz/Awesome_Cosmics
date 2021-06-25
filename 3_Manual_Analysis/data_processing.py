#!/usr/bin/python

# loading packages
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import tempfile
import subprocess
import csv


from muon_data import hit_data

# container
holes=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]#holes[number of holes][n-plane-event]
n_p_e = [0,0,0,0,0,0,0] #number of n-plane-events
hits = [0,0,0,0,0,0,0] #number of hits per plane

#definition to exclude zeros from start and beginning of a list_line
def clear_seq(list):
    while list[-1] == 1:
        list.pop(-1)
    while list[0] == 1:
        list.pop(0)


for event in range(len(hit_data)):

    ### count number of n-plane-events and the number of hits per plane
    n_p_e[hit_data[event]["number_of_planes"]-1] +=1
    #check which planes fired
    for i in range(7):
        if hit_data[event][i]["XC"] != -1:
            hits[i] +=1
        

    ### count the holes total (depending on the number of involved planes)

    # look in events with high number >=2 of involved planes (n-plane-events) 
    if hit_data[event]["number_of_planes"] >= 2:

        npe = hit_data[event]["number_of_planes"]
        seq=[0,0,0,0,0,0,0]
        # look through every plane, if there is a hole
        for i in range(7):
            #-1 signs a plane without a hit
            if hit_data[event][i]["XC"] == -1:
                #now a hole is marked as 1 in the sequence 
                seq[i]= 1
        #clear the beginning and end of the sequence, for example [1,0,0,0,0,0,1] -> [0,0,0,0,0], since gaps at the beginning and at the end are not part of the sequnce of hitted planes
        clear_seq(seq)
        num_holes = sum(seq)

        # if at least one hole is there
        if num_holes > 0:
            if num_holes == 1:
                holes[0][npe-2] += 1
            elif num_holes == 2:
                holes[1][npe-2] += 1
            elif num_holes == 3:
                holes[2][npe-2] += 1


    




#######################---CSV   CSV   CSV   CSV---#############################


###creating a csv file
with open("3_Manual_Analysis/csv/npe_data.csv","w", newline="") as f:

    #creating the the header
    header = [" pE_1", " pE_2", " pE_3", " pE_4", " pE_5", " pE_6", " pE_7"," total_N" ]
    writing = csv.DictWriter(f, fieldnames= header)

    # write the header in the file
    writing.writeheader()
    
    ### put in the values of N-PLANE-EVENTS
    writing.writerow({" pE_1" : n_p_e[0], " pE_2" : n_p_e[1], " pE_3" : n_p_e[2],
        " pE_4" : n_p_e[3], " pE_5" : n_p_e[4], " pE_6" : n_p_e[5], " pE_7" : n_p_e[6]," total_N" : sum(n_p_e)})


###creating a csv file
with open("3_Manual_Analysis/csv/hitpp_data.csv","w", newline="") as f:

    #creating the the header
    header = [" pE_1", " pE_2", " pE_3", " pE_4", " pE_5", " pE_6", " pE_7"," total_N" ]
    writing = csv.DictWriter(f, fieldnames= header)

    # write the header in the file
    writing.writeheader()

    ### put in the values of hits per plane
    writing.writerow({" pE_1" : hits[0], " pE_2" : hits[1],
        " pE_3" : hits[2]," pE_4" : hits[3], " pE_5" : hits[4], " pE_6" : hits[5],
        " pE_7" : hits[6], " total_N" : sum(hits)})


###creating a csv file SEQUENCE
with open("3_Manual_Analysis/csv/event_HOLES-data.csv","w", newline="") as f:

    #creating the the header
    header = [" s2_h1", " s3_h1", " s3_h2", " s4_h1", " s4_h2", " s4_h3",
     " s5_h1", " s5_h2", " s6_h1"]
    writing = csv.DictWriter(f, fieldnames= header)

    # write the header in the file
    writing.writeheader()
    
    # put in the values

    writing.writerow({" s2_h1" : holes[0][0], " s3_h1" : holes[0][1],
        " s3_h2" : holes[1][1], " s4_h1" : holes[0][2], " s4_h2" : holes[1][2],
        " s4_h3" : holes[2][2], " s5_h1" : holes[0][3], " s5_h2" : holes[1][3],
        " s6_h1" : holes[0][4]})
