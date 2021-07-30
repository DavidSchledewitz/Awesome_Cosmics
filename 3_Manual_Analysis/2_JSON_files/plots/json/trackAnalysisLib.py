#!/usr/bin/env python3

# Analysis of GBL and Straight Line Tracks from Corryvrecken
#
# Author: Alexander Ferk

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
from matplotlib.patches import Rectangle
from operator import itemgetter
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size

################################################################################
# global variables
################################################################################

detectorIDs=['pALPIDEfs_0','pALPIDEfs_1','pALPIDEfs_2','pALPIDEfs_3',       'pALPIDEfs_4','pALPIDEfs_5','pALPIDEfs_6'];

################################################################################
# data manager class for data import
################################################################################

class datamanager:
    #options for the datamanager:
    #datamanager('output/data.json') - imports data from output/data.json
    #datamanager('output/data.npy') - imports data from output/data.npy
    #datamanager('output/data') - checks the age of output/data.json and output/data.npy and imports whichever is newer.
    #datamanager('output/data',update=False) - imports data from output/data.npy
    #datamanager('output/data',tempDataPath='temp') - imports data from output/data.json or temp/data.npy, whichever is newer. (use this to split corry and python output)
    #datamanager('output/data',update=False,tempDataPath='temp') - imports data from temp/data.npy
    #use removeJSONFile=true to automatically save the data to .npy and delete the input file
    #use verbose=true to get an output when data is imported
    
    pixels, clusters, tracks=[],[],[];
    eventMap, clusterMap,associatedClusterMap, pixelMap=[],[],[],[];
    file='';tempDataPath='';
    
    def __init__(this,ifile,verbose=False,update=True,
                 tempDataPath='',removeJSONFile=False,mapping=False):
        if not tempDataPath:
            this.tempDataPath=ifile.replace('/'+ifile.split('/')[-1],'');
        else:
            this.tempDataPath=tempDataPath;
        this.file=ifile.replace('.json','').replace('.npz','');
        
        if update and os.path.exists(this.file+'.json'):
            jsonTime=os.path.getmtime(this.file+'.json');
            if os.path.exists(this.tempDataPath+'/'+this.file.split('/')[-1]+'.npz'):
                npyTime=os.path.getmtime(this.tempDataPath+'/'+this.file.split('/')[-1]+'.npz');
                if npyTime>jsonTime:
                    update=False;
        
        if ifile.split('.')[-1]=='npy' :
            this.pixels, this.clusters, this.tracks, \
                this.eventMap, this.clusterMap, this.associatedClusterMap,\
                this.pixelMap=np.load(this.file+'.npy',allow_pickle=True);
            if verbose:
                print('Imported %d Pixels, %d Clusters, %d Tracks from %s'%
                      (len(this.pixels),len(this.clusters),len(this.tracks), \
                       this.file+'.npz'));
        elif ifile.split('.')[-1]=='json' or \
            (update and not '.json' in ifile and os.path.exists(this.file+'.json')):
            with open(this.file+'.json') as jsonfile:
                jsonData = json.load(jsonfile);
            #flatten the data structure to two lists and generate a map
            data=[[] for _ in range(4)];
            failedCnt=0;
            for event in jsonData:
                eventStart=[len(data[0]),len(data[1]),len(data[2])]
                for obj in event:
                    if not '_typename' in obj:
                        failedCnt+=1; continue;
                    typename=obj['_typename']
                    if typename=='corryvreckan::Pixel' :
                        data[0].append(obj);
                    elif typename=='corryvreckan::Cluster' :
                        data[1].append(obj);
                    elif typename=='corryvreckan::GblTrack' :
                        data[2].append(obj);
                    elif typename=='corryvreckan::StraightLineTrack' :
                        data[2].append(obj);
                    else :
                        failedCnt+=1;
                currentEventMap=[];
                for i in range(3):
                    if eventStart[i]==len(data[i]):
                        currentEventMap.append((-1,-1));
                    else :
                        currentEventMap.append((eventStart[i],len(data[i])-1));
                data[3].append(tuple(currentEventMap.copy()))
            if failedCnt>0:
                print('%d objects were not importet from %s.'%(failedCnt,this.file+'.json'));
        
            this.pixels=np.array(data[0]);
            this.clusters=np.array(data[1]);
            this.tracks=np.array(data[2]);
            this.eventMap=np.array(data[3]);
            
            if verbose:
                print('Imported %d Pixels, %d Clusters, %d Tracks from %s'%
                      (len(this.pixels),len(this.clusters),len(this.tracks), \
                       this.file+'.json'));
        elif (not update and not '.' in ifile.split('/')[-1]) or \
            (not os.path.exists(this.file+'.json') and removeJSONFile) :
            loadedData=np.load(this.tempDataPath+'/'+this.file.split('/')[-1]+'.npz',
                                      allow_pickle=True);
            this.pixels=loadedData['pixels'];
            this.clusters=loadedData['clusters'];
            this.tracks=loadedData['tracks'];
            this.eventMap=loadedData['eventMap'];
            this.clusterMap=loadedData['clusterMap'];
            this.associatedClusterMap=loadedData['associatedClusterMap'];
            this.pixelMap=loadedData['pixelMap'];
            if verbose:
                print('Imported %d Pixels, %d Clusters, %d Tracks from %s'%
                      (len(this.pixels),len(this.clusters),len(this.tracks),\
                       this.tempDataPath+'/'+this.file.split('/')[-1]+'.npz'));
        else :
            print('unknown file format');return;
        
        if (removeJSONFile and os.path.exists(this.file+'.json')):
            this.save();
            os.remove(this.file+'.json');
            if verbose:
                print('Removed file: '+this.file+'.json');
        
        if mapping and (not this.clusterMap or not this.pixelMap):
            this.createPixelMapping();
            this.createClusterMapping();

    def save(this,saveFile=''):
        if not saveFile:
            saveFile=this.tempDataPath+'/'+this.file.split('/')[-1]+'.npz';
        np.savez_compressed(saveFile,pixels=this.pixels,
                          clusters=this.clusters,
                          tracks=this.tracks,
                          eventMap=this.eventMap,
                          clusterMap=this.clusterMap,
                          associatedClusterMap=this.associatedClusterMap,
                          pixelMap=this.pixelMap);


    def createClusterMapping(this):
        clusterMap,associatedClusterMap=[],[];
        for event in range(len(this.eventMap)):
            #create track->cluster mapping
            if np.array(this.eventMap)[event,2][0]!=-1 :
                for t in range(np.array(this.eventMap)[event,2][0],np.array(this.eventMap)[event,2][1]+1):
                    clusterUIDs,associatedClusterUIDs=[],[];
                    currentClusterMap,currentAssociatedClusterMap=[],[];
                    for clusterRef in this.tracks[t]['track_clusters_']:
                        clusterUIDs.append(clusterRef['fUniqueID']);
                    for clusterRef in this.tracks[t]['associated_clusters_']:
                        associatedClusterUIDs.append(clusterRef['fUniqueID']);
                    for c in range(np.array(this.eventMap)[event,1][0],np.array(this.eventMap)[event,1][1]+1):
                        if this.clusters[c]['fUniqueID'] in clusterUIDs:
                            currentClusterMap.append(c);
                        if this.clusters[c]['fUniqueID'] in associatedClusterUIDs:
                            currentAssociatedClusterMap.append(c);
                    clusterMap.append(currentClusterMap);
                    associatedClusterMap.append(currentAssociatedClusterMap);
        this.clusterMap=clusterMap;
        this.associatedClusterMap=associatedClusterMap;
    def createPixelMapping(this):
        for event in range(len(this.eventMap)):
            #create cluster->pixel mapping
            if np.array(this.eventMap)[event,1][0]!=-1 :
                for c in range(np.array(this.eventMap)[event,1][0],np.array(this.eventMap)[event,1][1]+1):
                    pixelUIDs=[];
                    currentPixelMap=[];
                    for pixelRef in this.clusters[c]['m_pixels']:
                        pixelUIDs.append(pixelRef['fUniqueID']);
                    for p in range(np.array(this.eventMap)[event,0][0],np.array(this.eventMap)[event,0][1]+1):
                        if this.pixels[p]['fUniqueID'] in pixelUIDs:
                            currentPixelMap.append(p);
                    this.pixelMap.append(currentPixelMap);


    def getClusterCoordinates(this, cluster,key=''):
        if not key : key='m_global'
        if 'fZ' in cluster[key]['fCoordinates']:
            return (cluster[key]['fCoordinates']['fX'],
                    cluster[key]['fCoordinates']['fY'],
                    cluster[key]['fCoordinates']['fZ']);
        else:
            return (cluster[key]['fCoordinates']['fX'],
                    cluster[key]['fCoordinates']['fY']);

    def getClustersCoordinates(this,clusters,key=''):
        coordinates=[];
        if type(clusters) == tuple:
            for cluster in this.clusters[clusters[0]:clusters[1]+1]:
                coordinates.append(this.getClusterCoordinates(cluster,key))
        elif type(clusters) == list and type(clusters[0]) == int:
            for c in clusters :
                coordinates.append(this.getClusterCoordinates(this.clusters[c],key))
        else :
            for cluster in clusters :
                coordinates.append(this.getClusterCoordinates(cluster,key))
        return np.array(coordinates);

    def getTrackParameters(this,track,key='',event=''):
        if track['_typename'] == 'corryvreckan::StraightLineTrack' :
            if not key:
                return ((track['m_state']['fCoordinates']['fX'],
                         track['m_state']['fCoordinates']['fY'],
                         track['m_state']['fCoordinates']['fZ']),
                        (track['m_direction']['fCoordinates']['fX'],
                         track['m_direction']['fCoordinates']['fY'],
                         track['m_direction']['fCoordinates']['fZ']));
            else:
                pars=[];
                for par in track[key] :
                    if 'fZ' in par['second']['fCoordinates'].keys():
                        pars.append((par['second']['fCoordinates']['fX'],
                                     par['second']['fCoordinates']['fY'],
                                     par['second']['fCoordinates']['fZ']));
                    else :
                        pars.append((par['second']['fCoordinates']['fX'],
                                     par['second']['fCoordinates']['fY']));
                return (track['m_state']['fCoordinates']['fX'],
                        track['m_state']['fCoordinates']['fY']), pars;
        elif track['_typename'] == 'corryvreckan::GblTrack' :
            if type(event)!=str:
                seedCoordinates=this.getClusterCoordinates(this.clusters[
                     next((c for c in range(event[1][0],event[1][1]+1) if track['seed_cluster_']['fUniqueID']==this.clusters[c]['fUniqueID']),None)]);
            else:
                seedCoordinates=this.getClusterCoordinates(
                    next((c for c in this.clusters if track['seed_cluster_']['fUniqueID']==c['fUniqueID']),None));
            if not key : key='corrections_';
            pars=[];
            for par in track[key] :
                if 'fZ' in par['second']['fCoordinates'].keys():
                    pars.append((par['second']['fCoordinates']['fX'],
                                 par['second']['fCoordinates']['fY'],
                                 par['second']['fCoordinates']['fZ']));
                else :
                    pars.append((par['second']['fCoordinates']['fX'],
                                 par['second']['fCoordinates']['fY']));
        return seedCoordinates, pars;


    def getTracksParamters(this,tracks,key=''):
        params=[];
        if type(tracks) == tuple:
            for track in this.tracks[tracks[0]:tracks[1]+1]:
                params.append(this.getTrackParameters(track, key))
        elif type(tracks) == list and type(tracks[0]) == int:
            for t in tracks:
                params.append(this.getTrackParameters(this.tracks[t], key))
        else :
            for track in tracks:
                params.append(this.getTrackParameters(track, key))
        return params;

    def getPixelsForCluster(this, cluster, id=False, event=''):
        return this.getPixelsForClusters([cluster], id=id, event=event);

    def getPixelsForClusters(this, clusters, id=False, event=''):
        if this.pixelMap and ids:
            return np.array(this.pixelMap)[clusters];
        else :
            pixelUIDs,pixels=[],[];
            for cluster in clusters:
                for pixelRef in cluster['m_pixels']:
                    pixelUIDs.append(pixelRef['fUniqueID']);
            if type(event)!=str:
                if event[0][0]==-1:
                    raise ValueError('Pixels of given event must not be empty!');
                for p in range(event[0][0],event[0][1]+1):
                    pixel=this.pixels[p]
                    if pixel['fUniqueID'] in pixelUIDs:
                        if id: pixels.append(p);
                        else : pixels.append(pixel);
            else:
                for p in range(len(this.pixels)) :
                    pixel=this.pixels[p]
                    if pixel['fUniqueID'] in pixelUIDs:
                        if id: pixels.append(p);
                        else : pixels.append(pixel);
            return pixels;

    def getClustersForTrack(this, track, id=False, event=''):
        return this.getClustersForTracks([track], id=id, event=event);

    def getClustersForTracks(this, tracks, id=False, event=''):
        if this.clusterMap and id:
            return np.array(this.clusterMap)[tracks],np.array(this.associatedClusterMap)[tracks];
        else :
            clusterUIDs,clusters=[],[];
            associatedclusterUIDs,associatedclusters=[],[];
            for track in tracks:
                for clusterRef in track['track_clusters_']:
                    clusterUIDs.append(clusterRef['fUniqueID']);
                for clusterRef in track['associated_clusters_']:
                    associatedclusterUIDs.append(clusterRef['fUniqueID']);
                if type(event)!=str:
                    for c in range(event[1][0],event[1][1]+1) :
                        cluster=this.clusters[c]
                        if cluster['fUniqueID'] in clusterUIDs:
                            if id: clusters.append(c);
                            else : clusters.append(cluster);
                        if cluster['fUniqueID'] in associatedclusterUIDs:
                            if id: associatedclusters.append(c);
                            else : associatedclusters.append(cluster);
                else:
                    for c in range(len(this.clusters)) :
                        cluster=this.clusters[c]
                        if cluster['fUniqueID'] in clusterUIDs:
                            if id: clusters.append(c);
                            else : clusters.append(cluster);
                        if cluster['fUniqueID'] in associatedclusterUIDs:
                            if id: associatedclusters.append(c);
                            else : associatedclusters.append(cluster);
                return clusters,associatedclusters;

