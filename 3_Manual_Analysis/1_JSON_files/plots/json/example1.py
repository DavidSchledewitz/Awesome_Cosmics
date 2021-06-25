#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
from matplotlib.patches import Rectangle

#This example imports 10 pixels from the file and plots the data without using the library.
path = os.path.join(os.path.split(os.path.dirname(__file__))[0],"json","data")
#path='./data'
file='GblTracks.json'
#get data from the file
with open('%s/%s'%(path,file)) as json_file:
    data = json.load(json_file);

#extract 10 objects of type 'corryvreckan::Pixel'
jsonPixels=[];
for event in data:
    for obj in event:
        if obj['_typename']=='corryvreckan::Pixel' :
            jsonPixels.append(obj);
        if len(jsonPixels)>=10 :###############################################################10 pixel cut
            break;
    if len(jsonPixels)>=10 :######################################################################see above
        break;

#define detector IDs and colormap for plotting
detectorIDs=['pALPIDEfs_0','pALPIDEfs_1','pALPIDEfs_2','pALPIDEfs_3',       'pALPIDEfs_4','pALPIDEfs_5','pALPIDEfs_6'];
cmap=plt.cm.get_cmap('Dark2',len(detectorIDs));

#extract x,y and detector data from the pixels
detector,x,y=[],[],[];
for pix in jsonPixels :
    detector.append(detectorIDs.index(pix['m_detectorID']));
    x.append(pix['m_column']);y.append(pix['m_row'])

#generate a figure and plot the pixels individually with color dependant on the detector
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111, aspect='equal')
for c, r, det in zip(x, y, detector):
    ax.add_patch(Rectangle(xy=(c,r),color=cmap(det),width=2,height=2));

#add a clorbar with size fixed to the plot
divider = make_axes_locatable(ax)
width = axes_size.AxesY(ax, aspect=1./20)
pad = axes_size.Fraction(0.5, width)
cax = divider.append_axes("right", size=width, pad=pad)
cbar=plt.colorbar(plt.cm.ScalarMappable(norm=None, cmap=cmap), cax=cax);
cbar.set_ticks(np.linspace(0.5/6,(len(detectorIDs)-1.5)/6.0,num=len(detectorIDs)))
cbar.set_ticklabels(detectorIDs)

#scale to full detector size and label axes
ax.axis([0,1024, 0, 512]);
ax.set_xlabel('column')
ax.set_ylabel('row')

#show the plot
plt.show()
