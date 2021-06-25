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

### count the holes total, incl.DUT
hole_1 = []
hole_1_dut = []
hole_2 = []
hole_2_dut = []
hole_3 = []
hole_3_dut = []

#definition to exclude zeros from start and beginning of a list_line
def clear_seq(list):
    while list[-1] == 1:
        list.pop(-1)
    while list[0] == 1:
        list.pop(0)

#go into a run 
for event in hit_data:
    #these are container to be later able to store, how many n-p-e's have how many holes
    holes=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],
    [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    # look in events with high number >=4 of involved planes (n-plane-events) 
    if hit_data[event]["number_of_planes"] >= 4:

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
        num_holes = sum.seq

        # if at least one hole is there
        if num_holes > 0:
            if num_holes == 1:
                if sum(np.array(seq[j][k][i]) == 4) ==1:
                    holes[3][k] += 1
                holes[0][k] += 1
            elif num_holes == 2:
                if sum(np.array(seq[j][k][i]) == 4) ==1:
                    holes[4][k] += 1
                holes[1][k] += 1
            elif num_holes == 3:
                print(seq[j][k][i])
                if sum(np.array(seq[j][k][i]) == 4) ==1:
                    holes[5][k] += 1
                holes[2][k] += 1
    hole_1.append(holes[0])
    hole_1_dut.append(holes[3])
    hole_2.append(holes[1])
    hole_2_dut.append(holes[4])
    hole_3.append(holes[2])
    hole_3_dut.append(holes[5])
    

#######################---CSV   CSV   CSV   CSV---#############################


###creating a csv file
with open("3_Manual_Analysis/csv/n-event-plane-data.csv","w", newline="") as f:

    #creating the the header
    header = ["RunNumber"," pE_1", " pE_2", " pE_3", " pE_4", " pE_5", " pE_6", " pE_7"]
    writing = csv.DictWriter(f, fieldnames= header)

    # write the header in the file
    writing.writeheader()
    
    # put in the values
    for j in range(len(run)):
        writing.writerow({"RunNumber" : run[j]," pE_1" : pE[j][0], " pE_2" : pE[j][1], " pE_3" : pE[j][2],
         " pE_4" : pE[j][3], " pE_5" : pE[j][4], " pE_6" : pE[j][5], " pE_7" : pE[j][6]})

###creating a csv file
with open("3_Manual_Analysis/csv/hits_per_plane.csv","w", newline="") as f:

    #creating the the header
    header = ["RunNumber"," hpP_1", " hpP_2", " hpP_3", " hpP_4", " hpP_5", " hpP_6", " hpP_7", " total_N"]
    writing = csv.DictWriter(f, fieldnames= header)

    # write the header in the file
    writing.writeheader()
    
    # put in the values
    for j in range(len(run)):
        writing.writerow({"RunNumber" : run[j]," hpP_1" : hits_plane[j][0], " hpP_2" : hits_plane[j][1],
         " hpP_3" : hits_plane[j][2]," hpP_4" : hits_plane[j][3], " hpP_5" : hits_plane[j][4], " hpP_6" : hits_plane[j][5],
          " hpP_7" : hits_plane[j][6], " total_N" : sum(hits_plane[j])})

# csv file
with open("3_Manual_Analysis/csv/DUT_n-event-plane-data.csv","w", newline="") as f:

    #creating the the header
    header = ["RunNumber"," pE_1", " pE_2", " pE_3", " pE_4", " pE_5", " pE_6", " pE_7"]
    writing = csv.DictWriter(f, fieldnames= header)

    # write the header in the file
    writing.writeheader()
    
    # put in the values
    for j in range(len(run)):
        writing.writerow({"RunNumber" : run[j]," pE_1" : dut[j][0], " pE_2" : dut[j][1],
         " pE_3" : dut[j][2], " pE_4" : dut[j][3], " pE_5" : dut[j][4], " pE_6" : dut[j][5],
          " pE_7" : dut[j][6]})


###creating a csv file SEQUENCE
with open("3_Manual_Analysis/csv/event_HOLES-data.csv","w", newline="") as f:

    #creating the the header
    header = ["RunNumber"," s2_h1", " s3_h1", " s3_h2", " s4_h1", " s4_h2", " s4_h3",
     " s5_h1", " s5_h2", " s6_h1"]
    writing = csv.DictWriter(f, fieldnames= header)

    # write the header in the file
    writing.writeheader()
    
    # put in the values
    for j in range(len(run)):
        writing.writerow({"RunNumber" : run[j]," s2_h1" : hole_1[j][0], " s3_h1" : hole_1[j][1],
         " s3_h2" : hole_2[j][1], " s4_h1" : hole_1[j][2], " s4_h2" : hole_2[j][2],
          " s4_h3" : hole_3[j][5], " s5_h1" : hole_1[j][3], " s5_h2" : hole_2[j][3],
           " s6_h1" : hole_1[j][4]})

###creating a csv file SEQUENCE DUT
with open("3_Manual_Analysis/csv/event_HOLES_DUT-data.csv","w", newline="") as f:

    #creating the the header
    header = ["RunNumber"," s2_h1", " s3_h1", " s3_h2", " s4_h1", " s4_h2", " s4_h3",
     " s5_h1", " s5_h2", " s6_h1"]
    writing = csv.DictWriter(f, fieldnames= header)

    # write the header in the file
    writing.writeheader()
    
    # put in the values
    for j in range(len(run)):
        writing.writerow({"RunNumber" : run[j]," s2_h1" : hole_1_dut[j][0], " s3_h1" : hole_1_dut[j][1],
         " s3_h2" : hole_2_dut[j][1], " s4_h1" : hole_1_dut[j][2], " s4_h2" : hole_2_dut[j][2],
          " s4_h3" : hole_3_dut[j][5], " s5_h1" : hole_1_dut[j][3], " s5_h2" : hole_2_dut[j][3],
           " s6_h1" : hole_1_dut[j][4]})
