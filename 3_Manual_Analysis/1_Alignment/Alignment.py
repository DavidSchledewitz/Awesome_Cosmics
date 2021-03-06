#!/usr/bin/python3

# For debugging
graphic_output = False
verbose = False

# Minimum number of planes to use for analysis
min_nop = 4
#Define pixel pitches
ppx, ppy, ppz = 0.02924, 0.02688, 20

import json
import os
import numpy as np
from tqdm import tqdm
import sys

# Importing data into python {{{
try: inp = sys.argv[1]
except IndexError:
    print('Please specify a JSON file. Exiting...')
    exit()
else:
    print('Loading File...')
    file = sys.argv[1]

with open(file) as json_file:
    data = json.load(json_file)
# }}}

# Convert into python object {{{
print('Initializing...')
hit_data = []    #initialize the list of all events
event_no = 0     #use a counter that will be incremented on each step

#Start the event loop
for event in data:
    
    #Skip over empty events
    if len(event) == 0: continue
        
    #Create a python dictionary for each event.
    hit_data.append({})
    
    #Create an entry in the dictionary for each plane
    for plane in range(7):
        hit_data[event_no][plane] = {}      #Stores all plane data
        hit_data[event_no][plane]["X"] = [] #Stores x-coordinates of hits
        hit_data[event_no][plane]["Y"] = [] #Stores y-coordinates of hits
    
    #Read out pixel by pixel
    for obj in event:
        
        #First, find out which plane the hit belongs to
        plane = int(obj["m_detectorID"].split("_")[1])
        #Second, read out x (column) and y (row) data
        hit_data[event_no][plane]["X"].append(int(obj["m_column"]))
        hit_data[event_no][plane]["Y"].append(int(obj["m_row"]))
        
    #Increment counter
    event_no+=1
# }}}

# Masking {{{
print('Creating Mask...')

#Create a matrix for each plane
pixels = np.zeros((7,1024,512),int)

#Loop over all events
for event in range(len(hit_data)):
    
    #Loop over all planes
    for plane in range(7):
        
        #Check, how many hits the event contains
        nhits = len(hit_data[event][plane]['X'])
        
        #Increment the corresponding matrix element
        for hit in range(nhits):
            x = hit_data[event][plane]['X'][hit]
            y = hit_data[event][plane]['Y'][hit]
            pixels[plane][x][y]+=1

# Check for the mean hit rate of all pixels
frequency = []
for plane in range(7):
    for x in range(1024):
        for y in range(512):
            frequency.append(pixels[plane][x][y])
            
mean_hits = np.mean(frequency)

print('Pixels fired on average {} times'.format(
    np.round(mean_hits,2)))

#Then, mask all pixels that fire 100x more frequent
mask_limit = int(np.round(100*mean_hits))

print('Masking all pixels that fired more than {} times'.format(
    mask_limit))

#We will store them in a list for quick reference
masked_pixels = []

with tqdm(total=7*1024*512) as pbar:
    for plane in range(7):
        masked_pixels.append([])
        for x in range(1024):
            for y in range(512):
                pbar.update()
                if (pixels[plane][x][y] > mask_limit):
                    masked_pixels[plane].append((x,y))

if verbose: print("Masked pixels:\n{}".format(masked_pixels))

#Save number of events before masking for later ;)
before_masking = len(hit_data)

for event in range(len(hit_data)):
    
    for plane in range(7):
        nhits = len(hit_data[event][plane]['X'])
        counter = 0
        for hit in range(nhits):
            x = hit_data[event][plane]['X'][counter]
            y = hit_data[event][plane]['Y'][counter]
            if (x,y) in masked_pixels[plane]:
                hit_data[event][plane]['X'].remove(x)
                hit_data[event][plane]['Y'].remove(y)
                counter-=1 #If an event is removed, check the next event that takes its place
            counter+=1
            