def findEquivalentTrackByClusters(track, dm1, dm2, id=False) :
    clusterCoords=dm1.getClustersCoordinates(dm1.getClustersForTracks([track])[0]);
    for t in range(len(dm2.tracks)):
        searchClusterCoords=dm2.getClustersCoordinates(dm2.getClustersForTracks([dm2.tracks[t]])[0]);
        if (searchClusterCoords==clusterCoords).all():
            if id:
                return t;
            else:
                return dm2.tracks[t];


cluster_shape_dict={((0,0)):0,
((0,0),):0,
((0,0),(0,1)):1,
((0,0),(1,0)):2,
((0,0),(0,1),(1,0)):3,
((0,0),(1,0),(1,1)):4,
((0,1),(1,0),(1,1)):5,
((0,0),(0,1),(1,1)):6,
((0,0),(0,-1),(0,1)):7,
((0,0),(-1,0),(1,0)):8,
((0,0),(0,1),(1,0),(1,1)):9,
((0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)):10,
((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)):11
};

cluster_pattern_dict={0:((0,0),),
1:((0,0),(0,1)),
2:((0,0),(1,0)),
3:((0,0),(0,1),(1,0)),
4:((0,0),(1,0),(1,1)),
5:((0,1),(1,0),(1,1)),
6:((0,0),(0,1),(1,1)),
7:((0,0),(0,-1),(0,1)),
8:((0,0),(-1,0),(1,0)),
9:((0,0),(0,1),(1,0),(1,1)),
10:((0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)),
11:((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2))
};

