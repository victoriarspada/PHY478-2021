# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 19:44:52 2021

@author: Victoria R Spada
"""

import numpy as np
from measurement import *
from scipy import interpolate 
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib.colors as colors
import pickle 
import matplotlib as mpl
from linear_trend import *
from deseasonalise import *
    
phase_shift = np.pi/4

def qbo_osc_linear_trend(x,y_err,y,l):
    # Input column vectors for x and y, and the column vector that is the associated error with x.
    # x: datenum (month number)
    # y: monthly averaged quantity
    # y_err: associated error for y
    # Create square covariance matrix (only non-zero on diagonals)
    y_err_reduced, y_reduced, x_reduced = y_err, y, x
    S = np.diag(y_err_reduced)
    try:
        Si = np.linalg.inv(S)
    except:
        out = np.zeros(2*len(l))
        out[:] = np.nan
        return out
    e = np.ones(np.size(x_reduced))    
    # Create cosine and sine vectors for the given period lengths
    sin_vectors, cos_vectors = [], []
    for i in range(0,len(l),1):
        frequency = 2*np.pi/l[i]
        sin_vectors = sin_vectors + [np.sin(frequency*x_reduced - phase_shift)]
        cos_vectors = cos_vectors + [np.cos(frequency*x_reduced - phase_shift)]    
    # Now ready to start constructing T matrix
    nvars = 2*len(l) # 2 linear terms + a cosine and sine term for each frequency
    T = np.zeros( (nvars, nvars) )
    # Do first row: corresponds to 'a', the constant term
    T[0,0] = 2*np.matmul( sin_vectors[0], np.matmul(Si, sin_vectors[0]) )
    T[0,1] = 2*np.matmul( sin_vectors[0].T, np.matmul(Si, cos_vectors[0].T))
    T[1,0] = 2*np.matmul( cos_vectors[0].T, np.matmul(Si, sin_vectors[0]) )
    T[1,1] = 2*np.matmul( cos_vectors[0].T, np.matmul(Si, cos_vectors[0]) )
    # Create q vector     
    q = np.zeros(nvars)    
    q[0] = 2*np.matmul( sin_vectors[0].T, np.matmul( Si, y_reduced) )
    q[1] = 2*np.matmul( cos_vectors[0].T, np.matmul( Si, y_reduced) )
    # Now solve for parameters: T*Params = q
    # print('\n',T,'\n')
    try:
        params = np.linalg.solve(T, q)
        return params
    except:
        out = np.zeros(nvars)
        out[:] = np.nan
        return out


filenamedat = 'singapore.dat.txt'
f=open(filenamedat,'r') # Open and read the data file.
lines = f.readlines()
needed_lines = lines[299:len(lines)]

hpa = np.array([10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100])
winds = np.zeros((17,15,12))
winds_timeseries = np.zeros((15, 17*12))
for i in range(0,300,1):
    if needed_lines[i]=="2021":
        skip=True
    elif len(needed_lines[i])==5:
        curr_year = int(needed_lines[i])
        skip=True
    elif needed_lines[i][0:3]=='hPa' and needed_lines[i]!="2021":
        for j in range(1,16,1):
            curr_line = needed_lines[i+j]
            b = []
            for t in curr_line.split():
                try:
                    b.append(float(t))
                except ValueError:
                    pass
            if len(b)>0: 
                b=b[1:len(b)]
                winds[curr_year-2004, j-1, :] = np.array(b)

winds = winds/0.1 # convert to m/s                

winds_timeseries = winds[0,:,:]
for i in range(1,17,1): # Through each year
    winds_timeseries = np.concatenate((winds_timeseries, winds[i,:]),axis=1)

# Try subtracting the average to bring the time series to a 0 y shift 
for i in range(0,15,1): # for each pressure slice
    winds_timeseries[i,:] = winds_timeseries[i,:] - np.mean(winds_timeseries[i,:]) 

name = 'singapore.pickle'
a = {'hPa' : hpa,
     'wind' : winds }
pickle_out = open(name,"wb")
pickle.dump(a, pickle_out)
pickle_out.close()
pickle_in = open(name,"rb")
open_meas = pickle.load(pickle_in) # Open the infoarray pickle file for this year

fig2, ax2 = plt.subplots(4, 5,figsize=[26, 17])
title = 'Singapore Winds'
fig2.suptitle(title,fontsize=30,y=0.93)
months=np.linspace(1,12,12)
for i in range(0,17,1):
    if i==0 or i==1 or i==2 or i==3 or i==4:
        j=0
        idx=i
    if i==5 or i==6 or i==7 or i==8 or i==9:
        j=1
        idx=i-5
    if i==10 or i==11 or i==12 or i==13 or i==14:
        j=2
        idx=i-10
    if i==15 or i==16:
        j=3
        idx=i-15
    ax2[j,idx].set_yticks(np.linspace(10,100,10))
    ax2[j,idx].set_ylabel('Pressure [hPa]',fontsize=15)
    ax2[j,idx].xaxis.grid()
    ax2[j,idx].set_xlim([1,12])
    ax2[j,idx].set_ylim([10,100])
    ax2[j,idx].set_xticks(np.linspace(1, 12, 12))
    ax2[j,idx].set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'])    
    ax2[j,idx].set_title(title,pad=2)
    ax2[j,idx].set_title(str(2004+i),fontsize=15)
    ax2[j,idx].yaxis.grid()
    h = np.flip(hpa)
    w = winds[i,:,:]
    for a in range(0,15,1):
        w[a,:] = np.flip(w[a,:])
    pcm1 = ax2[j,idx].pcolor(months, hpa, winds[i,:,:], cmap='jet', vmin=-4200, vmax=2500)
ax2[3,2].axis('off')
ax2[3,3].axis('off')
ax2[3,4].axis('off')

cax = plt.axes([0.46, 0.2, 0.4, 0.04])
sm = plt.cm.ScalarMappable(cmap='jet', norm=plt.Normalize(vmin=-4200, vmax=2500))
cbar=plt.colorbar(sm,cax,orientation='horizontal')
cbar.set_ticks([-4000,-3000,-2000,-1000,0,1000,2000])
cbar.set_ticklabels(['-4000','-3000','-2000','-1000','0','1000','2000'])
cbar.ax.tick_params(labelsize='large')
cbar.set_label('Wind Speed [m/s]',fontsize=20,labelpad=10)

fig2.savefig('singapore.png')

# months = np.linspace(1,204,204)
# heights = np.array([8340.4, 7070.7 ])
# for i in range(0,11,1): # Cycle through each hPa value
#     print(hpa[i])
#     l=28
#     params = qbo_osc_linear_trend( months ,  np.ones(len(months))*10, winds_timeseries[i,:], [l])
#     c,d = 1.7*params[0], 1.7*params[1]
#     trend = c*np.sin( 2*np.pi*months/l - phase_shift) + d*np.cos(2*np.pi*months/l - phase_shift)
#     fig = plt.figure(figsize=(6, 3.5)) 
#     gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1.25]) 
#     fig.suptitle('Singapore wind trend '+str(hpa[i])+' hPa',y=1.01)
#     ax0 = plt.subplot(gs[0])
    
#     ax0.plot(months, winds_timeseries[i,:], color='blue', markeredgecolor='blue')            
#     ax0.plot( months, trend, color='green', linestyle='--')
#     ax0.set_ylabel('VMR [ppv]')
#     ax0.set_xticks(np.arange(0, 204, step=12))
#     ax0.set_xticklabels(['','','','','','','','',''])
#     ax0.xaxis.set_minor_locator(MultipleLocator(1))
#     ax0.xaxis.grid()
#     ax0.set_xlim([0,204])
           
#     ax1 = plt.subplot(gs[1])
#     ax1.plot(np.linspace(0,300,10), np.zeros(10), linestyle='--', color='grey')
#     ax1.plot( months, winds_timeseries[i,:] - trend, linestyle='-', color='orangered' )
#     ax1.set_ylabel('Wind Speed [m/s]')
#     ax1.set_xlabel('Year',fontsize=19)
#     ax1.set_xticks(np.arange(0, 204, step=48))
#     ax1.set_xticklabels(['2004','2008','2012','2016','2020'])
#     ax1.xaxis.set_minor_locator(MultipleLocator(1))
#     ax1.xaxis.grid()
#     yabs_max = abs(max(ax1.get_ylim(), key=abs))
#     ax1.set_ylim(ymin=-yabs_max, ymax=yabs_max)
#     ax1.set_xlim([0,204])
    
#     plt.tight_layout()
         
         