#Finally remove all empty events (reverse to avoid confusion)
for event in reversed(range(len(hit_data))):
    
    #First, assume the event is empty
    empty = True
    
    #Check all planes
    for plane in range(7):
        
        #If there is a hit, mark as non-empty
        if hit_data[event][plane]['X']:
            empty = False
            break
    
    #Then delete the event
    if empty: del hit_data[event]
        
after_masking = len(hit_data)

print('Reduced {} events to {} events after masking'.format(before_masking,after_masking))
# }}}

# Adding some helpful information {{{
for event in range(len(hit_data)):
    
    total_planes = 7 #Set the total number of planes
    
    for plane in range(total_planes):
        if not hit_data[event][plane]["X"]:        #for each empty event
            hit_data[event][plane]["X"].append(-1) #write a -1 into the hit array
            hit_data[event][plane]["Y"].append(-1) #---"---
            total_planes-=1                        #and substract one from the total number of planes
           
    #Add an entry into the dictionary
    hit_data[event]["number_of_planes"] = total_planes

#Function for counting n-plane events
def count(nop):
    counter = 0
    for i in range(len(hit_data)):
        if (hit_data[i]['number_of_planes'] == int(nop)): counter+=1
    print('{} {}-plane events found.'.format(counter,nop))
    return counter
count(7)
# }}}

# Calculating hit positions {{{
print('Calculating hit positions...')

with tqdm(total=len(hit_data)) as pbar:

    for event in range(len(hit_data)):
    
        for plane in range(7):
        
            if (hit_data[event][plane]["X"][0] == -1):
                hit_data[event][plane]["XC"] = -1.0
                continue
                
            #Calculate the cluster position in X and Y (mean)
            Cluster_X = np.round(np.mean(hit_data[event][plane]["X"]),2)
            Cluster_Y = np.round(np.mean(hit_data[event][plane]["Y"]),2)
        
            #Calculate the standard deviation (the cluster spread)
            sdev = np.round(
                np.sqrt(
                    np.std(hit_data[event][plane]["X"])**2+
                    np.std(hit_data[event][plane]["Y"])**2),2)
        
            #If the cluster consists of one pixel alone, the uncertainty is defined by the binary resolution
            if sdev == 0:
                sdev = np.round(1/np.sqrt(12),2)
        
            #Add an entry to the dictionary
            hit_data[event][plane]["XC"] = Cluster_X
            hit_data[event][plane]["YC"] = Cluster_Y
            hit_data[event][plane]["sdev"] = sdev
                
        pbar.update(1)
# }}}


# Plot Function for debugging purposes {{{

connect_hits = True         #Connects the hits
plot_tracks = False         #Plots Tracks (for later)