def getClusterShape(dm,cluster,event='',
                    cluster_shape_dict=cluster_shape_dict):
    if len(cluster['m_pixels'])==0:
        raise ValueError('Cluster with 0 pixels given!');
    
    if type(event)!=str:
        if -1 in event[1]:
            raise ValueError('No clusters in given event!');
        if -1 in event[0]:
            raise ValueError('No pixels in given event!');
        pixels=dm.getPixelsForCluster(cluster,event=event);
    else:
        pixels=dm.getPixelsForCluster(cluster);

    row,col=[],[];
    for pix in pixels :
        col.append(pix['m_column']);row.append(pix['m_row'])
    origin=(min(col),min(row));
    col=np.array(col)-min(col);
    row=np.array(row)-min(row);
    pattern=tuple(sorted(zip(col,row)));
    shape=-1;
    if pattern in cluster_shape_dict.keys():
        shape=cluster_shape_dict[pattern];
    return shape, pattern, origin;


def calculateDutClusterDistance(dm,detectorInclude=['pALPIDEfs_3'],chi2ndof_cut=3,
                                closestCluster=False,clusterFilter='',
                                correction_fun=''):
    dX,dY=[],[];
    x,y=[],[];
    cUIDs,tUIDs,nEvent=[],[],[];
    trackCnt=0;
    for e in range(len(dm.eventMap)):
        event=dm.eventMap[e]
        if event[2][0]==-1: continue;
        for t in range(event[2][0],event[2][1]+1):
            track=dm.tracks[t];
            if chi2ndof_cut:
                if (type(chi2ndof_cut)==int or type(chi2ndof_cut)==float):
                    if track['chi2ndof_']>chi2ndof_cut:
                        continue;
                elif chi2ndof_cut(track['chi2ndof_']):
                    continue;
            zPlanes=[-60,-40,-20,0,20,40,60];
            if track['_typename'] == 'corryvreckan::GblTrack' :
                for cluster in dm.clusters[event[1][0]:event[1][1]]:
                    if track['seed_cluster_']['fUniqueID']==cluster['fUniqueID']:
                        s=dm.getClusterCoordinates(cluster);break;
                par=[];
                for p in track['corrections_'] :
                    par.append((p['second']['fCoordinates']['fX'],
                                p['second']['fCoordinates']['fY'],
                                p['second']['fCoordinates']['fZ']));
                par=np.array(par);
                cTrack=(np.add(par[:,0],s[0]),np.add(par[:,1],s[1]),zPlanes);
            elif track['_typename'] == 'corryvreckan::StraightLineTrack' :
                s=(track['m_state']['fCoordinates']['fX'],track['m_state']['fCoordinates']['fY']);
                cTrack=(s[0]+np.dot(track['m_direction']['fCoordinates']['fX'],zPlanes),
                        s[1]+np.dot(track['m_direction']['fCoordinates']['fY'],zPlanes),
                        zPlanes);
            associatedclusterUIDs,associatedclusters=[],[];
            for clusterRef in track['associated_clusters_']:
                associatedclusterUIDs.append(clusterRef['fUniqueID']);
            for c in range(event[1][0],event[1][1]+1) :
                cluster=dm.clusters[c]
                if cluster['fUniqueID'] in associatedclusterUIDs:
                    associatedclusters.append(cluster);
            if not associatedclusters:
                continue;
            for cluster in associatedclusters:
                closestClusterID='';
                if closestCluster:
                    for closestCluster in track['closest_cluster_']:
                        if closestCluster['first']==cluster['m_detectorID']:
                            closestClusterID=closestCluster['second']['fUniqueID'];
                if not closestClusterID or closestClusterID!=cluster['fUniqueID']:
                    continue;
                if not (cluster['m_detectorID'] in detectorInclude):
                    continue;
                if clusterFilter:
                    if not clusterFilter(dm,event,track,cluster):
                        continue;
                c=dm.getClusterCoordinates(cluster)
                p=np.array(cTrack)[:,zPlanes.index(c[2])];
                if correction_fun:
                    d=correction_fun(p,c,cluster,track,event)
                    dX.append(d[0]);
                    dY.append(d[1]);
                else:
                    dX.append(p[0]-c[0]);
                    dY.append(p[1]-c[1]);
                tUIDs.append(track['fUniqueID']);
                cUIDs.append(cluster['fUniqueID']);
                nEvent.append(e);
                x.append(c[0]);y.append(c[1]);
    return list(zip(dX,dY,x,y,cUIDs,tUIDs,nEvent));

