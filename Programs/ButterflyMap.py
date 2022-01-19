# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:17:21 2021

@author: Victoria R Spada
Last Edit: Feb 28 2021
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sb
import numpy as np
from matplotlib import cm
import datetime
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def ButterflyMap(o3_vmr,dates,lat,year,uvvis):
    # Create butterfly plot of O3 VMR Measurements
    fig, ax = plt.subplots(1, 1,figsize=[7, 4],sharey=True)
    ax.grid(linestyle="--", color='grey')
    title = 'ACE-MAESTRO O3 VMR measurements from '+str(year)
    ax.set_title(title)
    ax.set_ylabel('Latitude [°]')
    ax.set_xlabel('Date')
    ax.scatter(dates,lat,marker='o',c='red',s=5)
    fig.autofmt_xdate()
    ax.set_ylim([-90,90])
    ax.set_yticks(np.arange(-90, 90, 10))
    ax.set_xlim([datetime.datetime(int(year),1,1),datetime.datetime(int(year),12,31)])
    name = 'Butterfly map of O3 VMR Measurements, ACE-MAESTRO '+str(uvvis)+', '+str(year)+'.png'
    fig.savefig(name)
    return 
    
def WorldMap(o3_vmr,dates,lat,long,year,uvvis): 
    # Given an array of O3 VMR measurements as functions of altitude and their associated
    # dates, this function plots the measurements as a heatmap. 
    # Input
    # o3_vmr, dates retrievals
    altitudes = np.arange(0,100.5,0.5) # Altitude grid for ACE-MAESTRO
    months = []
    for i in range(0,len(dates),1):
        months = months + [int(dates[i].month)]
    colorbar_tags = ['Jan.','Feb.','Mar.','Apr.','May','June','July','Aug.','Sept.','Oct.','Nov.','Dec.']

    # Create map showing measurements throughout the year
    fig4, ax4 = plt.subplots(1, 1,figsize=[8, 4],sharey=True)
    title = 'Location of ACE-MAESTRO in '+str(year)
    ax4 = plt.axes(projection=ccrs.PlateCarree())
    ax4.set_global()
    ax4.set_title(title)
    ax4.coastlines()
    #ax4.scatter(lat, long,marker='o')  # didn't use transform, but looks ok...
    df=pd.DataFrame(data={'A':long,'B':lat,'C':months})
    points = ax4.scatter(df.A, df.B, c=df.C, cmap=plt.cm.get_cmap('jet', 12), vmin=1, vmax=12, lw=0, s=5)
    cbar = fig4.colorbar(points)
    cbar.set_label('Month', rotation=270,labelpad=13)
    cbar.set_ticks([1,2,3,4,5,6,7,8,9,10,11,12])
    cbar.set_ticklabels(colorbar_tags)
    
    gl = ax4.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    
    name4 = 'Measurements on map, '+str(uvvis)+', '+str(year)+'.png'
    fig4.savefig(name4)
    return 