def plot(n,connect_hits,plot_tracks,min_nop):

    import matplotlib.pyplot as plt
    from mpl_toolkits import mplot3d
    from mpl_toolkits.mplot3d import proj3d

    #Dimensions of the detector
    xlim = 1023*ppx
    ylim = 511*ppy
    zlim = 6*ppz

    #Create a figure object
    fig = plt.figure(figsize=(5,5))
    ax = plt.axes(projection='3d')    #Create 3d Axes
    ax._axis3don = False              #... but invisible
    ax.set_box_aspect((3,3,3))        #Define aspect ratio
    ax.set_xlim3d(0,xlim)             #Axis limits in x
    ax.set_ylim3d(0,ylim)             #Axis limits in y
    ax.set_zlim3d(0,zlim)             #Axis limits in z
    x = np.arange(0,1025*ppx,512*ppx) #Create a meshgrid for plane-plotting
    y = np.arange(0,1024*ppy,512*ppy)
    X, Y = np.meshgrid(x,y)
    Z = np.ndarray((len(y),len(x)))
    Z.fill(0)

    #Draw the planes
    for plane in range(7):
        Z.fill(plane*ppz)
        ax.plot_surface(X,Y,Z,alpha=.1,color='black')

    plot_counter = 0 #We count the plots because we only want SOME
    #Plot the hits
    for event in range(len(hit_data)):

        #Plot only events with the minimum amount of planes specified
        if (hit_data[event]['number_of_planes'] < min_nop): continue
        print('Plotting event {}'.format(event))

        x_data, y_data, z_data = [], [], []

        for plane in range(7):

            #Skip over empty hits
            if (hit_data[event][plane]["XC"] == -1): continue

            #Put everything else into plottable arrays
            x_data.append(ppx*hit_data[event][plane]["XC"])
            y_data.append(ppy*hit_data[event][plane]["YC"])
            z_data.append(plane*ppz)

            ax.scatter3D(x_data,y_data,z_data,alpha=.7,color='black',marker='.')

            # OPTIONAL: Connect dots for Better visibility of Tracks
            if connect_hits:
                ax.plot(x_data,y_data,z_data, linewidth=.5)#, color='grey')
                
            # OPTIONAL: Plot tracks associated to events
            if plot_tracks:
                x_track = [hit_data[event]['Track_Point_1'][0],hit_data[event]['Track_Point_2'][0]]
                y_track = [hit_data[event]['Track_Point_1'][1],hit_data[event]['Track_Point_2'][1]]
                z_track = [hit_data[event]['Track_Point_1'][2],hit_data[event]['Track_Point_2'][2]]
                ax.plot(x_track,y_track,z_track,linewidth=.5)

        plot_counter+=1
        if plot_counter == n: break
    plt.show()


# }}}

if graphic_output: plot(3,connect_hits,plot_tracks,6)


# Tracking {{{
print('Tracking...')

    
#Loop over all events
for event in range(len(hit_data)):

    #Number of planes belonging to the track
    nop = hit_data[event]["number_of_planes"]
    if nop < min_nop: continue

    #Create some arrays to calculate in (convert px to mm)
    Fit_Data = np.ndarray((nop,3))
    std_hit = np.ndarray((nop))
    planes_used = [] #This is to exclude empty planes later

    #Create a counter for the Fit Array
    counter = 0

    #Loop over all planes
    for plane in range(7):

        #Skip empty planes
        if (hit_data[event][plane]["XC"] == -1): continue

        #Note which planes are non-empty
        planes_used.append(plane)

        #Convert pixel lengths into mm
        Fit_Data[counter][0] = ppx*hit_data[event][plane]["XC"]
        Fit_Data[counter][1] = ppy*hit_data[event][plane]["YC"]
        Fit_Data[counter][2] = ppz*plane  
        std_hit[counter] = np.sqrt((ppx**2+ppy**2)/2)*hit_data[event][plane]["sdev"]
        counter+=1

    # Fitting Algorithm (Based on np.linalg.svd)
    datamean = Fit_Data.mean(axis=0)
    uu, dd, vv = np.linalg.svd(Fit_Data - datamean)
    linepts = vv[0] * np.mgrid[-100:100:2j][:,np.newaxis]
    linepts += datamean

    # Two Points Define the Fitted Track
    x1 = linepts[0]
    x2 = linepts[1]

    # Take the residual
    d = []
    for plane in planes_used:
        x0 = np.array([
            hit_data[event][plane]["XC"]*ppx,
            hit_data[event][plane]["YC"]*ppy,
            plane*ppz])

        # Solve for the point in plane of Track (simply z = a+mb)
        lbda = (x0[2] - x2[2])/(x2-x1)[2] # m = (z-a)/(b)
        xz = x2+lbda*(x2-x1) # find point in axis that lies in the same plane
        hit_data[event][plane]["resx"] = (x0-xz)[0]
        hit_data[event][plane]["resy"] = (x0-xz)[1]
        d.append(np.linalg.norm(xz-x0))

    #Add an entry into the dictionary containing the track coordinates
    hit_data[event]["Track_Point_1"], hit_data[event]["Track_Point_2"] = [],[]
    for i in range(3):
        hit_data[event]["Track_Point_1"].append(x1[i])
        hit_data[event]["Track_Point_2"].append(x2[i])

    # From there, calculate chi2 to determine the goodness of the fit
    chi2 = 0
    for entry in range(len(d)):
        chi2 += d[entry]**2/std_hit[entry]**2

    hit_data[event]["chi2"] = chi2
    #Also add an entry for reduced chi2
    hit_data[event]["chi2red"] = chi2/(nop*3-4)
