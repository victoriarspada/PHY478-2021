# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:39:33 2020
@author: Victoria Spada
Contact: victoria.spada@mail.utoronto.ca
Last edited: July 17 2020.
"""
import copy
import numpy
from numpy import sqrt
from instrument import instrument
import matplotlib.pyplot as plt
import os 

# This function produces and saves a figure with 3 subplots: 
# (1) Average O3 VMR Profiles.
# (2) Mean absolute difference profiles between the two instruments.
# (3) Mean Relative difference profiles between the two isntruments
# The function takes average O3 VMR for each year for the input instruments and plots
# these profiles on a common grid and then saves the figure.
# INPUT: 
# pair: The input to this function is an 'pair' class object.
# instruments: This is a list of strings, where the strings are the two instruments involved: 
# ie, ['ACE-FTS', 'DIAL']. The list must be two elements to be valid. 
# folder: String; the name of the folder in which we want to save the figure.
# OUTPUT: N/A

def averageVMRComparePlotter(pair,instruments,folder):
    altitude_grid = numpy.linspace(0.5,149.5,150)
    N_grid = [] # Create empty grid of dimensions for altitude grid.
    for i in range(0,len(altitude_grid),1):
       N_grid = N_grid + [numpy.NaN] # Create empty list for VMRs to be averaged on.
    alt=[]
    
    nd1=copy.deepcopy(N_grid) # Create copies of the empty grid
    nd1_err=copy.deepcopy(N_grid)
    N1 = copy.deepcopy(N_grid)
    nd2=copy.deepcopy(N_grid)
    nd2_err=copy.deepcopy(N_grid)
    N2=copy.deepcopy(N_grid)
    
    diff = copy.deepcopy(N_grid) # Create axis templates for mean absolute differences.
    diff_err = copy.deepcopy(N_grid)
    diffN = copy.deepcopy(N_grid)
    diff_stddev = copy.deepcopy(N_grid)
    
    rel_diff = copy.deepcopy(N_grid) # Create axis templates for mean relative differences.
    rel_diff_err = copy.deepcopy(N_grid)
    rel_diffN = copy.deepcopy(N_grid)
    rel_diff_stddev = copy.deepcopy(N_grid)

    spv_difference=copy.deepcopy(N_grid)
    spv_difference_N=copy.deepcopy(N_grid)  
    
    mad=[]
    madalt=[]
    mrd=[]
    mrdalt=[]
    
    cm = pair.coincident_pairs # Extract list of coincident pairs.

    for i in range(0,len(cm),1): # Each element contains two elements
       print('pair',i)
       curr_nd1=[]
       curr_nd2=[]
       curr_alt1=[]
       curr_alt2=[]
       curr_nd1_err=[]
       curr_nd2_err=[]
       if type(((cm[i])[0]).common_altitude)==list and type(((cm[i])[1]).common_altitude)==list and type(((cm[i])[0]).common_o3_vmr)==list and type(((cm[i])[1]).common_o3_vmr)==list:
         
          curr_alt1 = list(((cm[i])[0]).common_altitude) # Current altitude range #1 
          curr_nd1 = ((cm[i])[0]).common_o3_vmr # Current VMR profile #1
          curr_alt2 = list(((cm[i])[1]).common_altitude) # Current altitude range #2
          curr_nd2 = ((cm[i])[1]).common_o3_vmr
          curr_nd1_err = cm[i][0].common_o3_vmr_error # Current VMR error profile #1
          curr_nd2_err = cm[i][1].common_o3_vmr_error 
       # Find range of altitude where O3 VMR was recorded for both instruments.
       if len(curr_nd1)!=0 and len(curr_nd2)!=0 and len(curr_alt1)!=0 and len(curr_alt2)!=0 and len(curr_nd1_err)!=0 and len(curr_nd2_err)!=0:
          for j in range(0,len(curr_nd1),1):
             if numpy.isnan(curr_nd1[j])==False:
                break
          min1 = curr_alt1[j] # Index of minimum altitude with valid O3 VMR measurement.
          for j in range(len(curr_nd1)-1,-1,-1):
             if numpy.isnan(curr_nd1[j])==False:
                break
          max1 = curr_alt1[j] # Index of maximum altitude with a valid O3 VMR measurement.
          for j in range(0,len(curr_nd2),1):
             if numpy.isnan(curr_nd2[j])==False:
                break
          min2 = curr_alt2[j] # Index of minimum altitude with valid O3 VMR measurement.
          for j in range(len(curr_nd2)-1,-1,-1):
             if numpy.isnan(curr_nd2[j])==False:
                break
          max2 = curr_alt2[j] # Index of maximum altitude with a valid O3 VMR measurement.
          minalt = float(max(min1,min2))
          maxalt = float(min(max1,max2))
          k = minalt
          while k <= maxalt:
             curr_altitude = k
             curr_idx = list(altitude_grid).index(curr_altitude) # Find the index in the grid for the current altitude. 
             # Add measurements for instrument one. 
             idx1 = (curr_alt1).index(curr_altitude) # Find index for instrument 1 corresponding to the current altitude.
             idx2 = (curr_alt2).index(curr_altitude) # Find index for instrument 2 corresponding to the current altitude.
             if numpy.isnan(nd1[curr_idx])==False and numpy.isnan(curr_nd1_err[idx1])==False and numpy.isnan(curr_nd1[idx1])==False  and numpy.isnan(curr_nd2_err[idx2])==False and numpy.isnan(curr_nd2[idx2])==False:
                nd1[curr_idx] = nd1[curr_idx] + curr_nd1[idx1]
                N1[curr_idx] = N1[curr_idx] +1
                nd1_err[curr_idx] = nd1_err[curr_idx] + curr_nd1_err[idx1]
                
             if numpy.isnan(nd1[curr_idx])==True and numpy.isnan(curr_nd1_err[idx1])==False and numpy.isnan(curr_nd1[idx1])==False  and numpy.isnan(curr_nd2_err[idx2])==False and numpy.isnan(curr_nd2[idx2])==False:
                nd1[curr_idx] = curr_nd1[idx1]
                N1[curr_idx] = 1
                nd1_err[curr_idx] = curr_nd1_err[idx1]

             # Add measurements for instrument two. 
             if numpy.isnan(nd2[curr_idx])==False and numpy.isnan(curr_nd2_err[idx2])==False and numpy.isnan(curr_nd2[idx2])==False and numpy.isnan(curr_nd1_err[idx1])==False and numpy.isnan(curr_nd1[idx1])==False :
                nd2[curr_idx] = nd2[curr_idx] + curr_nd2[idx2]
                nd2_err[curr_idx] = nd2_err[curr_idx] + curr_nd2_err[idx2]
                N2[curr_idx] = N2[curr_idx] +1 
             if numpy.isnan(nd2[curr_idx])==True and numpy.isnan(curr_nd2_err[idx2])==False and numpy.isnan(curr_nd2[idx2])==False and numpy.isnan(curr_nd1_err[idx1])==False and numpy.isnan(curr_nd1[idx1])==False :
                nd2[curr_idx] = curr_nd2[idx2]
                nd2_err[curr_idx] = curr_nd2_err[idx2]
                N2[curr_idx] = 1           
                
             if numpy.isnan(curr_nd1[idx1])==False and numpy.isnan(curr_nd2[idx2])==False:  
                mad = mad + [curr_nd1[idx1]-curr_nd2[idx2]]
                madalt = madalt + [curr_altitude]
                mrd = mrd + [(curr_nd1[idx1]-curr_nd2[idx2])/((curr_nd1[idx1]+curr_nd2[idx2])/2)]
                mrdalt = mrdalt + [curr_altitude]
                
             k+=1 # Increment 1 km.
          
    for k in range(0,len(altitude_grid),1):
       if N1[k]!=0:
          nd1[k] = nd1[k]/N1[k]
          nd1_err[k] = nd1_err[k]/sqrt(N1[k])
       if N2[k]!=0:
          nd2[k] = nd2[k]/N2[k]
          nd2_err[k] = nd2_err[k]/sqrt(N2[k]) 
       if N1[k]!=0 and N2[k]!=0: # Do differences calculation          
          diff[k] = nd1[k] - nd2[k]
          diff_err[k] = sqrt( (nd1_err[k])**2 + (nd2_err[k])**2 )/sqrt(N1[k])
          rel_diff[k] = 100*(nd1[k] - nd2[k])/( (nd1[k] + nd2[k])/2 )
          rel_diff_err[k] = (diff_err[k]/diff[k])*rel_diff[k]
    # Now find the standard deviation of the differences at each point.
    for i in range(0,len(cm),1): # Each element contains two elements
       if type(((cm[i])[0]).common_altitude)==list and type(((cm[i])[1]).common_altitude)==list and type(((cm[i])[0]).common_o3_vmr)==list and type(((cm[i])[1]).common_o3_vmr)==list:
          curr_alt1 = list(((cm[i])[0]).common_altitude) # Current altitude range #1 
          curr_nd1 = ((cm[i])[0]).common_o3_vmr # Current VMR profile #1
          curr_alt2 = list(((cm[i])[1]).common_altitude) # Current altitude range #2
          curr_nd2 = ((cm[i])[1]).common_o3_vmr
          curr_nd1_err = cm[i][0].common_o3_vmr_error # Current VMR error profile #1
          curr_nd2_err = cm[i][1].common_o3_vmr_error 
       # Find range of altitude where O3 VMR was recorded for both instruments.
       if len(curr_nd1)!=0 and len(curr_nd2)!=0 and len(curr_alt1)!=0 and len(curr_alt2)!=0 and len(curr_nd1_err)!=0 and len(curr_nd2_err)!=0:
          for j in range(0,len(curr_nd1),1):
             if numpy.isnan(curr_nd1[j])==False:
                break
          min1 = curr_alt1[j] # Index of minimum altitude with valid O3 VMR measurement.
          for j in range(len(curr_nd1)-1,-1,-1):
             if numpy.isnan(curr_nd1[j])==False:
                break
          max1 = curr_alt1[j] # Index of maximum altitude with a valid O3 VMR measurement.
          for j in range(0,len(curr_nd2),1):
             if numpy.isnan(curr_nd2[j])==False:
                break
          min2 = curr_alt2[j] # Index of minimum altitude with valid O3 VMR measurement.
          for j in range(len(curr_nd2)-1,-1,-1):
             if numpy.isnan(curr_nd2[j])==False:
                break
          max2 = curr_alt2[j] # Index of maximum altitude with a valid O3 VMR measurement.
          minalt = float(max(min1,min2))
          maxalt = float(min(max1,max2))
          k = minalt
          while k <= maxalt:
             curr_altitude = k
             curr_idx = list(altitude_grid).index(curr_altitude) # Find the index in the grid for the current altitude. 
             idx1 = (curr_alt1).index(curr_altitude) # Find index for instrument 1 corresponding to the current altitude.
             idx2 = (curr_alt2).index(curr_altitude) # Find index for instrument 2 corresponding to the current altitude.
             if numpy.isnan(diff_stddev[curr_idx])==False and numpy.isnan(curr_nd1[idx1])==False and numpy.isnan(curr_nd2[idx2])==False  and numpy.isnan(curr_nd1_err[idx1])==False and numpy.isnan(curr_nd2_err[idx2])==False and numpy.isnan(nd1[curr_idx])==False and numpy.isnan(nd2[curr_idx])==False:
                diff_stddev[curr_idx] = diff_stddev[curr_idx] + ((curr_nd1[idx1]-curr_nd2[idx2])-(nd1[curr_idx]-nd2[curr_idx]))**2
             if numpy.isnan(diff_stddev[curr_idx])==True and numpy.isnan(curr_nd1[idx1])==False and numpy.isnan(curr_nd2[idx2])==False  and numpy.isnan(curr_nd1_err[idx1])==False and numpy.isnan(curr_nd2_err[idx2])==False and numpy.isnan(nd1[curr_idx])==False and numpy.isnan(nd2[curr_idx])==False:  
                diff_stddev[curr_idx] = ((curr_nd1[idx1]-curr_nd2[idx2])-(nd1[curr_idx]-nd2[curr_idx]))
             if numpy.isnan(rel_diff_stddev[curr_idx])==False and numpy.isnan(curr_nd1[idx1])==False and numpy.isnan(curr_nd2[idx2])==False  and numpy.isnan(curr_nd1_err[idx1])==False and numpy.isnan(curr_nd2_err[idx2])==False and numpy.isnan(nd1[curr_idx])==False and numpy.isnan(nd2[curr_idx])==False:
                rel_diff_stddev[curr_idx] =  rel_diff_stddev[curr_idx] + ((curr_nd1[idx1]-curr_nd2[idx2])/((curr_nd1[idx1]+curr_nd2[idx2])/2) - (nd1[curr_idx]-nd2[curr_idx])/((nd1[curr_idx]+nd2[curr_idx])/2) )**2
             if numpy.isnan(rel_diff_stddev[curr_idx])==True and numpy.isnan(curr_nd1[idx1])==False and numpy.isnan(curr_nd2[idx2])==False  and numpy.isnan(curr_nd1_err[idx1])==False and numpy.isnan(curr_nd2_err[idx2])==False and numpy.isnan(nd1[curr_idx])==False and numpy.isnan(nd2[curr_idx])==False:  
                rel_diff_stddev[curr_idx] = ((curr_nd1[idx1]-curr_nd2[idx2])/((curr_nd1[idx1]+curr_nd2[idx2])/2) - (nd1[curr_idx]-nd2[curr_idx])/((nd1[curr_idx]+nd2[curr_idx])/2) )**2   
                     
             k+=1 # Increment 1 km.
    for i in range(0,len(diff_stddev),1):
       if N1[i]!=0 and numpy.isnan(N1[i])==False:
          diff_stddev[i] = sqrt(diff_stddev[i]/N1[i])  # Divide by N + Square root the variances to get standard deviation.        
    fig, axs = plt.subplots(1, 3,figsize=[11, 6],sharey=True)

    axs[0].errorbar(x=list(nd1),y=list(altitude_grid),xerr=list(nd1_err),capsize=0,elinewidth=1,ecolor='red',marker='o',markerfacecolor='red',markersize=2,ls='-',color='red')
    axs[0].errorbar(x=list(nd2),y=list(altitude_grid),xerr=list(nd2_err),capsize=0,elinewidth=2,ecolor='forestgreen',marker='o',markerfacecolor='forestgreen',markersize=2,ls='-',color='forestgreen')             
    title= 'Average O3 Volume Mixing Ratio' 
    axs[0].set_title(title)
    if type(instruments)==list and len(instruments)==2 and type(instruments[0])==str and type(instruments[1])==str:
    # Check for valid axis labels.
       axs[0].legend(instruments)

    if instruments[1]=='O3sonde' and len(nd1)==len(altitude_grid) and len(nd1)==len(N1) and len(nd1)!=0:
       for i in range(0,40,2):
          if N1[i]!=0:
             axs[0].annotate( N1[i], xy=(nd1[i], altitude_grid[i]), xytext=(1.0*10**13,altitude_grid[i]))

    if instruments[1]=='DIAL' and len(nd1)==len(altitude_grid) and len(nd1)==len(N1) and len(nd1)!=0:
       for i in range(0,80,3):
          if N1[i]!=0:
             axs[0].annotate( N1[i], xy=(nd1[i], altitude_grid[i]), xytext=(1.0*10**13,altitude_grid[i]))

    if (instruments[1]=='PEARL-GBS' or instruments[1]=='UT-GBS') and len(nd1)==len(altitude_grid) and len(nd1)==len(N1) and len(nd1)!=0:
       for i in range(0,70,3):
          if N1[i]!=0:
             axs[0].annotate( N1[i], xy=(nd1[i], altitude_grid[i]), xytext=(1.0*10**13,altitude_grid[i]))

    if instruments[1]=='ACE-MAESTRO-VIS' and len(nd1)==len(altitude_grid) and len(nd1)==len(N1) and len(nd1)!=0:
       for i in range(0,100,3):
          if N1[i]!=0:
             axs[0].annotate( N1[i], xy=(nd1[i], altitude_grid[i]), xytext=(1.0*10**13,altitude_grid[i]))


    if instruments[1]=='ACE-MAESTRO-VIS':
       axs[0].set_ylim(0,105)
    if instruments[1]=='O3sonde':
       axs[0].set_ylim(0,40)
    if instruments[1]=='DIAL':
       axs[0].set_ylim(0,80)
    if instruments[1]=='UT-GBS' or instruments[1]=='PEARL-GBS':
       axs[0].set_ylim(0,70)
    axs[0].set_xlim(-0.001,0.0025)
    axs[0].set_xlabel('Average VMR [molec cm^-3]',labelpad=18)
    axs[0].set_ylabel('Altitude [km]') 

    x=[0,0] # Set up two points for a dark line to show the ideal 0 point.
    y=[0,155]  

    axs[1].plot(numpy.concatenate([numpy.array(diff) + numpy.array(diff_stddev), numpy.array(diff) - numpy.array(diff_stddev)]),list(altitude_grid)+list(altitude_grid),'--',color='dimgrey',label='Mean \u0394 ± \u03C3')
    axs[1].errorbar(x=list(diff),y=list(altitude_grid),xerr=list(diff_err),marker='o',capsize=0,elinewidth=1,ecolor='deeppink',markerfacecolor='deeppink',markersize=0,color='deeppink',label='Mean \u0394',linewidth=2)   
   # im=axs[1].hist2d(mad,madalt, bins=80, cmap='Blues')
    # cb = plt.colorbar(im, ax=axs[1])
    # cb.set_label('N',x=-0.05,y=1,rotation=0)
    axs[1].legend(['Mean \u0394', 'Mean \u0394 ± \u03C3'], bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=1, borderaxespad=1.0)
    title = 'Mean Absolute Differences ' 
    axs[1].set_title(title)
    if instruments[1]=='O3sonde':
        axs[1].set_ylim(0,40)
    if instruments[1]=='DIAL':
        axs[1].set_ylim(0,80)
    if instruments[1]=='UT-GBS' or instruments[1]=='PEARL-GBS':
        axs[1].set_ylim(0,70)
    axs[1].set_xlim(-0.003,0.007)
    axs[1].set_xlabel('Difference [molec cm^-3]',labelpad=18)
    axs[1].plot(x,y,color='black') # Iedal 0 line.
    
   # im = axs[2].hist2d(mrd,mrdalt, bins=40, cmap='Blues')
    axs[2].plot(x,y,color='black') # Iedal 0 line.    
    axs[2].plot(numpy.concatenate([numpy.array(rel_diff) + numpy.array(rel_diff_stddev),numpy.array(rel_diff) - numpy.array(rel_diff_stddev)]),list(altitude_grid)+list(altitude_grid),'--',color='dimgrey',linewidth=1)
    axs[2].errorbar(x=list(rel_diff),y=list(altitude_grid),xerr=list(rel_diff_err),marker='o',capsize=0,elinewidth=1,ecolor='deeppink',markerfacecolor='deeppink',markersize=0,color='deeppink',linewidth=2)
    title = 'Mean Relative Differences ' 
    # cb = fig.colorbar(im[3], ax=axs[2], orientation="vertical", pad=0.06)
    # cb.set_label('N')
    axs[2].set_title(title)
    if instruments[1]=='ACE-MAESTRO-VIS':
       axs[2].set_ylim(0,105)
    if instruments[1]=='O3sonde':
       axs[2].set_ylim(0,40)
    if instruments[1]=='DIAL':
       axs[2].set_ylim(0,80)
    if instruments[1]=='UT-GBS' or instruments[1]=='PEARL-GBS':
       axs[2].set_ylim(0,70)
    axs[2].set_xlim(-60,60)
    axs[2].set_xlabel('Difference [%]',labelpad=18)

    if type(instruments)==list and len(instruments)==2 and type(instruments[0])==str and type(instruments[1])==str:   
       filenamepng = title + instruments[0] + ' ' + instruments[1] +' .png' # Create name for png plot file.
    else: # If instrument strings are not given, give generic title.
       filenamepng = title + ' .png'
    if type(folder)==str and ((os.path.exists(folder))== True):
       filenamepng = folder+"/"+filenamepng  # Write path of subdirectory/filename.
    plt.savefig(filenamepng)
    plt.close()   
    return