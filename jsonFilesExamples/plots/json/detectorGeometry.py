#!/usr/bin/env python3

import numpy as np
from scipy.spatial.transform import Rotation

#default units - mm is 1 to comply with corryvreckan
units = {'m':1e3,'um':1e-3,'mm':1,'':1,'deg':1,'us':1e-6}
def stringValueConversion(string):
    unit=string.strip('0123456789.,+- ');
    value=float(string.strip(unit));
    value=value*units[unit];
    return value;

def stringsValueConversion(strings):
    values=[]
    for s in strings:
        values.append(stringValueConversion(s));
    return values;


class geometry:
    detectors=[];
    def __init__(this,file_name):
        auto_convert=['material_budget',
                      'number_of_pixels',
                      'orientation',
                      'pixel_pitch',
                      'position',
                      'spatial_resolution',
                      'time_resolution'];
        detector={};
        with open(file_name,'r') as file:
            for line in file:
                if '=' in line:
                    if line.split('=')[0].strip() in auto_convert:
                        val=stringsValueConversion(line.split('=')[1].strip(' \n\"').split(','));
                        detector[line.split('=')[0].strip()]=val;
                    else:
                        detector[line.split('=')[0].strip()]=line.split('=')[1].strip(' \n\"');
                elif '[' in line:
                    if detector and detector['name']:
                        this.detectors.append(detector.copy());
                        detector['name']=line.strip('[]\n');
                    else:
                        detector['name']=line.strip('[]\n');
            this.detectors.append(detector);

    def getDetectorByName(this,name):
        for detector in this.detectors:
            if detector['name']==name:
                return detector;

    def globalToLocal(this,globalPos,detectorName):
        detector=this.getDetectorByName(detectorName);
        #rotation=Rotation.from_rotvec(np.radians(detector['orientation'])).inv();
        mode=detector['orientation_mode'].lower();
        rotation=Rotation.from_euler(mode,detector['orientation'],degrees=True).inv();
        return rotation.apply(globalPos-detector['position']);
        #return globalPos-detector['position'];

    def localToGlobal(this,localPos,detectorName):
        detector=this.getDetectorByName(detectorName);
        #rotation=Rotation.from_rotvec(np.radians(detector['orientation']));
        mode=detector['orientation_mode'].lower();
        rotation=Rotation.from_euler(mode,detector['orientation'],degrees=True);
        return rotation.apply(localPos)+detector['position'];
        #return localPos+detector['position'];

    def localToColRow(this,localPos,detectorName):
        detector=this.getDetectorByName(detectorName);
        pitch=detector['pixel_pitch'];
        n_pixels=detector['number_of_pixels'];
        col=localPos[0]/pitch[0]+n_pixels[0]/2-0.5;
        row=localPos[1]/pitch[1]+n_pixels[1]/2-0.5;
        return (col,row);

    def globalToColRow(this,globalPos,detectorName):
        localPos=this.globalToLocal(globalPos,detectorName);
        return this.localToColRow(localPos,detectorName);

    def colRowToLocal(this,colRow,detectorName):
        detector=this.getDetectorByName(detectorName);
        pitch=detector['pixel_pitch'];
        n_pixels=detector['number_of_pixels'];
        x=(colRow[0]-n_pixels[0]/2+0.5)*pitch[0];
        y=(colRow[1]-n_pixels[1]/2+0.5)*pitch[1];
        return np.array((x,y,0));

    def colRowToGlobal(this,colRow,detectorName):
        localPos=this.colRowToLocal(colRow,detectorName);
        return this.localToGlobal(localPos,detectorName);