# }}}

if graphic_output: plot(3,True,True,7)

# Quality of fits {{{
def plotchi2(chi2_cut,number_of_bins):
    plt.style.use('bmh')
    chi2_7 = []
    chi2_6 = []
    chi2_5 = []
    chi2_4 = []
    for i in range(len(hit_data)):
        if hit_data[i]['number_of_planes'] < 4: continue
        if hit_data[i]['chi2red'] >= chi2_cut: continue
        if (hit_data[i]['number_of_planes'] == 7):
            chi2_7.append(hit_data[i]['chi2red'])
            chi2_6.append(hit_data[i]['chi2red'])
            chi2_5.append(hit_data[i]['chi2red'])
            chi2_4.append(hit_data[i]['chi2red'])
        elif (hit_data[i]['number_of_planes'] == 6):
            chi2_6.append(hit_data[i]['chi2red'])
            chi2_5.append(hit_data[i]['chi2red'])
            chi2_4.append(hit_data[i]['chi2red'])
        elif (hit_data[i]['number_of_planes'] == 5):
            chi2_5.append(hit_data[i]['chi2red'])
            chi2_4.append(hit_data[i]['chi2red'])
        elif (hit_data[i]['number_of_planes'] == 4):
            chi2_4.append(hit_data[i]['chi2red'])

    plt.hist(chi2_4,number_of_bins,color='#061822',label='4 Planes')
    plt.hist(chi2_5,number_of_bins,color='#063268',label='5 Planes')
    plt.hist(chi2_6,number_of_bins,color='#3647a0',label='6 Planes')
    plt.hist(chi2_7,number_of_bins,color='#5668c7',label='7 Planes')
    plt.xlabel(r'$\chi^2/\nu$')
    plt.ylabel('# entries')
    plt.legend()
    plt.plot()
# }}}
    
if graphic_output: plotchi2(6000,np.arange(0,6000,150))

# Alignment {{{
planes_used = [0,6]   #Planes fixed for alignment
alignments = 50       #Number of alignment steps (~50 recommended)
fine_alignments = 10  #Number of fine alignment steps (~10 recommended)
plot_each_step = False#Debugging
chi2_cut = np.logspace(5.3,1,alignments-fine_alignments)
min_chi2_reached = False

N = len(hit_data) # Number of events (hardcoded for now)
cnt = 0

# Initialize list for plotting alignment progress
posx, posy, dposx, dposy = [], [], [], []
for i in range(7):
    posx.append([])
    posy.append([])
    dposx.append([])
    dposy.append([])
    posx[i].append(0)
    posy[i].append(0)
    dposx[i].append(0)
    dposy[i].append(0)

print('Starting Alignment procedure...')