################################################################################
# functions for text output
################################################################################

def printTrackParamterStatistics(dm):
    if dm.tracks[0]['_typename'] == 'corryvreckan::StraightLineTrack':
        params=dm.getTracksParamters((0,len(dm.tracks)));
        p=np.array(params)[:,0,:];dir=np.array(params)[:,1,:];
        print('--- Straight Line Track Statistics: %d Tracks ---'%(len(dm.tracks)))
        print('Mean Point / Std. Point')
        print(np.mean(np.array(p),0),' / ',np.std(np.array(p),0));
        print('Mean Direction / Std. Direction')
        print(np.mean(np.array(dir),0),' / ',np.std(np.array(dir),0));
    elif dm.tracks[0]['_typename'] == 'corryvreckan::GblTrack' :
        kinks=np.array(dm.getTracksParamters((0,len(dm.tracks)),key='m_kink'))[:,1];
        corr=np.array(dm.getTracksParamters((0,len(dm.tracks)),key='corrections_'))[:,1];
        res=np.array(dm.getTracksParamters((0,len(dm.tracks)),key='residual_global_'))[:,1];
        kinks=np.array(list(map(np.array,kinks)));
        corr=np.array(list(map(np.array,corr)));
        res=np.array(list(map(np.array,res)));
        print('--- GBL Track Statistics: %d Tracks ---'%(len(dm.tracks)))
        print('Mean Kinks')
        print(np.mean(np.array(kinks),0));
        print('Std. Kinks')
        print(np.std(np.array(kinks),0));
        print('Mean Residual (reference planes)')
        print(np.mean(np.array(res),0));
        print('Std. Residual (reference planes)')
        print(np.std(np.array(res),0));
        print('Mean Corrections')
        print(np.mean(np.array(corr),0));
        print('Std. Corrections')
        print(np.std(np.array(corr),0));

