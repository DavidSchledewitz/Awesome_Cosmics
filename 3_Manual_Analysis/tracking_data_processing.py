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
from scipy.optimize import curve_fit

# we want to import the data

from example_data import hit_data

#data_path = os.path.join(os.path.split(os.path.split(os.path.dirname(__file__))[0])[0], "data","compressed") ../../data/compressed


#######################---data structure   data structure   data structure---#############################

#hit_data[event_number][plane#, "tp1","tp2","number_of_planes","chi2","chi2red"][für plane number:"X","Y","XC","YC","sdev","resx","resy"]
#zu chi2: chi2red = chi2/numberofplanes*3coords-4


#######################---MAIN_CODE   MAIN_CODE   MAIN_CODE   MAIN_CODE---#############################

##container to store plot information
Phi =  np.array([])
Chi2red =  np.array([])
Phi4,Phi5,Phi6,Phi7 = np.array([]),np.array([]),np.array([]),np.array([])

chi2red = 10 ###############   choose chi2red cut for the data visualisation


# select an event(run over all events)
for event in range(len(hit_data)):

    #check that the vent has at least 4 involved planes
    if hit_data[event]["number_of_planes"] >= 4:

        #check, if chi2red < 10, to justify that the fit of the track in this event is good
        if hit_data[event]["chi2"]/(hit_data[event]["number_of_planes"]*3-4) <= chi2red:

            #save chi2red for good tracks in list
            Chi2red = np.append(Chi2red,hit_data[event]["chi2"]/(hit_data[event]["number_of_planes"]*3-4))

            #extract the distances out of the two track point (tp1 and tp2) given
            d_x = hit_data[event]["tp2"][0]-hit_data[event]["tp1"][0]
            d_y = hit_data[event]["tp2"][1]-hit_data[event]["tp1"][1]
            d_z = hit_data[event]["tp2"][2]-hit_data[event]["tp1"][2]
            d_t = np.sqrt(d_x**2 + d_y**2)

            #calculate angle of the track
            phi = np.arctan(d_t/d_z)*360/(2*np.pi)
            Phi = np.append(Phi,phi)

            # look at the angles for events with different numbers of involved planes
            if hit_data[event]["number_of_planes"]==4:
                Phi4 = np.append(Phi4,phi)
            if hit_data[event]["number_of_planes"]==5:
                Phi5 = np.append(Phi5,phi)
            if hit_data[event]["number_of_planes"]==6:
                Phi6 = np.append(Phi6,phi)
            if hit_data[event]["number_of_planes"]==7:
                Phi7 = np.append(Phi7,phi)


#######################---PLOTS   PLOTS   PLOTS   PLOTS---#############################

plt.hist(Phi,bins= 14 ,range=(0,28), color= "darkblue")#, label="Selected tracks, $\chi^2_{red} \leqslant$ "+str(chi2red))
plt.title("Angular distribution of 4 or more plane events with $\chi^2_{red} \leqslant$ "+str(chi2red))
plt.xlabel("Zenith angle [°]")
plt.ylabel("Counts")
plt.legend()
#plt.savefig("/home/david/Desktop/Bachelor_images/6_2/angular_ALL_chi100_4_and_more.png", dpi=300)
plt.show()

plt.figure(figsize=(8, 8))
plt.hist(Chi2red, bins=20, color="darkblue")#, label="Selected tracks, $\chi^2_{red}$ in range "+str(chi11)+" to "+str(chi12))+" and "+str(chi21)+" to "+str(chi22)
#plt.hist(Chi,range=(0,100), bins=50, label="Selected tracks, $\phi$ in range "+str(phi111)+" to "+str(phi142))
plt.title("$\chi^2_{red}$-distribution of 4 and more plane events with cut at $\chi^2_{red} =$ "+str(chi2red), fontsize = 24)# in range "+str(chi11)+" to "+str(chi12))
plt.xlabel("$\chi^2_{red}$", fontsize = 18)
plt.ylabel("Counts", fontsize = 18)
plt.tick_params(axis='both', labelsize=18)
#plt.legend()
#plt.savefig("/home/david/Desktop/Bachelor_images/6_2/chi_distr_cut_100_7pe.png", dpi=300)
plt.show()

plt.figure(figsize=(12, 10))
plt.hist(([Phi7,Phi6,Phi5,Phi4]), bins= 14 ,range=(0,28),label=("7 planes","6 or more planes","5 or more planes","4 or more planes" ), color= ("darkred","darkgreen","darkorange","darkblue")
, histtype="barstacked")#, weights=(np.ones(len(Phi7)),np.ones(len(Phi6))/2,np.ones(len(Phi5))/3,np.ones(len(Phi4))/4))
plt.title("Angular distribution of n-plane-eventswith, $\chi^2_{red}\leq$"+str(chi2red), fontsize = 24)#, $\chi^2_{red}$ in range "+str(chi11)+" to "+str(chi12), fontsize = 24)
plt.xlabel("Zenith angle [°]", fontsize = 18)
plt.ylabel("Counts", fontsize = 18)
plt.tick_params(axis='both', labelsize=18)
plt.legend(fontsize = 18)
#plt.savefig("/home/david/Desktop/Bachelor_images/6_2/angular_chi100_4_5_6_7.png", dpi=300)
plt.show()      