for a in range(alignments):
    
    if min_chi2_reached:
        print('Iteration step {}/{} (fine alignment)'.format(a+1,alignments),end="\r")
    else:
        print('Iteration step {}/{}'.format(a+1,alignments),end="\r")

    # Count how many tracks are used for alignment after chi2cut
    cnt_track = 0

    # Show chi2 distro (debugging)
    chi2_array = []

    for track in range(N):

        # Number of planes belonging to the track
        nop = hit_data[track]["number_of_planes"]
        if nop < min_nop: continue

        # Fix Offset of planes_used to be 0
        plane1, plane2 = planes_used[0], planes_used[1]
        posx[plane1][a], posy[plane1][a] = 0, 0
        posx[plane2][a], posy[plane2][a] = 0, 0

        # Apply alignment for the planes
        for plane in range(7):
            if (hit_data[track][plane]["XC"] == -1): continue
            hit_data[track][plane]["XC"]-=posx[plane][a]/ppx #TAKE CARE! convert back to pixels
            hit_data[track][plane]["YC"]-=posy[plane][a]/ppy # --- "" ---
        
        # Convert pixel into mm
        Fit_Data = np.zeros((nop,3))
        tracked_planes = []
        count_planes = 0
        for plane in range(7):
            if (hit_data[track][plane]["XC"] == -1): continue
            tracked_planes.append(plane)
            Fit_Data[count_planes][0] = ppx*hit_data[track][plane]["XC"]
            Fit_Data[count_planes][1] = ppy*hit_data[track][plane]["YC"]
            Fit_Data[count_planes][2] = ppz*plane
            count_planes+=1
        
        # Fitting Algorithm
        datamean = Fit_Data.mean(axis=0)
        uu, dd, vv = np.linalg.svd(Fit_Data - datamean)
        linepts = vv[0] * np.mgrid[-100:100:2j][:,np.newaxis]
        linepts += datamean

        # Two Points Define the Fitted Track
        x1 = linepts[0]
        x2 = linepts[1]

        # Calculate the residuals for all planes
        d = []
        std_hit = []
        for plane in tracked_planes:
            x0 = np.array([
                ppx*hit_data[track][plane]["XC"],
                ppy*hit_data[track][plane]["YC"],
                ppz*plane])
            # Solve for the point in plane of Track z = a+mb
            lbda = (x0[2] - x2[2])/(x2-x1)[2] # m = (z-a)/(b)
            xz = x2+lbda*(x2-x1) # find point in axis that lies in the same plane
            hit_data[track][plane]["resx"] = (x0-xz)[0]
            hit_data[track][plane]["resy"] = (x0-xz)[1]
            std_hit.append(np.sqrt((ppx**2+ppy**2)/2)*hit_data[track][plane]["sdev"])
            d.append(np.linalg.norm(xz-x0))

        #Add an entry into the dictionary containing the track coordinates
        hit_data[track]["Track_Point_1"], hit_data[track]["Track_Point_2"] = [],[]
        for i in range(3):
            hit_data[track]["Track_Point_1"].append(x1[i])
            hit_data[track]["Track_Point_2"].append(x2[i])

        # From there, calculate chi2 to determine the goodness of the fit
        chi2 = 0
        for entry in range(len(d)):
            chi2 += d[entry]**2/std_hit[entry]**2
        hit_data[track]["chi2"] = chi2
        hit_data[track]["chi2red"] = chi2/(nop*3-4)

        # Plot distro (DEBUG??)
        if chi2/(nop*3-4) <= chi2_cut[cnt]:
            chi2_array.append(chi2)

    # Create Dictionary for Residuals
    Res = {}
    for plane in range(7):
        Res[plane] = {}
        Res[plane]['x'] = []
        Res[plane]['y'] = []

    # Fill Residual Dictionary
    for track in range(N):
        nop = hit_data[track]["number_of_planes"]
        if nop < min_nop: continue
        if (hit_data[track]['chi2red'] >= chi2_cut[cnt]): continue
        cnt_track+=1

        # After minimum chi2red is reached
        if min_chi2_reached:
            for plane in range(7):
                if (hit_data[track][plane]['XC'] == -1): continue
                if (abs(hit_data[track][plane]['resx']) <= 10*ppx): # To avoid faraway residuals
                    Res[plane]['x'].append(hit_data[track][plane]['resx'])
                if (abs(hit_data[track][plane]['resy']) <= 10*ppy):
                    Res[plane]['y'].append(hit_data[track][plane]['resy'])

        # Before min chi2 is reached
        else:
            for plane in range(7):
                if (hit_data[track][plane]['XC'] == -1): continue
                Res[plane]['x'].append(hit_data[track][plane]['resx'])
                Res[plane]['y'].append(hit_data[track][plane]['resy'])

    if plot_each_step:
        plt.hist(chi2_array,40)
        plt.show()

    # Calculate mean of residual
    OffsetX, OffsetY, dOffsetX, dOffsetY = [], [], [], []
    for plane in range(7):
        if plane in planes_used:
            OffsetX.append(0)
            OffsetY.append(0)
            dOffsetX.append(np.std(Res[plane]['x']))
            dOffsetY.append(np.std(Res[plane]['y']))
            continue
        OffsetX.append(np.mean(Res[plane]['x']))
        OffsetY.append(np.mean(Res[plane]['y']))
        dOffsetX.append(np.std(Res[plane]['x']))
        dOffsetY.append(np.std(Res[plane]['y']))
        
    if verbose:
        print('{} Tracks survived the chi2 cut of {}'.format(cnt_track,chi2_cut[cnt]))
        if cnt_track <= 200: print('WARNING!!! CHI2 CUT MIGHT BE TOO STRONG')
        
    # Append changes to position array
    for plane in range(7):
        if verbose: print("Offset plane {}: x = {} y = {}".format(
                plane,np.round(OffsetX[plane],4),np.round(OffsetY[plane],4)))
        posx[plane].append(OffsetX[plane])
        posy[plane].append(OffsetY[plane])
        dposx[plane].append(dOffsetX[plane])
        dposy[plane].append(dOffsetY[plane])

    # increment counter for chi2 cut
    if (cnt < len(chi2_cut)-1):
        cnt+=1
    else: min_chi2_reached = True

