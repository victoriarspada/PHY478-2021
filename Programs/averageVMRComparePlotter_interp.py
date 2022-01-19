# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:39:33 2020
@author: Victoria Spada
Contact: victoria.spada@mail.utoronto.ca
Last edited: Feb 17 2020.
"""
import copy
import numpy
from numpy import sqrt
from instrument import instrument
import matplotlib.pyplot as plt
import os 
import datetime
import numpy as np

# This function produces and saves a figure with 3 subplots: 
# (1) Average O3 VMR Profiles.
# (2) Mean absolute difference profiles between the two instruments.
# (3) Mean Relative difference profiles between the two isntruments
# The function takes average O3 VMR for each year for the input instruments and plots
# these profiles on a common grid and then saves the figure.
# INPUT: 
# pair: The input to this function is an 'pair' class object.
# instruments: This is a list of strings, where the strings are the two instruments involved: 
# ie, ['ACE-MAESTRO', 'DIAL']. The list must be two elements to be valid. 
# folder: String; the name of the folder in which we want to save the figure.
# OUTPUT: N/A

def averageVMRComparePlotter_interp(pair,instruments,folder,year):
    altitude_grid = numpy.arange(0,100.5,0.5) # Altitude grid for ACE-MAESTRO, length 201
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
    
    cm = pair.coincident_pairs # Extract list of coincident pairs.

    for i in range(0,len(cm),1): # Each element contains two elements
       curr_nd1=[]
       curr_nd2=[]
       curr_alt1=[]
       curr_alt2=[]
       curr_nd1_err=[]
       curr_nd2_err=[]
       if type(((cm[i])[0]).altitude)==list and type(((cm[i])[1]).altitude)==list and type(((cm[i])[0]).o3_vmr)==list and type(((cm[i])[1]).o3_vmr)==list and type(((cm[i])[0]).common_o3_vmr_error)==list and type(((cm[i])[1]).o3_vmr_error)==list and (type((cm[i])[0].is_retrieved)==list) and (type((cm[i])[1].is_retrieved)==list) and (type((cm[i])[0].is_retrieved)==list) and (type((cm[i])[1].is_retrieved)==list) and len((((cm[i])[0]).common_altitude))==201 and len((((cm[i])[1]).altitude))==201 and len((((cm[i])[0]).common_o3_vmr))==201 and len((((cm[i])[1]).o3_vmr))==201 and  len((((cm[i])[1]).is_retrieved))==201 and len((((cm[i])[0]).common_o3_vmr_error))==201 and len((((cm[i])[1]).o3_vmr_error))==201:
          
          curr_alt1 = list(((cm[i])[0]).common_altitude) # Current altitude range #1 
          curr_nd1 = ((cm[i])[0]).common_o3_vmr # Current VMR profile #1
          curr_alt2 = list(((cm[i])[1]).altitude) # Current altitude range #2
          curr_nd2 = ((cm[i])[1]).o3_vmr
          curr_nd1_err = cm[i][0].common_o3_vmr_error # Current VMR error profile #1
          curr_nd2_err = cm[i][1].o3_vmr_error 
          # curr_retrievals1 = cm[i][0].common_is_retrieved # Current retrieval documentation
          curr_retrievals2 = cm[i][1].is_retrieved
          
       # Find range of altitude where O3 VMR was recorded for both instruments.
       minalt = 0
       maxalt = 100
       k = minalt
       if len(curr_alt1)==201 and len(curr_alt2)==201:
          while k <= maxalt:
             curr_altitude = k
             curr_idx = list(altitude_grid).index(curr_altitude) # Find the index in the grid for the current altitude. 
             # Add measurements for instrument one. 
        
             idx1 = (curr_alt1).index(curr_altitude) # Find index for instrument 1 corresponding to the current altitude.
             idx2 = (curr_alt2).index(curr_altitude) # Find index for instrument 2 corresponding to the current altitude.
             if abs(curr_nd1[idx1])<1 and abs(curr_nd2[idx2])<1 and curr_retrievals2[curr_idx]==1:
                if numpy.isnan(nd1[curr_idx])==False:
                   nd1[curr_idx] = nd1[curr_idx] + curr_nd1[idx1]
                   N1[curr_idx] = N1[curr_idx] +1
                   nd1_err[curr_idx] = nd1_err[curr_idx] + curr_nd1_err[idx1]                
                if numpy.isnan(nd1[curr_idx])==True:
                   nd1[curr_idx] = curr_nd1[idx1]
                   N1[curr_idx] = 1
                   nd1_err[curr_idx] = curr_nd1_err[idx1]
                if numpy.isnan(nd2[curr_idx])==False: 
                   nd2[curr_idx] = nd2[curr_idx] + curr_nd2[idx2]
                   nd2_err[curr_idx] = nd2_err[curr_idx] + curr_nd2_err[idx2]
                   N2[curr_idx] = N2[curr_idx] +1 
                if numpy.isnan(nd2[curr_idx])==True:
                   nd2[curr_idx] = curr_nd2[idx2]
                   nd2_err[curr_idx] = curr_nd2_err[idx2]
                   N2[curr_idx] = 1         
                if numpy.isnan(diff_stddev[curr_idx])==False:
                   diff_stddev[curr_idx] = diff_stddev[curr_idx] + ((curr_nd1[idx1]-curr_nd2[idx2])-(nd1[curr_idx]-nd2[curr_idx]))**2
                if numpy.isnan(diff_stddev[curr_idx])==True:
                   diff_stddev[curr_idx] = ((curr_nd1[idx1]-curr_nd2[idx2])-(nd1[curr_idx]-nd2[curr_idx]))
                if numpy.isnan(rel_diff_stddev[curr_idx])==False:
                   rel_diff_stddev[curr_idx] =  rel_diff_stddev[curr_idx] + ((curr_nd1[idx1]-curr_nd2[idx2])/((curr_nd1[idx1]+curr_nd2[idx2])/2) - (nd1[curr_idx]-nd2[curr_idx])/((nd1[curr_idx]+nd2[curr_idx])/2) )**2
                if numpy.isnan(rel_diff_stddev[curr_idx])==True:
                   rel_diff_stddev[curr_idx] = ((curr_nd1[idx1]-curr_nd2[idx2])/((curr_nd1[idx1]+curr_nd2[idx2])/2) - (nd1[curr_idx]-nd2[curr_idx])/((nd1[curr_idx]+nd2[curr_idx])/2) )**2   
                                      
             k+=0.5 # Increment 1 km.
          
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
    for i in range(0,len(diff_stddev),1):
       if N1[i]!=0 and numpy.isnan(N1[i])==False:
          diff_stddev[i] = sqrt(diff_stddev[i]/N1[i])  # Divide by N + Square root the variances to get standard deviation.        

    # Create associated plot
    fig, axs = plt.subplots(1, 3,figsize=[11, 6],sharey=True,dpi=100)
    axs[0].plot(nd1,altitude_grid,c='red',marker='o',markersize=1)
    axs[0].plot(nd2,altitude_grid,c='forestgreen',marker='o',markersize=1)             
    axs[0].fill_betweenx(altitude_grid, np.array(nd1)-np.array(nd1_err), np.array(nd1)+np.array(nd1_err), color='mistyrose')
    axs[0].fill_betweenx(altitude_grid, np.array(nd2)-np.array(nd2_err), np.array(nd2)+np.array(nd2_err), color='lightgreen', alpha=0.5)
    title = 'Average O3 Volume Mixing Ratio' 
    axs[0].legend([instruments[0], instruments[1]],loc='upper left',fontsize=8)
    axs[0].set_title(title)
    axs[0].set_ylim(0,105)
    axs[0].set_xlim(-1e-7,5e-5)
    axs[0].set_xlabel('Average VMR [ppv]',labelpad=18)
    axs[0].set_ylabel('Altitude [km]') 
    for i in range(0,201,8):
       if N2[i]!=0 and np.isnan(N2[i])==False:
          axs[0].annotate( N2[i], xy=(3.9e-5, altitude_grid[i]), xytext=(3.9e-5,altitude_grid[i]))
    x=[0,0] # Set up two points for a dark line to show the ideal 0 point.
    y=[0,155]  
    X = numpy.concatenate([numpy.array(diff) + numpy.array(diff_stddev), numpy.array(diff) - numpy.array(diff_stddev)])
    Y = list(altitude_grid)+list(altitude_grid)
    axs[1].plot(X,Y,'--',color='dimgrey',label='Mean \u0394 ± \u03C3')
    axs[1].plot(diff,altitude_grid,linewidth=1,color='deeppink',label='Mean \u0394')   
    axs[1].plot(x,y,color='black') # Ideal 0 line.
    axs[1].fill_betweenx(altitude_grid, np.array(diff)-np.array(diff_err),np.array(diff)+np.array(diff_err),color='lightpink',alpha=0.5)   
    axs[1].legend(['Mean \u0394 ± \u03C3', 'Mean \u0394'], bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=1, borderaxespad=1.0)
    title = 'Mean Absolute Differences ' 
    axs[1].set_title(title)
    axs[1].set_xlim(-1e-5,1e-5)
    axs[1].set_ylim(0,105)
    axs[1].set_xlabel('Difference [ppv]',labelpad=18)

    axs[2].plot(x,y,color='black') # Ideal 0 line.    
    A = numpy.concatenate([numpy.array(rel_diff) + numpy.array(rel_diff_stddev),numpy.array(rel_diff) - numpy.array(rel_diff_stddev)])
    B = list(altitude_grid)+list(altitude_grid)
    axs[2].plot(A,B,'--',color='dimgrey',linewidth=1)
    axs[2].plot(rel_diff,altitude_grid,linewidth=1,color='deeppink')
    axs[2].fill_betweenx(altitude_grid, np.array(rel_diff)-np.array(rel_diff_err), np.array(rel_diff)+np.array(rel_diff_err), color='lightpink', alpha=0.5)

    title = 'Mean Relative Differences ' 
    axs[2].set_title(title)
    axs[2].set_ylim(0,105)
    axs[2].set_xlim(-300,300)
    axs[2].set_xlabel('Difference [%]',labelpad=18)
    filenamepng = title + instruments[0]+"  "+instruments[1]+', errorbars '+str(year)+'.png' # Create name for png plot file.
    fig.savefig(filenamepng) 
    
    return diff, diff_err, rel_diff, rel_diff_err