def printTrackParamters(track,dm):
    if track['_typename'] == 'corryvreckan::StraightLineTrack':
        p,dir=dm.getTrackParameters(track);
        print('--- Straight Line Track ---')
        print('Point:', (*p,0))
        print('Direction:', (*dir,1));
    elif track['_typename'] == 'corryvreckan::GblTrack' :
        s,corr=dm.getTrackParameters(track);
        print('--- GBL Track ---')
        print('Corrections:')
        print(np.array(corr));
        print('Seedcluster: ',tuple(s));

def telescopeOptimizerURL(track,dm):
    clusters=dm.getClustersForTracks([gblTrack])
    clusters=[*clusters[0],*clusters[1]];
    y=dm.getClustersCoordinates(clusters)[:,1];
    return 'http://mmager.web.cern.ch/mmager/telescope/tracking.html#part=e \
&p=5.4\
&x=[-10,-6,-4,-2,0,2,4,6,10]\
&XX0=[,0.0005,0.0005,0.001,0.001,0.001,0.0005,0.0005,]\
&sy=[,0.0005,0.0005,0.0005,0.0005,0.0005,0.0005,0.0005,]\
&en=[0,1,1,0,0,0,1,1,0]\
&ymc=[0,0,0,0,0,0,0,0,0]\
&ym='+str(list(np.concatenate([[0],np.array(y)/10,[0]]))).replace(' ','')+'\
&scaley='+str(np.around(np.max(np.array(y)/10)))+'\n\n';

