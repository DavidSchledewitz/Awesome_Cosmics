#!/usr/bin/env python3
from tempfile import TemporaryFile
# outfile = TemporaryFile()
# np.savez(outfile, x=x, y=y)
# _ = outfile.seek(0)
# npzfile = np.load(outfile)
# sorted(npzfile.files)
# ['x', 'y']
# npzfile['x']
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# np.save(outfile, x)
# np.load(outfile)
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

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

#extract 1000 objects of type 'corryvreckan::Pixel'
jsonPixels=[];
for event in data:
    for obj in event:
        if obj['_typename']=='corryvreckan::Pixel' :
            jsonPixels.append(obj);
        if len(jsonPixels)>=10 :###############################################################1000 pixel cut
            break;
    if len(jsonPixels)>=10 :######################################################################see above
        break;

print(jsonPixels)