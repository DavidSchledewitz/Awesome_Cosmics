#!/usr/bin/env python
# coding: utf-8

# # Python data analysis script
# This script takes `.json` files exported from the `[JSONWriter]` module of Corryvreckan, and is aimed towards analyzing and plotting the hit data.

# In[1]:


import json
import os
import numpy as np
from tqdm import tqdm


# ## Importing data into python
# ### Reading in .json file

# In[2]:


file = 'data/example.json'

with open(file) as json_file:
    data = json.load(json_file)


# The JSON file is structured as follows:
# 
# ![image.png](attachment:image.png)
# 
# The information of a single pixel hit is stored inside of an object, and these objects are bundled into events.

# ### Writing all relevant data into one object
# The goal of this section is to create a python object that contains all necessary data of all events. It should be able to be appended further down the line. The easiest way to do this is to use python lists and dictonaries.

# In[3]:


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


# For example, we can look at the 614th event like this:

# In[4]:


hit_data[613]


# ### Masking
# Some pixels on some planes have a high tendency to fire randomly. In this step, the goal is to find these pixels, and exclude them from our analysis.

# In[5]:


#Create a matrix for each plane
pixels = np.zeros((7,1024,512),int)

#Loop over all events
for event in range(len(hit_data)):
    
    #Loop over all planes
    for plane in range(7):
        
        #Check, how many hits the event contains
        nhits = len(hit_data[event][plane]['X'])
        
        #Write them into the corresponding matrix
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
                if (pixels[plane][x][y] > 100*mean_hits):
                    masked_pixels[plane].append((x,y))

print("Masked pixels:\n{}".format(masked_pixels))


# Now we see, that also our 614th event is affected by a hot pixel on `plane_1`. To fix this, we clean up the `hit_data` object:

# In[7]:


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


# In[8]:


hit_data[613]


# ### Adding some helpful information

# For later analysis, it can come in handy, to seperate the events into different categories, based on the number of planes that have been hit. So we'll quickly add an entry for that.

# In[9]:


for event in range(len(hit_data)):
    
    total_planes = 7 #Set the total number of planes
    
    for plane in range(total_planes):
        if not hit_data[event][plane]["X"]:        #for each empty event
            hit_data[event][plane]["X"].append(-1) #write a -1 into the hit array
            hit_data[event][plane]["Y"].append(-1) #---"---
            total_planes-=1                        #and substract one from the total number of planes
            
    #Add an entry into the dictionary
    hit_data[event]["number_of_planes"] = total_planes
    


# Now, our object will look like this:

# In[10]:


hit_data[613]


# This way, we can add all sort of stuff into the dictionary as we go on, from tracking information, all the way to residuals and goodness-of-fit information.

# ## Calculating hit positions

# For now, our data consisted of individual pixel hits. In the next step, we want to combine these hits into a cluster, to determine the
# hit position more accurately. For that we will make some distinctions:
# - **Only one pixel fired** In this case, we write only the given coordinate
# - **Two pixels fired** In this case we take the mean between the two given coordinates
# - **More than two pixels fired** This case is a little bit more complicated. We will define what's called a __search window__ around each pixel hit. If other pixels are included in the search window, the pixel will be marked as `True`, if not, it will be marked as `False`. This way, we will filter out single pixel hits that occur randomly on the plane (which happens A LOT (53% of all cases))

# In[11]:


bad_counter = 0
good_counter = 0
#Add a cool status bar
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
                good_counter-=1
            if sdev >= 10: bad_counter+=1
            else: good_counter+=1
        
            #Add an entry to the dictionary
            hit_data[event][plane]["XC"] = Cluster_X
            hit_data[event][plane]["YC"] = Cluster_Y
            hit_data[event][plane]["sdev"] = sdev
                
        pbar.update(1)
                


# In[12]:


bad_counter/good_counter


# Now, our object will contain a lot of new, helpful stuff!

# In[13]:


hit_data[613]


# ## Taking a first look at the data

# We will be using the `mplot3d` toolkit from `matplotlib` to visualize the data. First we import it:

# In[14]:


import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import proj3d


# Next we choose what data to plot, and how we want it to look like

# In[15]:


#Define pixel pitches
#ppx, ppy, ppz = 0.02924, 0.02688, 20 #Pixel pitches in x and y [mm]
ppx, ppy, ppz = 0.02924, 0.02688, 20


# In[16]:


plot = 1                    #Plot the first 3 events
connect_hits = True         #Connects the hits
min_nop = 6                 #Plot only events that include 7 planes

#Dimensions of the detector
xlim = 1023*ppx
ylim = 511*ppy
zlim = 6*ppz

#Create a figure object
fig = plt.figure(figsize=(5,5))
ax = plt.axes(projection='3d')    #Create 3d Axes
ax._axis3don = False              #... but invisible
#ax.set_box_aspect((3,3,3))       #Define aspect ratio
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
        
    plot_counter+=1
    if plot_counter == plot: break
    


# ## Tracking
# 

# In the next step, we'll investigate a way to approximate the data with 
# tracks. Describing the data with tracks is a very useful concept that will later help us align the detector planes.
# 
# The first step is to approximate each event with a track. A track is a mathematical object, and is not limited to the pixel matrix. It has a much higher accuracy than the hits themselves.
# 
# Secondly, we want to assign a value to each track, describing the goodness-of-fit to the track. This will be done with a residual (chi squared) analysis.

# In[21]:


with tqdm(total=len(hit_data)) as pbar:
    
    #Loop over all events
    for event in range(len(hit_data)):
    
        #Number of planes belonging to the track
        nop = hit_data[event]["number_of_planes"]
    
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
            Fit_Data[counter][2] = plane*ppz
            std_hit[counter] = hit_data[event][plane]["sdev"]  
            #std_hit[counter] = np.sqrt((ppx**2+ppy**2)/2)*hit_data[event][plane]["sdev"]
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
            
            # Solve for the point in plane of Track z = a+mb
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
        
        pbar.update(1)


# In[22]:


hit_data[613]


# Now, our object contains also Track data, which we can plot in the next step

# In[23]:


plot = 3                    #Plot the first X events
connect_hits = True         #Connects the hits
plot_tracks = True         #Plot tracks associated to events
min_nop = 6                 #Plot only events that include 7 planes

#Create a figure object
fig = plt.figure(figsize=(5,5))
ax = plt.axes(projection='3d')  #Create 3d Axes
ax._axis3don = False            #... but invisible
#ax.set_box_aspect((3,3,3))     #Define aspect ratio
ax.set_xlim3d(0,xlim)           #Axis limits in x
ax.set_ylim3d(0,ylim)           #Axis limits in y
ax.set_zlim3d(0,zlim)     
x = np.arange(0,1025*ppx,512*ppx) #Again convert pixel into mm
y = np.arange(0,1024*ppy,512*ppy)
X, Y = np.meshgrid(x,y)
Z = np.ndarray((len(y),len(x)))
Z.fill(0)

#Draw the planes
for plane in range(7):
    Z.fill(plane*ppz)
    ax.plot_surface(X,Y,Z,alpha=.1,color='black')

plot_counter = 0

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
    if plot_counter == plot: break

plt.show()

# In[24]:


hit_data[613]


# In[ ]:





# In[ ]:





# In[ ]:




