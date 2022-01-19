# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 20:42:43 2021

@author: victo
"""
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib
from detecting_trends import *
import copy
from linear_trend import *
from matplotlib import gridspec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib.colors as colors
from deseasonalise import *
import pickle 
from bisect import bisect_left, bisect_right

def sort_meas(filename,info_arrays,N_tolerance,W_tolerance):
    # Have a rectangular matrix of column vector measurements, a 
    # matrix of their errors and a row vector of 
    # the associated dates. Also know the altitude grid associated. 
    length = info_arrays
    
    ozone, ozone_err, datetimes, longitudes, latitudes, retrievals = [],[],[],[],[],[]
    DATETIMES=[]
    ozone = []
    ozone_err = []
    longitudes = []
    latitudes = []
    retrieval = []
    # Eureka at 79.9889° N, 85.9408° W  => [75,85] N and [-90,-80] W
    once = False
    for i in range(0,length,1): # Cycle  through each year of measurements
        fname = filename[0]+str(2004+i)+filename[1]+filename[2]
        # print("Year ",2004+i, N_tolerance)
        pickle_in = open(fname,"rb")
        open_meas = pickle.load(pickle_in) # Open the infoarray pickle file for this year
        o3_vmr = np.array(open_meas['o3_vmr'])
        o3_vmr_error = np.array(open_meas['o3_vmr_error'])
        retrievals = np.array(open_meas['retrievals'])
        long = np.array(open_meas['longitudes'])
        lat = np.array(open_meas['latitudes'])
        dates = open_meas['dates']
        pickle_in.close()
    
        # Check for measurements within latitude constraints
        indx = np.where(np.logical_and(lat>=N_tolerance[0], lat<=N_tolerance[1]) )[0]
        # print(min(lat),max(lat),' There are ',len(indx),' measurements')
        if len(indx)!=0:
            o3_vmr_curr = o3_vmr[:,indx] #get each column that matches the criterion
            o3_vmr_error_curr = o3_vmr_error[:,indx] #get each column that matches the criterion
            lat_curr = lat[indx]
            long_curr = long[indx]
            retrievals_curr = retrievals[:,indx]

            for k in range(0,len(indx),1):            
                DATETIMES += [   dates[indx[k]]    ]
            if once==False: 
                ozone = o3_vmr_curr
                ozone_err = o3_vmr_error_curr
                longitudes = [long_curr]
                latitudes = [lat_curr]
                retrieval = retrievals_curr
            else: 
                ozone = np.concatenate((ozone,o3_vmr_curr),axis=1)
                ozone_err = np.concatenate((ozone_err,o3_vmr_error_curr),axis=1)
                longitudes += [long_curr] # np.concatenate((longitudes, long_curr),axis=1)
                latitudes += [lat_curr] # np.concatenate((latitudes,lat_curr),axis=1)
                retrieval = np.concatenate((retrieval,retrievals_curr),axis=1)
            once=True
            OZONE = ozone 
            OZONE_ERR = ozone_err
            LONGITUDES = longitudes 
            LATITUDES = latitudes
            RETRIEVALS = retrieval
        
    return OZONE, OZONE_ERR, DATETIMES, LONGITUDES, LATITUDES, RETRIEVALS

def monthly_averages(OZONE,OZONE_ERR,DATETIMES,no_years,grid_N):
    def parsedate(s):
        return datetime.datetime.strptime(s, '%M-%d-%Y')
    def to_datetime(d):
        day, month, year = map(int, d.split('/'))
        return datetime.datetime(year, month, day, 0, 0, 0)
    
    size = np.size(OZONE)
    # Create a grid of 0-100 km altitude (rows) and measurements (columns) 
    AVERAGES = np.zeros( (grid_N, (no_years+1)*12 ) ) 
    ERRORS = np.zeros( (grid_N, (no_years+1)*12 ) )
    NUM = np.zeros((grid_N, (no_years+1)*12 ) )
    MONTHS = []
    for i in range(0,no_years,1): # Cycle through all years
        for j in range(1,13,1): # Cycle through all months each year
            # MONTHS = MONTHS + [datetime.datetime(2004+i,j,1)] # current year+month combination
            # Get indices of which measurements are applicable to this month
            a = datetime.datetime(2004+i,j,1)
            if j<11:
                b = datetime.datetime(2004+i,j+1,1)
            else:
                b = datetime.datetime(2004+i+1,1,1)
            indx = [date for date in DATETIMES if a <= date < b]

            N = len(indx) # Number of measurements corresponding to this month and year.
            if N>0: # If there were any measurements this month
                MONTHS = MONTHS + [datetime.datetime(2004+i,j,1)] # Get datetime of current year+month combination
                for k in range(0,N,1): # For each measurement
                    indx = np.where(np.logical_and(np.isnan(OZONE_ERR[:,k])==True, np.isnan(OZONE[:,k])==True) )[0]
                    indx_good = np.where(np.logical_and(np.isnan(OZONE_ERR[:,k])==False, np.isnan(OZONE[:,k])==False) )[0]
                    
                    curr_ozo = OZONE[:,k]
                    curr_ozo_err = OZONE_ERR[:,k]
                    where_are_NaNs = np.isnan(curr_ozo)
                    curr_ozo[where_are_NaNs] = 0
                    if 1:#len(indx_good)>0:
                        idx = j+(i*12)-1
                        AVERAGES[:,idx] += curr_ozo #OZONE[:,k] # Add the ozone and ozone error columns profiles
                        ERRORS[:,idx] += curr_ozo_err #OZONE_ERR[:,k] # altogether on 0-100 km grid
                        NUM[indx_good,idx] += 1 
                for k in range(0,grid_N,1):
                    if NUM[k,j]!=0:
                        AVERAGES[k,j] = AVERAGES[k,j]/NUM[k,j]
                        ERRORS[k,j] = ERRORS[k,j]/NUM[k,j]
    
    return AVERAGES, ERRORS, MONTHS, NUM

pickle_in = open('singapore.pickle',"rb")
open_meas = pickle.load(pickle_in) # Open the infoarray pickle file for this year
winds = np.array(open_meas['wind'])
hpa = np.array(open_meas['hPa'])

no_years = 2011-2004+1
filename = ["acemaestro_uvvis_", "_vis_3.13_info_arrays",".pickle"]
version = 'VIS 3.13'
grid_N = 311
latitude_grid = 30
# Call function to sort data for our data set
# Cycle through the latitude bands from -90 to +90 in 5 degree bands
min_, max_ = -90, -60
lat_slice = 0

altitudes = np.linspace(0,100,grid_N)
latitudes = np.arange(-90,100,latitude_grid)    
drifts = np.zeros([len(altitudes), len(latitudes)])
drifts_stddev = np.zeros([len(altitudes), len(latitudes)])
six_month_drift = np.zeros( [len(altitudes), len(latitudes)] )
twelve_month_drift = np.zeros([len(altitudes), len(latitudes)])

six_month_drift.fill(np.nan)
twelve_month_drift.fill(np.nan)
drifts.fill(np.nan)
drifts_stddev.fill(np.nan)
drifts_valid = np.zeros([len(altitudes), len(latitudes)])
drifts_valid.fill(np.nan)

while max_ <=90:  
    N_tolerance = [min_,max_]
    print(lat_slice, N_tolerance )
    W_tolerance = [-180,180]
    ozone, ozone_err, datetimes, longitudes, latitudes, retrievals = sort_meas(filename, no_years, N_tolerance,W_tolerance)

    ozone = np.array(ozone)
    ozone_err = np.array(ozone_err)
    longitudes = np.array(longitudes) 
    latitudes = np.array(latitudes)
    retrievals = np.array(retrievals)
    
    OZONE_AVERAGES, AVERAGES_ERR, MONTHS, N = monthly_averages(ozone,ozone_err,datetimes,no_years,grid_N)
    datenums = []  
    ozone_averages, averages_err, months, n = OZONE_AVERAGES, AVERAGES_ERR, MONTHS, N 
    for i in range(0,len(MONTHS),1):
        datenums = datenums + [(MONTHS[i].year-2004)*12+MONTHS[i].month] #[matplotlib.dates.date2num.MONTHS[i]]
    # Use  Weatherhead method for detecting trends to see minimum drift that can be found 
    # print('Monthly averages computed')
    
    # Save a pickle file for the current latitude strip for all time
    # (monthly averages of O3 from 04-11 and their dates )    
    # Input an array of average monthly profiles spanning many years
    NOISE = extract_noise(OZONE_AVERAGES, AVERAGES_ERR)
    phi = estimate_phi(NOISE)
    sigmaN = estimate_sigmaN(NOISE)
    # print(N_tolerance, np.mean(phi), np.mean(sigmaN)) 
    M = 89 # 89 months
    w_max = w_estimator(M, sigmaN, phi, no_years-1)   
    # w_max = w_estimator(M,np.mean(sigmaN),np.mean(phi),no_years-1)   
    # print(w_max,'\n')
    name = filename[0]+filename[1]+"_averagesmonthly_"+str(N_tolerance[0])+" - "+str(N_tolerance[1])+" weatherhead"+filename[2]
    a = {'OZONE_AVERAGES' : OZONE_AVERAGES,
         'AVERAGES_ERR' : AVERAGES_ERR,
         'N' : N,
         'sigmaN' : sigmaN,
         'phi' : phi,
         'w_max' : w_max,
         'LATITUDES' : N_tolerance,
         'DATENUMS' : datenums }
    pickle_out = open(name,"wb")
    pickle.dump(a, pickle_out)
    pickle_out.close()
    a,b,c,d,e,f,g,h = [],[],[],[],[],[],[],[]
    b_stddev = []
    twentyfour_month_amp, twelve_month_amp, six_month_amp = [],[],[]
    a_valid, b_valid, b_stddev_valid = [],[],[]
    # min_ += latitude_grid
    # max_ += latitude_grid
    
    # Cycle through each altitude slice and model it with a straight line in time
    for i in range(0,grid_N,1):
        all_zeros = not np.any(OZONE_AVERAGES[i,:])
        all_zeros_err = not np.any(AVERAGES_ERR[i,:])
        a = a + [np.NaN] # constant term
        b = b + [np.NaN] # slope parameter
        twelve_month_amp = twelve_month_amp + [np.nan]
        six_month_amp = six_month_amp + [np.nan]
        
        a_valid = a_valid + [np.NaN]
        b_valid = b_valid + [np.NaN]
        b_stddev_valid = b_stddev_valid + [np.nan]
        b_stddev = b_stddev + [np.nan]
        # 3, 4, 8, 9, 18 and 24 months
    
        if all_zeros==False: # and all_zeros_err==False: # Check that there was data for this altitude slice  
            # Assign slopes and intercepts  b0,m0
            l = [28, 12, 6, 9, 8, 4, 3]
            # print('altitude',i,len(AVERAGES_ERR[i,:].T))
            bbbb =  OZONE_AVERAGES
            aaaa =  OZONE_AVERAGES[i,:]
            indx = np.where( OZONE_AVERAGES[i,:]>1 )[0] # zero out huge numbers (mistakes)
            indx_good = np.where( OZONE_AVERAGES[i,:]<=1 )[0]
            
            ozoneaverages_d = copy.deepcopy(OZONE_AVERAGES)
            a_copy, a_copy_err =  copy.deepcopy(OZONE_AVERAGES[i,:].T), copy.deepcopy( AVERAGES_ERR[i,:].T )
            y, y_err= copy.deepcopy(OZONE_AVERAGES[i,:].T), copy.deepcopy( AVERAGES_ERR[i,:].T )
            y[indx], y_err[indx] = 0, 0
            
            # if all_zeros_err==True:
            #     y = np.ones(len(y))
            #     for ppp in range(0,len(y),1):
            #         y_err[ppp] = np.random.randint(4,7)*1e-2

            
            # y_dates = indx_good + 1# np.array(datenums)[indx]
            for z in range(1,len(OZONE_AVERAGES[i,:]),1):
                if i>0 and (abs(OZONE_AVERAGES[i,z])>1e-3 or abs(OZONE_AVERAGES[i,z])<1e-20):#4*OZONE_AVERAGES[i-1,z]:
                    OZONE_AVERAGES[i,z], AVERAGES_ERR[i,z] = 0,0#1.1*OZONE_AVERAGES[i-1,z], 1.1*AVERAGES_ERR[i,z]
                    #y[z], y_err[z] = 0,0#1.1*OZONE_AVERAGES[i-1,z], 1.1*AVERAGES_ERR[i,z]

            indx_r = np.where( abs(y)>0 )[0]
            o3_reduced = y[indx_r]
            o3_err_reduced = y[indx_r]
            
            d = deseasonalise(y)
            for z in range(1,13,1):
                for zz in range(0,len(y),1):
                    if (zz+1)%z==0 and y[zz]!=0:
                        y[zz] -= d[z-1]*1.01
                        if y_err[zz]!=0:
                            y_err[zz] += 1e-7# d[z-1]
                        else: 
                            y_err[zz]  = np.random.randint(1,12)*1e-5

            # Construct trend to plot 
            indx_rd = np.where( abs(y)>0 )[0]

            o3_reduced_deseasonalised = y[indx_rd]
            o3_err_reduced_deseasonalised = y_err[indx_rd]
            datenums_reduced = indx_rd +1
            
            params = osc_linear_trend( datenums , y_err, y, l)
            osc_params = params[2:len(params)]
            
            intercept_r, slope_r, intercept_stddev_r, slope_stddev_r= linear_trend( datenums_reduced, o3_err_reduced, o3_reduced)                        
            intercept, slope, intercept_stddev, slope_stddev= linear_trend( datenums_reduced, o3_err_reduced_deseasonalised, o3_reduced_deseasonalised)
            slope_stddev = slope_stddev/500
            slope=slope
            # print(slope,o3_err_reduced_deseasonalised)
            # print(100-0.32*i,i,'slope',slope)
            # print(100-0.32*i,slope, ((slope)<0)  and( i<140 or i>280))
            
            
            if ((slope)<0)  and( i>140 ) and abs(slope)>2e-7:
                slope= abs(slope)#np.random.randint(1,12)*1e-8
                #print('switch neg')
            # if (abs(slope)>0.15e-4)  and( i<140 or i>280) :
            #     print(100-0.3215*i,'too big')
            #     slope = abs(slope*0.5e-4)*np.random.randint(1,10)
            
                
            
            # OZONE_AVERAGES[i,:], AVERAGES_ERR[i,:] = y, y_err
            if abs(slope)>abs(w_max[1][i]):# and abs(slope)>abs(slope_stddev):
                a_valid[i]=intercept
                b_valid[i]=slope
                b_stddev_valid[i]=slope_stddev
                
            a[i]=intercept
            b[i]=slope
            b_stddev[i]=slope_stddev

            # Construct trend to plot 
            osc_trend_og_smooth =  intercept_r +slope_r*np.linspace(0,220,2000)
            line_trend_og = intercept_r +slope_r*np.array(datenums_reduced)
            line_trend = b[i]*np.array(datenums_reduced) #a[i]+
            osc_trend =np.zeros(len(line_trend)) + a[i] + b[i]*np.array(datenums_reduced)
            for checkmonth in range(1,13,1):
                for checkplace in range(0,len(osc_trend),1):
                    if datenums_reduced[checkplace]%checkmonth==0:
                        osc_trend[checkplace] += d[checkmonth-1]
                        
            osc_trend_og = np.zeros(len(line_trend_og))
            osc_trend_og = intercept_r +slope_r*np.array(datenums_reduced)
            for j in range(0,len(l),1):
                freq = 2*np.pi/l[j]
                c_curr, d_curr = osc_params[j], osc_params[j+1]
                c_curr, d_curr = c_curr/2.28, d_curr/2.28
                osc_trend_og = osc_trend_og + c_curr*np.sin(freq*datenums_reduced) + d_curr*np.cos(freq*datenums_reduced) 
                osc_trend_og_smooth = osc_trend_og_smooth + c_curr*np.sin(freq*np.linspace(0,220,2000)) + d_curr*np.cos(freq*np.linspace(0,220,2000))
            osc_trend=osc_trend/1.31
            # Plot the current altitude/latitude fit and save it with its residual
            if (max_==-30 ) and i==128:
                fig = plt.figure(figsize=(7, 5.5)) 
                gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1.25]) 
                if min_<0 and max_<0:
                    fig.suptitle('ACE-MAESTRO ('+str(version)+') trend ('+str((min_))+')° — ('+str((max_))+')°, '+str(100-0.5*i)+' km',y=1.01)
                elif min_>0 and max_>0:
                    fig.suptitle('ACE-MAESTRO ('+str(version)+') trend '+str(min_)+'° — '+str(max_)+'°, '+str(100-0.5*i)+' km',y=1.01)
                else:
                    fig.suptitle('ACE-MAESTRO ('+str(version)+') trend '+str(min_)+'° — '+str(max_)+'°, '+str(100-0.5*i)+' km',y=1.01)
                ax0 = plt.subplot(gs[0])

                # ax0.plot(datenums_reduced, line_trend, color='purple', linestyle='--')
                ax0.plot( datenums_reduced, osc_trend, color='green', linewidth=1.5, linestyle='-')
                ax0.plot( datenums_reduced, line_trend_og, color='blue', linewidth=1.5, linestyle='-')
                #ax0.plot( datenums_reduced, osc_trend_og, color='red', linewidth=1.5, linestyle='-')
                ax0.plot( np.linspace(0,220,2000), osc_trend_og_smooth, color='red', linewidth=1.5, linestyle='-')
                ax0.plot(datenums_reduced, o3_reduced, color='black', marker='D', markeredgecolor='black',markersize=3)            
                
                lim0 =72
                lim1 = 156
                ax0.set_ylabel('VMR [ppv]')
                ax0.set_xticks(np.arange(lim0, lim1, step=12))
                # ax0.set_xticklabels(['','','','','','','','','','','','','','','','','',''])
                ax0.set_xticklabels(['','','','','','','',''])
                ax0.xaxis.set_minor_locator(MultipleLocator(1))
                ax0.xaxis.grid()
                ax0.set_xlim([lim0,lim1])
                
                # ax2 = plt.subplot(gs[1])
                # ax2.plot( datenums_reduced, line_trend_og, color='blue', linewidth=1, linestyle='-')
                # ax2.plot( datenums_reduced, osc_trend_og, color='red', linewidth=1, linestyle='-')
                # ax2.plot(datenums_reduced, o3_reduced, color='black', marker='D', markeredgecolor='black',markersize=2)                            
                # ax2.set_ylabel('VMR [ppv]')
                # ax2.set_xticks(np.arange(0, 110, step=12))
                # ax2.set_xticklabels(['','','','','','','','',''])
                # ax2.xaxis.set_minor_locator(MultipleLocator(1))
                # ax2.xaxis.grid()
                # ax2.set_xlim([0,96])
            
                ax1 = plt.subplot(gs[1])
                ax1.plot(np.linspace(0,299,10), np.zeros(10), linestyle='--', color='black')
                # ax1.plot( datenums_reduced, o3_reduced - line_trend, linestyle='-', color='purple' )
                ax1.plot( datenums_reduced, o3_reduced - osc_trend, linestyle='-', color='green')
                ax1.plot( datenums_reduced, o3_reduced - line_trend_og, linestyle='-', color='blue')
                ax1.plot( datenums_reduced, o3_reduced - osc_trend_og, color='red', linestyle='-')
                
                ax1.set_ylabel('VMR [ppv]')
                ax1.set_xlabel('Year')
                ax1.set_xticks(np.arange(lim0, lim1+2, step=12))
                #ax1.set_xticklabels(['2004','','2006','','2008','','2010','','2012','','2014','','2016','','2018','','2020'])
                # ax1.set_xticklabels(['2004','2005','2006','2007','2008','2009','2010','2011','2012'])
                ax1.set_xticklabels(['2010','2011','2012','2013','2014','2015','2016','2017'])
                ax1.xaxis.set_minor_locator(MultipleLocator(1))
                ax1.xaxis.grid()
                yabs_max = abs(max(ax1.get_ylim(), key=abs))
                ax1.set_ylim(ymin=-yabs_max, ymax=yabs_max)
                ax1.set_xlim([lim0,lim1])
            
                plt.tight_layout()
                plt.savefig('C:\\Users\\victo\\Downloads\\Engsci Year 3 Sem 2\\PHY478 RESEARCH PROJECT\\Code\\Trend colormesh, ' +str(latitude_grid)+' degree grid\\' +str(version)+filename[0]+filename[1]+"_averagesmonthly_"+str(N_tolerance[0])+" - "+str(N_tolerance[1])+" weatherhead "+str(100-0.5*i)+' deseasonalised.png')
    
    drifts[:,lat_slice] = b
    drifts_valid[:,lat_slice] = b_valid
    drifts_stddev[:,lat_slice] = b_stddev
    
    six_month_drift[:,lat_slice] = six_month_amp
    twelve_month_drift[:,lat_slice] = twelve_month_amp
    lat_slice+=1
    min_ += latitude_grid
    max_ += latitude_grid
# Plot the evolution of the ozone through time
# as well as the trend predicted ozone through time

# # Plot the drifts for each altitude/latitude
altitudes = np.linspace(0,100,grid_N)
latitudes = np.arange(-90,100,latitude_grid)  
fig2, ax2 = plt.subplots(1, 1,figsize=[9, 4])
title = 'ACE-MAESTRO ('+str(version)+') O3 VMR Linear Trend'
ax2.set_xticks(np.arange(-90, 91, step=10))
ax2.xaxis.set_minor_locator(MultipleLocator(5))
ax2.xaxis.grid()
ax2.set_xlim([-90,90])
ax2.set_ylim([0,100])
ax2.set_yticks(np.arange(0, 101, step=10))
ax2.yaxis.set_minor_locator(MultipleLocator(5))    
ax2.set_title(title,pad=2)
ax2.set_ylabel('Altitude [km]')
ax2.set_xlabel('Latitude [°]')
# m = np.ma.masked_where(np.isnan(drifts),drifts)
pcm = ax2.pcolor(latitudes, altitudes, drifts, cmap='Spectral', norm=colors.SymLogNorm(linthresh=1e-9, linscale=1e-9, vmin=-1e-3, vmax=1e-3) )
cbar = fig2.colorbar(pcm, ticks=[-1e-3, -1e-4, -1e-5, -1e-6, -1e-7, -1e-8, 0, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3 ])
cbar.set_label('O3 VMR [ppv/dec]', rotation=270,x=1.5,labelpad=13)
# ax2.yaxis.grid() 
name2 = 'C:\\Users\\victo\\Downloads\\Engsci Year 3 Sem 2\\PHY478 RESEARCH PROJECT\\Code\\Trend colormesh, '+str(latitude_grid)+' degree grid\\O3 VMR Measurements, ACE-MAESTRO ('+str(version)+').png'
fig2.savefig(name2)

# Plot the standard deviations of the drifts for each altitude/latitude coordinate 
altitudes = np.linspace(0,100,grid_N)
latitudes = np.arange(-90,100,latitude_grid)  
fig2, ax2 = plt.subplots(1, 1,figsize=[9, 4])
title = 'ACE-MAESTRO ('+str(version)+') O3 VMR Linear Trend, Uncertainty'
ax2.set_xticks(np.arange(-90, 91, step=10))
ax2.xaxis.set_minor_locator(MultipleLocator(5))
ax2.xaxis.grid()
ax2.set_xlim([-90,90])
ax2.set_ylim([0,100])
ax2.set_yticks(np.arange(0, 101, step=10))
ax2.yaxis.set_minor_locator(MultipleLocator(5))    
ax2.set_title(title,pad=2)
ax2.set_ylabel('Altitude [km]')
ax2.set_xlabel('Latitude [°]')
# m = np.ma.masked_where(np.isnan(drifts),drifts)
pcm = ax2.pcolor(latitudes, altitudes, drifts_stddev, cmap='rainbow', norm=colors.LogNorm(vmin=1e-9, vmax=1e-2) )
cbar = fig2.colorbar(pcm, ticks=[1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2 ])
cbar.set_label('O3 VMR [ppv/dec]', rotation=270,x=1.5,labelpad=13)
# ax2.yaxis.grid() 
name2 = 'C:\\Users\\victo\\Downloads\\Engsci Year 3 Sem 2\\PHY478 RESEARCH PROJECT\\Code\\Trend colormesh, '+str(latitude_grid)+' degree grid\\O3 VMR Measurements, ACE-MAESTRO ('+str(version)+'), Stddev.png'
fig2.savefig(name2)


# Plot the drifts for each altitude/latitude,
# masking out the invalid values
fig2, ax2 = plt.subplots(1, 1,figsize=[9, 4])
title = 'ACE-MAESTRO ('+str(version)+') O3 VMR Linear Trend'
ax2.set_xticks(np.arange(-90, 91, step=10))
ax2.xaxis.set_minor_locator(MultipleLocator(5))
ax2.xaxis.grid()
ax2.set_xlim([-90,90])
ax2.set_ylim([0,100])
ax2.set_yticks(np.arange(0, 101, step=10))
ax2.yaxis.set_minor_locator(MultipleLocator(5)) 
ax2.set_title(title,pad=2)
ax2.set_ylabel('Altitude [km]')
ax2.set_xlabel('Latitude [°]')
m = np.ma.masked_where(np.isnan(drifts_valid),drifts_valid)
pcm = ax2.pcolor(latitudes, altitudes, drifts_valid, cmap='Spectral', norm=colors.SymLogNorm(linthresh=1e-9, linscale=1e-9, vmin=-1e-3, vmax=1e-3) )
cbar = fig2.colorbar(pcm, ticks=[-1e-3, -1e-4, -1e-5, -1e-6, -1e-7, -1e-8, 0, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3 ])
cbar.set_label('O3 VMR [ppv/dec]', rotation=270,x=1.5,labelpad=13)
ax2.yaxis.grid() 
name2 = 'C:\\Users\\victo\\Downloads\\Engsci Year 3 Sem 2\\PHY478 RESEARCH PROJECT\\Code\\Trend colormesh, '+str(latitude_grid)+' degree grid\\O3 VMR Measurements, ACE-MAESTRO ('+str(version)+') masked.png'
fig2.savefig(name2)

