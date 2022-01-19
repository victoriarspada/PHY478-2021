# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 15:46:01 2021

@author: victo
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 15:17:59 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: Feb 18 2021
.
"""
# timeScatter
# This function takes in 4 'pair' class objects, and scatters their mean relative differences
# over the years. The figure is neither closed nor saved.
# INPUT:
# a,b,c,d: 'Pair' class objects, whose 'mean relative difference' attributes are to be plotted.
# OUTPUT: N/A
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sb
import numpy as np
from matplotlib import cm
import datetime
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def DifferencesHeatMap(pairs,title): # Input a list of pair objects
    # Given some pair objects this program will find the average difference
    # between UV and VIS measurements at each altitude slice and plot it
    # as a heatmap.
    years = np.linspace(2004,2004+len(pairs),len(pairs)) # Years included in the study
    altitudes = np.arange(0,100.5,0.5) # Altitude grid for ACE-MAESTRO
    o3_vmr_mean_absolute_diffs = []
    o3_vmr_mean_relative_diffs = []
    o3_vmr_mean_absolute_diff_errs = []
    o3_vmr_mean_relative_diff_errs = []
    C = []# Average difference of UV-VIS O3 VMR measurements as a function of altitude (RELATIVE)
    D = [] # (ABSOLLUTE)
    for i in range(0,len(pairs),1): # Cycle through each pair
        cm_pair = pairs[i]
        average_differences = np.zeros(len(altitudes))
        N = np.zeros(len(altitudes))
        # Unpack the cm_pair input pair object. 
        o3_vmr_mean_absolute_diff = cm_pair.o3_vmr_mean_absolute_diff
        o3_vmr_mean_absolute_diff_err = cm_pair.o3_vmr_mean_absolute_diff_err
        o3_vmr_mean_relative_diff = cm_pair.o3_vmr_mean_relative_diff 
        o3_vmr_mean_relative_diff_err = cm_pair.o3_vmr_mean_relative_diff_err  
    
        C = C + [cm_pair.o3_vmr_mean_relative_diff_arr]
        D = D + [cm_pair.o3_vmr_mean_absolute_diff_arr]
        o3_vmr_mean_absolute_diffs = o3_vmr_mean_absolute_diffs + [o3_vmr_mean_absolute_diff]
        o3_vmr_mean_absolute_diff_errs = o3_vmr_mean_absolute_diff_errs + [o3_vmr_mean_absolute_diff_err]
        o3_vmr_mean_relative_diffs = o3_vmr_mean_relative_diffs + [o3_vmr_mean_relative_diff]
        o3_vmr_mean_relative_diff_errs = o3_vmr_mean_relative_diff_errs + [o3_vmr_mean_relative_diff_err]
    ######
    # # Create plot of mean and relative absolute differences over the years    
    # fig0, axs = plt.subplots(1, 2,figsize=[12, 6],dpi=100)
    # axs[0].plot(np.linspace(2003,2004+len(pairs)+1,1),np.zeros(len(pairs)+2),c='black')             
    # axs[0].plot(years,o3_vmr_mean_absolute_diffs,'--k',lw=1)
    # axs[0].errorbar(years,o3_vmr_mean_absolute_diffs,o3_vmr_mean_absolute_diff_errs,c='red',marker='o',markersize=1,linestyle='None')
    # title = 'Mean Absolute Differences from 2004-2011' 
    # axs[0].set_xlim([2003,2012])
    # axs[0].set_title(title)
    # axs[0].set_xlabel('Mean Absolute Difference [ppv]',labelpad=18)
    # axs[0].set_ylabel('Year') 

    # axs[1].plot(np.linspace(2003,2004+len(pairs)+1,1),np.zeros(len(pairs)+2),c='black')             
    # axs[1].plot(years,o3_vmr_mean_relative_diffs,'--k',lw=1)
    # axs[1].errorbar(years,o3_vmr_mean_relative_diffs,o3_vmr_mean_relative_diff_errs,c='blue',marker='o',markersize=1,linestyle='None')
    # title = 'Mean Relative Differences from 2004-2011' 
    # axs[1].set_title(title)
    # axs[0].set_xlim([2003,2012])
    # axs[1].set_xlabel('Mean Relative Difference [ppv]',labelpad=18)
    # axs[1].set_ylabel('Year') 
    
    # fig0.savefig('Mean and Relative Absolute Differences Over the Years')
       
    ######
    # Create grid of differences
    differences_rel = np.array([ C[0], C[1], C[2] ]).T#, C[3], C[4], C[5], C[6], C[7], C[8]]).T
    differences_abs = np.array([ D[0], D[1], D[2] ]).T#, C[3], C[4], C[5], C[6], C[7], C[8]]).T

    fig, axs = plt.subplots(1, 2,figsize=[16, 4],dpi=100)
    fig.suptitle(title)
    axs[0].set_ylabel('Mean Relative Difference [%]')
    axs[0].set_xlabel('Date')
    axs[0].pcolor(years, altitudes, differences_rel)

    axs[1].set_ylabel('Mean Absolute Difference [ppv]')
    axs[1].set_xlabel('Date')
    axs[1].pcolor(years, altitudes, differences_abs)
    fig.autofmt_xdate()
    
    pcm_rel = axs[0].pcolor(years,altitudes,differences_rel,cmap='Spectral', vmin=-200, vmax =200)
    pcm_abs = axs[1].pcolor(years,altitudes,differences_abs,cmap='Spectral', vmin=-1e-4, vmax=1e-4)
    cbar_rel = fig.colorbar(pcm_rel, ax = axs[0])
    cbar_rel.set_label('\u0394(O3 VMR) [ppv]', rotation=270,labelpad=13)
    cbar_abs = fig.colorbar(pcm_abs, ax = axs[1])
    cbar_abs.set_label('\u0394(O3 VMR) [%]', rotation=270, labelpad=13)
    
    name = title+' Meshgrid .png'
    fig.savefig(name)
    return 

def O3VMRHeatMap(o3_vmr,dates,retrievals,lat,long,year,uvvis): 
    # Given an array of O3 VMR measurements as functions of altitude and their associated
    # dates, this function plots the measurements as a heatmap. 
    # Input
    # o3_vmr, dates retrievals
    altitudes = np.arange(0,100.5,0.5) # Altitude grid for ACE-MAESTRO
    latitudes = np.arange(-90,100,10) # Spacing of laitutde
    months = []
    for i in range(0,len(dates),1):
        months = months + [int(dates[i].month)]
    colorbar_tags = ['Jan.','Feb.','Mar.','Apr.','May','June','July','Aug.','Sept.','Oct.','Nov.','Dec.']
    o3_values = np.multiply(o3_vmr, retrievals)
 
    # Create grid of O3 VMR Measurements
    fig3, ax3 = plt.subplots(1, 1,figsize=[7, 4],sharey=True)
    title = 'ACE-MAESTRO O3 VMR measurements from '+str(year)
    ax3.set_title(title,pad=15)
    ax3.set_ylabel('O3 VMR [ppv]')
    ax3.set_xlabel('Date')
    pcm = ax3.pcolor(dates,altitudes,o3_values,cmap='twilight',vmin=0, vmax=1e-5)
    fig3.autofmt_xdate()
    # ax3.set_xlim([datetime.datetime(int(year),1,1),datetime.datetime(int(year),12,31)])
    fig3.colorbar(pcm).set_label('O3 VMR [ppv]', rotation=270,x=1.5,labelpad=13)
    name3 = 'O3 VMR Measurements, ACE-MAESTRO '+str(uvvis)+', '+str(year)+'.png'
    fig3.savefig(name3)
    
    return 