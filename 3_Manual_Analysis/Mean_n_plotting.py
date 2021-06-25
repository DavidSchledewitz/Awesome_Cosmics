#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import csv


# load data
data = np.loadtxt("3_Manual_Analysis/csv/npe_data.csv", delimiter=",", skiprows=1, usecols=(0,1,2,3,4,5,6),dtype=int)
#load number of hits per plane
data_hits = np.loadtxt("3_Manual_Analysis/csv/hitpp_data.csv", delimiter=",", skiprows=1, usecols=(0,1,2,3,4,5,6),dtype=int)
# load holes
data_holes = np.loadtxt("3_Manual_Analysis/csv/event_HOLES-data.csv", delimiter=",", skiprows=1, usecols=(0,1,2,3,4,5,6,7,8),dtype=int)


plane = np.arange(1, 8)
    

# holes
#differentiate different hole numbers
hole_1 = np.array([0, data_holes[0], data_holes[1], data_holes[3], data_holes[6], data_holes[8], 0])
hole_2 = np.array([0, 0, data_holes[2], data_holes[4], data_holes[7],0, 0])
hole_3 = np.array([0, 0, 0, data_holes[5], 0, 0, 0])

holes = np.array([0, data_holes[0], data_holes[1]+data_holes[2], data_holes[3]+data_holes[4]+data_holes[5],
     data_holes[6]+data_holes[7], data_holes[8], 0])

#total number of holes
sum_hole_1= sum(hole_1)
sum_hole_2= sum(hole_2)
sum_hole_3= sum(hole_3)


####################################################################### plotting
plt.figure(figsize=(14, 10))
plt.yscale("log")
plt.grid(which="both", axis="both")
plt.errorbar(plane, data, xerr=0.5, fmt='k', elinewidth=1.5, lw=0, capsize=3, capthick=1.5)
plt.xlabel("Number of traversed planes", fontsize=18)
plt.ylabel("Number of events", fontsize=18)
plt.title("Number of measured measured multi-plane-events", fontsize=24)
plt.tick_params(axis='both', labelsize=18)
#plt.legend(fontsize=18)
#plt.savefig("/home/david/Desktop/Bachelor_images/6_1/rate_comparison.png", dpi=300)
plt.show()


# plotting HOLES
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(18, 8))
ax1.set_yscale("log")
ax1.grid(which="both", axis="both")
ax1.errorbar(plane, data,xerr=0.5, fmt='k',elinewidth=1.5, lw=0, capsize=3, capthick=1.5, label= "Measured number of n-p-e")
ax1.errorbar(plane, holes,xerr=0.5, fmt='b', elinewidth=1.5, lw=0, capsize=3, capthick=1.5, label= "Number of events with gaps")

ax1.set_xlabel("number of traversed planes", fontsize=18)
ax1.set_ylabel("mean rate $[1/s]$", fontsize=18)
ax1.tick_params(axis='both', labelsize=18)
#ax1.set_title("Mean rate of measured multi-plane-events, considering holes")
ax1.legend()#(fontsize=16)

ax2.errorbar(plane, holes/(data+0.00000000001), xerr=0.5,fmt='k',
             elinewidth=1.5, lw=0, capsize=3, capthick=1.5)
ax2.grid(which="both", axis="both")
ax2.set_xlabel("number of traversed planes", fontsize=18)
ax2.set_ylabel("Ratio of events with gaps to all measured events", fontsize=18)
ax2.tick_params(axis='both', labelsize=18)
#ax2.set_title("Ratio of events with gaps to total rate of n-plane-events")
#plt.savefig("/home/david/Desktop/Bachelor_images/6_1/holes.png", dpi=300)
plt.show()


# plotting MORE ON HOLES
plt.figure(figsize=(14, 10))
plt.grid(which="both", axis="both")
plt.errorbar(plane[1:6], holes[1:6], xerr=0.5,fmt='k', elinewidth=1.5, lw=0, capsize=6, capthick=1.5, label= "Total number of holes")
plt.errorbar(plane[1:6], hole_1[1:6],xerr=0.5,fmt='r',elinewidth=1.5, lw=0, capsize=3, capthick=1.5, label= "number of 1 hole events")
plt.errorbar(plane[1:6], hole_2[1:6],xerr=0.5, fmt='b',elinewidth=1.5, lw=0, capsize=3, capthick=1.5, label= "number of 2 hole events")
plt.errorbar(plane[1:6],hole_3[1:6], xerr=0.5,fmt='green',elinewidth=1.5,lw=0,capsize=3, capthick=1.5, label= "number of 3 hole events")

plt.xlabel("number of traversed planes")
plt.ylabel("Number of holes")
# plt.title("Mean rate of holes")
plt.legend()
plt.show()


# plotting_TOTAL_HITS


plt.figure(figsize=(14, 10))
plt.grid(which="both", axis="both")
plt.errorbar(plane-1, data_hits, xerr=0.5, fmt='k',
             elinewidth=1.5, lw=0, capsize=3, capthick=1.5)
plt.xlabel("Plane", fontsize=18)
#plt.ylabel("Mean rate $[1/s]$", fontsize=18)
plt.ylabel("Counts", fontsize = 18)
plt.tick_params(axis='both', labelsize=18)
plt.title("Number of hits per plane", fontsize=24)
# plt.legend()
plt.show()