################################################################################
# functions for plotting
################################################################################

def plotPixelsForTrack(track,dm,ax=''):
    if not ax:
        fig = plt.figure(figsize=(12,6));
        ax=fig.add_subplot(111,aspect='equal');
    clusters=dm.getClustersForTracks([track]);
    cCluster=dm.getClustersCoordinates([*clusters[0],*clusters[1]]);
    pixels=dm.getPixelsForClusters([*clusters[0],*clusters[1]]);
    detector,x,y=[],[],[];
    for pix in pixels :
        detector.append(ta.detectorIDs.index(pix['m_detectorID']));
        x.append(pix['m_column']);y.append(pix['m_row'])
    cmap=plt.cm.get_cmap('Dark2',len(detectorIDs));
    for x, y, det in zip(x, y, detector):
        ax.add_patch(Rectangle(xy=(x,y),color=cmap(det),width=1,height=1));
    cdetector,cx,cy=[],[],[];
    for c in [*clusters[0],*clusters[1]] :
        cdetector.append(ta.detectorIDs.index(c['m_detectorID']));
        cx.append(c['m_column']);cy.append(c['m_row'])
    cdetector,cx,cy=zip(*sorted(zip(cdetector,cx,cy)))
    ax.plot(cx,cy);
    ax.axis([0,1024, 0, 512]);
    divider = make_axes_locatable(ax)
    width = axes_size.AxesY(ax, aspect=1./20)
    pad = axes_size.Fraction(0.5, width)
    cax = divider.append_axes("right", size=width, pad=pad)
    cbar=plt.colorbar(plt.cm.ScalarMappable(norm=None, cmap=cmap),cax=cax);
    cbar.set_ticks(np.linspace(0.5/6,(len(ta.detectorIDs)-1.5)/6.0,num=len(ta.detectorIDs)))
    cbar.set_ticklabels(ta.detectorIDs)
    ax.set_xlabel('column')
    ax.set_ylabel('row')