# So far, only the offsets have been written to posx... need to append instead...
for a in range(alignments):
    for plane in range(7):
        posx[plane][a+1]+=posx[plane][a]
        posy[plane][a+1]+=posy[plane][a]

if verbose:
    for plane in range(7):
        print('Plane {} X: {} +- {}'.format(
            plane,np.round(posx[plane][alignments],2),np.round(dposx[plane][alignments],2)))
        print('Plane {} Y: {} +- {}'.format(
            plane,np.round(posy[plane][alignments],2),np.round(dposy[plane][alignments],2)))
print('Finished! Writing to file...')
# }}}

# Plot section {{{
if graphic_output:
    print('Plotting...')
    markers=['o','^','x','s','p','h','D']
    col=['#fbcf36','#ed4c1c','#9c7e70','#5ac2f1','#11776c','#e0363a','#6a1c10']
    xaxis = np.arange(alignments+1)
    plt.figure(figsize=(10,5))
    plt.xlabel('Alignment iterations')
    plt.ylabel('Plane position in X [??m]')
    #plt.ylim(-1000,400)
    for plane in range(7):
        if plane in planes_used: continue
        plt.errorbar(xaxis,posx[plane],yerr=dposx[plane], label='Plane {}'.format(plane+1),
                linewidth=1,marker=markers[plane],color='black',capsize=3,mfc=col[plane])
    plt.legend()
    plt.tight_layout()

    plt.figure(figsize=(10,5))
    plt.xlabel('Alignment iterations')
    plt.ylabel('Plane position in Y [??m]')
    #plt.ylim(-1200,600)
    for plane in range(7):
        if plane in planes_used: continue
        plt.errorbar(xaxis,posy[plane],yerr=dposy[plane], label='Plane {}'.format(plane+1),
                linewidth=1,marker=markers[plane],color='black',capsize=3,mfc=col[plane])
    plt.legend()
    plt.tight_layout()
    plt.show()
# }}}

if graphic_output: plotchi2(10,np.arange(0,10,.25))

if graphic_output: plot(5,True,True,6)

# Write to file for further anaylsis
fx = open("hit_data_{}.py".format(sys.argv[1].split(".")[-2].split("/")[-1]),"w")
fx.write("hit_data = "+str(hit_data))
fx.close
