import numpy as np
import matplotlib.pyplot as plt
import hit_data_unaligned as Data

hit_data = Data.hit_data

planes_used = [0,6]   #Planes fixed for alignment
alignments = 20       #Number of alignment steps (~50 recommended)
fine_alignments = 10  #Number of fine alignment steps (~10 recommended)
plot_each_step = False#Debugging
chi2_cut = np.logspace(5.3,1,alignments-fine_alignments)
min_chi2_reached = False

min_nop = 4
N = len(hit_data) # Number of events (hardcoded for now)
ppx, ppy, ppz = 0.02924, 0.02688, 20
cnt = 0

plt.style.use('bmh')

# {{{ Plot Function
def plot(n,connect_hits,plot_tracks,min_nop):
    #Dimensions of the detector
    xlim = 1023*ppx
    ylim = 511*ppy
    zlim = 6*ppz

    #Create a figure object
    fig = plt.figure(figsize=(20,20))
    ax = plt.axes(projection='3d')    #Create 3d Axes
    ax._axis3don = False              #... but invisible
    #ax.set_box_aspect((xlim,ylim,zlim))       #Define aspect ratio (doesn't work in jupyter)
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
        ax.plot_surface(X-posx[plane][a],
                Y-posy[plane][a],
                Z,alpha=.1,color='black')

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
    #plt.savefig('GIF{}.png'.format(a))
    plt.show()
# }}}

# Plot chi2 Function {{{
def plotchi2(chi2_cut,number_of_bins):
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
    plt.show()
# }}}

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

    print('Tracking...')

    plot(3,False,True,6)

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

    if min_chi2_reached:
        print('Fine Alignment iteration {}'.format(a-alignments+fine_alignments+1))

    # Fill Residual Dictionary
    print('Calculating Residuals...')
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

    # Append changes to position array
    print('{} Tracks survived the chi2 cut of {}'.format(cnt_track,chi2_cut[cnt]))
    if cnt_track <= 200: print('WARNING!!! CHI2 CUT MIGHT BE TOO STRONG')

    for plane in range(7):
        print("Offset plane {}: x = {} y = {}".format(
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

for plane in range(7):
    print('Plane {} X: {} +- {}'.format(
        plane,np.round(posx[plane][alignments],2),np.round(dposx[plane][alignments],2)))
    print('Plane {} Y: {} +- {}'.format(
        plane,np.round(posy[plane][alignments],2),np.round(dposy[plane][alignments],2)))

# Plot section {{{
print('Plotting...')
markers=['o','^','x','s','p','h','D']
col=['#fbcf36','#ed4c1c','#9c7e70','#5ac2f1','#11776c','#e0363a','#6a1c10']
xaxis = np.arange(alignments+1)
plt.figure(figsize=(10,5))
plt.xlabel('Alignment iterations')
plt.ylabel('Plane position in X [μm]')
#plt.ylim(-1000,400)
for plane in range(7):
    if plane in planes_used: continue
    plt.errorbar(xaxis,posx[plane],yerr=dposx[plane], label='Plane {}'.format(plane+1),
            linewidth=1,marker=markers[plane],color='black',capsize=3,mfc=col[plane])
plt.legend()
plt.tight_layout()

plt.figure(figsize=(10,5))
plt.xlabel('Alignment iterations')
plt.ylabel('Plane position in Y [μm]')
#plt.ylim(-1200,600)
for plane in range(7):
    if plane in planes_used: continue
    plt.errorbar(xaxis,posy[plane],yerr=dposy[plane], label='Plane {}'.format(plane+1),
            linewidth=1,marker=markers[plane],color='black',capsize=3,mfc=col[plane])
plt.legend()
plt.tight_layout()
plt.show()
# }}}

plot(10,True,True,5)

plotchi2(10,np.arange(0,10,.25))

# Write to file for further anaylsis
fx = open("hit_data_aligned.py","w")
fx.write("hit_data = "+str(hit_data))
fx.close