def plotTrack(track,dm,fig='',proj='xy') :
    if not fig: plt.figure(figsize=(10,8));
    a=[['x','y','z'].index(proj[0]),['x','y','z'].index(proj[1])];
    cmap=plt.cm.get_cmap('Dark2',len(detectorIDs));
    clusters=dm.getClustersForTracks([track]);
    cCluster=dm.getClustersCoordinates([*clusters[0],*clusters[1]]);
    cplt=plt.scatter(cCluster[:,a[0]],cCluster[:,a[1]],
                     c=cmap([detectorIDs.index(c['m_detectorID']) for c in [*clusters[0],*clusters[1]]]), label='Clusterposition');
    zPlanes=sorted(cCluster[:,2]);
    s,par=dm.getTrackParameters(track);
    zPlanesRef=dm.getClustersCoordinates(clusters[0])[:,2]
    res=np.array(dm.getTrackParameters(track,key='residual_global_')[1]);
    if track['_typename'] == 'corryvreckan::StraightLineTrack':
        cTrack=(s[0]+np.dot(par[0],zPlanes),s[1]+np.dot(par[1],zPlanes),zPlanes);
        cError=((s[0]+np.dot(par[0],zPlanesRef),s[1]+np.dot(par[1],zPlanesRef),zPlanesRef),
                (res[:,0],res[:,0],np.zeros((1,len(res[:,0])))[0]));
    elif track['_typename'] == 'corryvreckan::GblTrack' :
        par=np.array(par);
        cTrack=(np.add(par[:,0],s[0]),np.add(par[:,1],s[1]),zPlanes);
        parRef=[]
        for zp in zPlanes:
            if zp in zPlanesRef:
                parRef.append(par[zPlanes.index(zp)]);
        parRef=np.array(parRef);
        cError=((np.add(parRef[:,0],s[0]),np.add(parRef[:,1],s[1]),zPlanesRef),
                (res[:,0],res[:,0],np.zeros((1,len(res[:,0])))[0]));
    tplt=plt.plot(cTrack[a[0]],cTrack[a[1]],label=track['_typename'].split('::')[-1]);
    errplt=plt.errorbar(x=cError[0][a[0]],y=cError[0][a[1]],
                        xerr=cError[1][a[0]],yerr=cError[1][a[1]],
                        label='Reference Plane Residuals', fmt=' ',capsize=3)
    cbar=plt.colorbar(plt.cm.ScalarMappable(norm=None, cmap=cmap));
    cbar.set_ticks(np.linspace(0.5/6,(len(detectorIDs)-1.5)/6.0,num=len(detectorIDs)))
    cbar.set_ticklabels(detectorIDs)
    plt.xlabel('%s / mm'%(['x','y','z'][a[0]]));
    plt.ylabel('%s / mm'%(['x','y','z'][a[1]]));
    plt.legend();
