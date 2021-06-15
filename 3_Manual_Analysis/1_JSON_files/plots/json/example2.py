#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
from matplotlib.patches import Rectangle
import sys
import trackAnalysisLib as ta

#This example plots a Straight Line Track and GBL Track with the same clusters

# read pixels, clusters and tracks from JSON
dmGbl=ta.datamanager('./data/GBLTracks.json');
dmS=ta.datamanager('./data/StraightTracks.json');

#select one gbl track we want to analyze
gblTrack=dmGbl.tracks[0];

#find the equivalent straight line track
sTrack=ta.findEquivalentTrackByClusters(gblTrack, dmGbl, dmS);

#plot comparison in xy projection
fig = plt.figure(figsize=(10,8));
proj='xz';a=[['x','y','z'].index(proj[0]),['x','y','z'].index(proj[1])];
cmap=plt.cm.get_cmap('Dark2',len(ta.detectorIDs));
clusters=dmGbl.getClustersForTracks([gblTrack]);
cCluster=dmGbl.getClustersCoordinates([*clusters[0],*clusters[1]]);
cplt=plt.scatter(cCluster[:,a[0]],cCluster[:,a[1]],
                 c=cmap([ta.detectorIDs.index(c['m_detectorID']) for c in [*clusters[0],*clusters[1]]]), label='Clusterposition');
zPlanes=sorted(cCluster[:,2]);
zPlanesRef=dmGbl.getClustersCoordinates(clusters[0])[:,2]

s,par=dmGbl.getTrackParameters(gblTrack);
res=np.array(dmGbl.getTrackParameters(gblTrack,key='residual_global_')[1]);
par=np.array(par);
cTrack=(np.add(par[:,0],s[0]),np.add(par[:,1],s[1]),zPlanes);
parRef=[]
for zp in zPlanes:
    if zp in zPlanesRef:
        parRef.append(par[zPlanes.index(zp)]);
parRef=np.array(parRef);
cError=((np.add(parRef[:,0],s[0]),np.add(parRef[:,1],s[1]),zPlanesRef),
        (res[:,0],res[:,0],np.zeros((1,len(res[:,0])))[0]));
tplt=plt.plot(cTrack[a[0]],cTrack[a[1]],'b',label='GblTrack');
errplt=plt.errorbar(x=cError[0][a[0]],y=cError[0][a[1]],
                    xerr=cError[1][a[0]],yerr=cError[1][a[1]],
                    label='Residuals (ref.) for GblTrack', fmt=' ',capsize=3,c='g')

s,par=dmS.getTrackParameters(sTrack);
res=np.array(dmS.getTrackParameters(sTrack,key='residual_global_')[1]);
cTrack=(s[0]+np.dot(par[0],zPlanes),s[1]+np.dot(par[1],zPlanes),zPlanes);
cError=((s[0]+np.dot(par[0],zPlanesRef),s[1]+np.dot(par[1],zPlanesRef),zPlanesRef),
            (res[:,0],res[:,0],np.zeros((1,len(res[:,0])))[0]));
tplt=plt.plot(cTrack[a[0]],cTrack[a[1]],'r',label='Straight Track');
errplt=plt.errorbar(x=cError[0][a[0]],y=cError[0][a[1]],
                    xerr=cError[1][a[0]],yerr=cError[1][a[1]],
                    label='Residuals (ref.) for Straight Track', fmt=' ',capsize=3,c='orange')

cbar=plt.colorbar(plt.cm.ScalarMappable(norm=None, cmap=cmap));
cbar.set_ticks(np.linspace(0.5/6,(len(ta.detectorIDs)-1.5)/6.0,num=len(ta.detectorIDs)))
cbar.set_ticklabels(ta.detectorIDs)
plt.xlabel('%s / mm'%(['x','y','z'][a[0]]));
plt.ylabel('%s / mm'%(['x','y','z'][a[1]]));
plt.legend();

#save or show the plot dependant on user input
if 'show' in sys.argv:
    plt.show();
if 'save' in sys.argv:
    plt.savefig('Track_Comparison.png');
