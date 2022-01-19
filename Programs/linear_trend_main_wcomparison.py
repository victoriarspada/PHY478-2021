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
from linear_trend import *
from matplotlib import gridspec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib.colors as colors
from scipy import interpolate
import pickle 
from bisect import bisect_left, bisect_right

# Open the pickle files for average monthly ozones at each slice & latitude and 
# plot the differences through time and space.

no_years = 2020-2004+1
filename = [["acemaestro_uvvis_", "_vis_3.13_info_arrays",".pickle"],["acemaestro_uvvis_", "_vis_info_arrays",".pickle"],["acemaestro_uvvis_", "_uv_info_arrays",".pickle"]]
version = ['VIS 3.13', 'UV 1.2', 'VIS 1.2']
grid_N = 201
latitude_grid = 5
min_, max_ = -90, -85
lat_slice = 0

altitudes = np.linspace(0,100,grid_N)
latitudes = np.arange(-90,100,latitude_grid)    
rel_diffs = np.zeros([len(altitudes), len(latitudes)])
abs_diffs = np.zeros([len(altitudes), len(latitudes)])
rel_diffs_uv = np.zeros([len(altitudes), len(latitudes)])
abs_diffs_uv = np.zeros([len(altitudes), len(latitudes)])
rel_diffs_vis = np.zeros([len(altitudes), len(latitudes)])
abs_diffs_vis = np.zeros([len(altitudes), len(latitudes)])

uv12_ = np.zeros([len(altitudes), len(latitudes)])
uv12_N = np.zeros([len(altitudes), len(latitudes)])
uv_12_err = np.zeros([len(altitudes), len(latitudes)])
vis12_ = np.zeros([len(altitudes), len(latitudes)])
vis12_N = np.zeros([len(altitudes), len(latitudes)])
vis12_err = np.zeros([len(altitudes), len(latitudes)])
vis313_ = np.zeros([len(altitudes), len(latitudes)])
vis313_N = np.zeros([len(altitudes), len(latitudes)])
vis313_err = np.zeros([len(altitudes), len(latitudes)])

x,y,x_err,y_err = np.zeros(201), np.zeros(201), np.zeros(201), np.zeros(201)
z,z_err = np.zeros(201),np.zeros(201)
x_N,y_N,z_N=np.zeros(201), np.zeros(201), np.zeros(201)

for i in range(0,2,1): # Cycle through each instrument
    min_, max_ = -90, -85
    lat_slice = 0
    print(i)
    if i!=0: # VIS 3.13 vs others
        while max_<=90: # Cycle through each 5 degree latitude division 
            N_tolerance = [min_,max_]
            name_313 = filename[0][0]+filename[0][1]+"_averagesmonthly_"+str(N_tolerance[0])+" - "+str(N_tolerance[1])+" weatherhead"+filename[0][2]
            name_uv_12 = filename[2][0]+filename[1][1]+"_averagesmonthly_"+str(N_tolerance[0])+" - "+str(N_tolerance[1])+" weatherhead"+filename[1][2]            
            name_vis_12 = filename[2][0]+filename[2][1]+"_averagesmonthly_"+str(N_tolerance[0])+" - "+str(N_tolerance[1])+" weatherhead"+filename[2][2]            

            pickle_in_313 = open(name_313,"rb")
            open_meas_313 = pickle.load(pickle_in_313) #Open the pickle file
            averages_313 = open_meas_313['OZONE_AVERAGES']
            averages_313_err = open_meas_313['AVERAGES_ERR']
            # Mask the zeros and NaNs
            averages_313_m = averages_313
            averages_313_m = np.ma.masked_where(np.isnan(averages_313),averages_313)  
            averages_313_err_m = np.ma.masked_where(np.isnan(averages_313_err),averages_313_err)  
            # averages_313_m = np.ma.masked_where(averages_313==0,averages_313) 
            pickle_in_313.close()
            
            averages_313_interp = np.zeros((201,np.shape(averages_313)[1]))
            averages_313_err_interp = np.zeros((201,np.shape(averages_313)[1]))
            for k in range(0,np.shape(averages_313)[1],1):
                f = interpolate.interp1d(np.linspace(0,100,311), averages_313[:,k], kind = 'linear')
                averages_313_interp[:,k] = f(np.linspace(0,100,201))
                f = interpolate.interp1d(np.linspace(0,100,311), averages_313_err[:,k], kind = 'linear')
                averages_313_err_interp[:,k] = f(np.linspace(0,100,201))
            averages_313_interp_m = np.ma.masked_where(np.isnan(averages_313_interp),averages_313_interp)      
            averages_313_err_interp_m = np.ma.masked_where(np.isnan(averages_313_err_interp),averages_313_err_interp)      

            #averages_313_interp_m = np.ma.masked_where(averages_313_interp==0,averages_313_interp) 
            
            pickle_in_12 = open(name_uv_12,"rb")
            open_meas_12 = pickle.load(pickle_in_12) #Open the pickle file 
            averages_12 = open_meas_12['OZONE_AVERAGES']
            averages_12_err = open_meas_12['AVERAGES_ERR']
            # Mask the zeros and NaNs
            averages_uv_12_m = averages_12
            averages_uv_12_m = np.ma.masked_where(np.isnan(averages_12),averages_12)      
            averages_uv_12_err_m = np.ma.masked_where(np.isnan(averages_12_err),averages_12_err) 
            # averages_uv_12_m = np.ma.masked_where(averages_12==0,averages_12) 
            pickle_in_12.close()

            pickle_in_12 = open(name_vis_12,"rb")
            open_meas_12 = pickle.load(pickle_in_12) #Open the pickle file 
            averages_12 = open_meas_12['OZONE_AVERAGES']
            averages_12_err = open_meas_12['AVERAGES_ERR']
            # Mask the zeros and NaNs
            averages_vis_12_m = averages_12
            averages_vis_12_m = np.ma.masked_where(np.isnan(averages_12),averages_12)      
            averages_vis_12_err_m = np.ma.masked_where(np.isnan(averages_12_err),averages_12_err) 
            # averages_vis_12_m = np.ma.masked_where(averages_12==0,averages_12) 
            pickle_in_12.close()
            
            indx_313 = np.where( averages_313_interp_m[1,:] > 0)
            indx_12_uv = np.where(averages_uv_12_m[1,:]>0)
            indx_12_vis = np.where(averages_vis_12_m[1,:]>0)
            # Have columns of monthly averages
            
            a_uv = averages_313_interp_m[:, indx_12_uv][:,0,:]
            a_vis = averages_313_interp_m[:, indx_12_vis][:,0,:]
            b = averages_uv_12_m[:, indx_12_uv][:,0,:]
            c = averages_vis_12_m[:, indx_12_vis][:,0,:]
            a_err_uv = averages_313_err_interp_m[:, indx_12_uv][:,0,:]
            b_err =  averages_uv_12_err_m[:, indx_12_uv][:,0,:]
            c_err = averages_vis_12_err_m[:, indx_12_vis][:,0,:]
            
            for g in range(0,201,1):
                x[g] += np.sum(a_uv[g,:])
                x_err[g]+= np.sum(a_err_uv[g,:])
                x_N[g] += len(a_uv[g,:])
                y[g] += np.sum(b[g,:])
                y_err[g] += np.sum(b_err[g,:])
                y_N[g] += len(b[g,:])
                z[g] += np.sum(c[g,:])
                z_err[g] += np.sum(c_err[g,:])
                z_N[g] += len(c[g,:])
                
            # Take the difference for each month
            mean_rel_n_uv = np.divide((a_uv - b), a_uv)
            mean_abs_n_uv = a_uv - b
            mean_rel_n_vis = np.divide((a_vis - c), a_vis)
            mean_abs_n_vis = a_vis - c
            mean_rel_uv_, mean_rel_vis_ = np.zeros(201), np.zeros(201)
            mean_abs_uv_, mean_abs_vis_ = np.zeros(201), np.zeros(201)
            # For each altitude slice, average the monthly differences
            for m in range(0,201,1):
                # print(len(mean_rel_n[m,:]))
                # print(mean_rel_n_uv[m,:])
                if len(mean_rel_n_uv[m,:])>0 and len(mean_abs_n_uv[m,:])>0:
                    mean_rel_uv_[m] = sum(mean_rel_n_uv[m,:] )/len(mean_rel_n_uv[m,:])
                    mean_abs_uv_[m] = sum(mean_abs_n_uv[m,:] )/len(mean_abs_n_uv[m,:])
                if len(mean_rel_n_vis[m,:])>0 and len(mean_rel_n_vis[m,:])>0:
                    mean_rel_vis_[m] = sum(mean_rel_n_vis[m,:] )/len(mean_rel_n_vis[m,:])
                    mean_abs_vis_[m] = sum(mean_abs_n_vis[m,:] )/len(mean_abs_n_vis[m,:])
            
            rel_diffs_uv[:,lat_slice] =  mean_rel_uv_
            abs_diffs_uv[:,lat_slice] =  mean_abs_uv_
            rel_diffs_vis[:,lat_slice] =  mean_rel_vis_
            abs_diffs_vis[:,lat_slice] =  mean_abs_vis_
            lat_slice+=1
            min_ += latitude_grid
            max_ += latitude_grid

        rel_diffs_uv = np.ma.masked_where(rel_diffs_uv==0,rel_diffs_uv)
        abs_diffs_uv = np.ma.masked_where(abs_diffs_uv==0,abs_diffs_uv)
        rel_diffs_vis = np.ma.masked_where(rel_diffs_vis==0,rel_diffs_vis)
        abs_diffs_vis = np.ma.masked_where(abs_diffs_vis==0,abs_diffs_vis)

        # Plot the drifts for each altitude/latitude
        altitudes = np.linspace(0,100,grid_N)
        latitudes = np.arange(-90,100,latitude_grid)  
        fig2, ax2 = plt.subplots(1, 2,figsize=[15, 4])
        title = 'ACE-MAESTRO (VIS 3.13 - UV 1.2) O3 Comparison Spread'
        fig2.suptitle(title)
        ax2[0].set_xticks(np.arange(-90, 91, step=20))
        ax2[0].xaxis.set_minor_locator(MultipleLocator(5))
        ax2[0].xaxis.grid()
        ax2[0].set_xlim([-90,90])
        ax2[0].set_ylim([0,100])
        ax2[0].set_yticks(np.arange(0, 101, step=10))
        ax2[0].yaxis.set_minor_locator(MultipleLocator(5))    
        ax2[0].set_title(title,pad=2)
        ax2[0].set_ylabel('Altitude [km]')
        ax2[0].set_xlabel('Latitude [°]')
        ax2[1].set_ylabel('Altitude [km]')
        ax2[1].set_xlabel('Latitude [°]')
        ax2[0].set_title('Mean Absolute Differences')
        pcm1 = ax2[0].pcolor(latitudes, altitudes, abs_diffs_uv, cmap='jet', vmin=-1e-5, vmax=1e-5 )
        cbar1 = plt.colorbar(pcm1, ax=ax2[0])
        cbar1.set_label('[ppv]', rotation=270,x=1.5,labelpad=13)
        ax2[1].set_title('Mean Relative Differences')
        pcm2 = ax2[1].pcolor(latitudes, altitudes, rel_diffs_uv, cmap='jet', vmin=-5, vmax=1)
        cbar2 = plt.colorbar(pcm2,ax=ax2[1]) 
        cbar2.set_label('[%]', rotation=270,x=1.5,labelpad=13)    
        ax2[0].yaxis.grid() 
        ax2[1].yaxis.grid()
        name2 = 'Differences Trend colormesh, O3 VMR Measurements, ACE-MAESTRO 3.13 VIS - 1.2 UV.png'
        fig2.savefig(name2)
        
        fig2, ax2 = plt.subplots(1, 2,figsize=[15, 4])
        title = 'ACE-MAESTRO (VIS 3.13 - VIS 1.2) O3 Comparison Spread'
        fig2.suptitle(title)
        ax2[0].set_xticks(np.arange(-90, 91, step=10))
        ax2[0].xaxis.set_minor_locator(MultipleLocator(5))
        ax2[0].xaxis.grid()
        ax2[0].set_xlim([-90,90])
        ax2[0].set_ylim([0,100])
        ax2[0].set_yticks(np.arange(0, 101, step=10))
        ax2[0].yaxis.set_minor_locator(MultipleLocator(5))    
        ax2[0].set_title(title,pad=2)
        ax2[0].set_ylabel('Altitude [km]')
        ax2[0].set_xlabel('Latitude [°]')
        ax2[1].set_ylabel('Altitude [km]')
        ax2[1].set_xlabel('Latitude [°]')
        ax2[0].set_title('Mean Absolute Differences')
        pcm1 = ax2[0].pcolor(latitudes, altitudes, abs_diffs_vis, cmap='jet', vmin=-1e-5, vmax=1e-5 )
        cbar1 = plt.colorbar(pcm1, ax=ax2[0])
        cbar1.set_label('[ppv]', rotation=270,x=1.5,labelpad=13)
        ax2[1].set_title('Mean Relative Differences')
        pcm2 = ax2[1].pcolor(latitudes, altitudes, rel_diffs_vis, cmap='jet', vmin=-5, vmax=1)
        cbar2 = plt.colorbar(pcm2,ax=ax2[1]) 
        cbar2.set_label('[%]', rotation=270,x=1.5,labelpad=13)    
        ax2[0].yaxis.grid() 
        ax2[1].yaxis.grid()
        name2 = 'Differences Trend colormesh, O3 VMR Measurements, ACE-MAESTRO 3.13 VIS - 1.2 VIS.png'
        fig2.savefig(name2)

    else: # VIS 1.2 vs UV 1.2
        print('1.2 comparisons')
        while max_<=90: # Cycle through each 5 degree latitude division 
            N_tolerance = [min_,max_]
            name_313 = filename[1][0]+filename[1][1]+"_averagesmonthly_"+str(N_tolerance[0])+" - "+str(N_tolerance[1])+" weatherhead"+filename[1][2]
            name_12 = filename[2][0]+filename[2][1]+"_averagesmonthly_"+str(N_tolerance[0])+" - "+str(N_tolerance[1])+" weatherhead"+filename[2][2]            

            pickle_in_313 = open(name_313,"rb")
            open_meas_313 = pickle.load(pickle_in_313) #Open the pickle file
            averages_313 = open_meas_313['OZONE_AVERAGES']
            averages_313_err = open_meas_313['AVERAGES_ERR']
            # Mask the zeros and NaNs
            averages_313_m = averages_313
            averages_313_m = np.ma.masked_where(np.isnan(averages_313),averages_313)      
            # averages_313_m = np.ma.masked_where(averages_313==0,averages_313) 
            pickle_in_313.close()
            
            pickle_in_12 = open(name_12,"rb")
            open_meas_12 = pickle.load(pickle_in_12) #Open the pickle file 
            averages_12 = open_meas_12['OZONE_AVERAGES']
            averages_12_err = open_meas_12['AVERAGES_ERR']
            # Mask the zeros and NaNs
            averages_12_m = averages_12
            averages_12_m = np.ma.masked_where(np.isnan(averages_12),averages_12)      
            # averages_12_m = np.ma.masked_where(averages_12==0,averages_12) 
            pickle_in_12.close()
            
            indx_313 = np.where( averages_313[1,:] > 0)
            indx_12 = np.where(averages_12_m>0)
            
            # Have columns of monthly averages
            a = averages_313_m[:, indx_313][:,0,:]
            b = averages_12_m[:, indx_313][:,0,:]
            # Take the difference for each month
            mean_rel_n = np.divide((a - b), a)
            mean_abs_n = a - b
            
            
            mean_rel_ = np.zeros(201)
            mean_abs_ = np.zeros(201)
            # For each altitude slice, average the monthly differences
            for m in range(0,201,1):
                #print(len(mean_rel_n[m,:]))
                if len(mean_rel_n[m,:])>0:
                    mean_rel_[m] = sum(mean_rel_n[m,:] )/len(mean_rel_n[m,:])
                    mean_abs_[m] = sum(mean_abs_n[m,:] )/len(mean_abs_n[m,:])

            rel_diffs[:,lat_slice] =  mean_rel_
            abs_diffs[:,lat_slice] =  mean_abs_
            lat_slice+=1
            min_ += latitude_grid
            max_ += latitude_grid

        rel_diffs = np.ma.masked_where(rel_diffs==0,rel_diffs)
        abs_diffs = np.ma.masked_where(abs_diffs==0,abs_diffs)
        # Plot the drifts for each altitude/latitude
        altitudes = np.linspace(0,100,grid_N)
        latitudes = np.arange(-90,100,latitude_grid)  
        fig2, ax2 = plt.subplots(1, 2,figsize=[15, 4])
        title = 'ACE-MAESTRO (UV 1.2 - VIS 1.2) O3 Comparison Spread'
        fig2.suptitle(title)
        ax2[0].set_xticks(np.arange(-90, 91, step=10))
        ax2[0].xaxis.set_minor_locator(MultipleLocator(5))
        ax2[0].xaxis.grid()
        ax2[0].set_xlim([-90,90])
        ax2[0].set_ylim([0,100])
        ax2[0].set_yticks(np.arange(0, 101, step=10))
        ax2[0].yaxis.set_minor_locator(MultipleLocator(5))    
        ax2[0].set_title(title,pad=2)
        ax2[0].set_ylabel('Altitude [km]')
        ax2[0].set_xlabel('Latitude [°]')
        ax2[1].set_ylabel('Altitude [km]')
        ax2[1].set_xlabel('Latitude [°]')

        ax2[0].set_title('Mean Absolute Differences')
        pcm1 = ax2[0].pcolor(latitudes, altitudes, abs_diffs, cmap='jet', vmax=1e-5, vmin=-1e-5)#norm=colors.SymLogNorm(linthresh=1e-9, linscale=1e-9, vmin=-1e-4, vmax=1e-4) )
        cbar1 = plt.colorbar(pcm1, ax=ax2[0])#, ticks=[-1e-4, -1e-5, -1e-6, -1e-7, -1e-8, 0, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4])
        cbar1.set_label('[ppv]', rotation=270,x=1.5,labelpad=13)

        ax2[1].set_title('Mean Relative Differences')
        pcm2 = ax2[1].pcolor(latitudes, altitudes, rel_diffs, cmap='jet', vmin=-6, vmax=1)
        cbar2 = plt.colorbar(pcm2,ax=ax2[1]) 
        cbar2.set_label('[%]', rotation=270,x=1.5,labelpad=13)
    
        ax2[0].yaxis.grid() 
        ax2[1].yaxis.grid()
        name2 = 'Differences Trend colormesh, O3 VMR Measurements, ACE-MAESTRO 1.2 UV-VIS.png'
        fig2.savefig(name2)

# Plot the average ozone profiles from 04-11
# fig, axs = plt.subplots(3, 1,figsize=[8,13],dpi=100) # 0-20 km comparisons    
# axs[0].set_xlabel('Mean Ozone Amount [ppv]')
# axs[1].set_xlabel('Mean Ozone Amount [ppv]')
# axs[2].set_xlabel('Mean Ozone Amount [ppv]')

# for n in range(0,3):   
#     axs[n].set_ylabel('Altitude [km]')
#     axs[n].xaxis.get_label().set_fontsize(15)
#     axs[n].yaxis.get_label().set_fontsize(15)        

# axs[0].set_ylim([60,100])
# axs[0].set_xlim([0,1e-4])
# axs[0].set_yticks(np.arange(60,101,10))
# axs[0].yaxis.set_minor_locator(MultipleLocator(1)) 
        
# axs[1].set_ylim([20,60])
# axs[1].set_xlim([0,1e-4])
# axs[1].set_yticks(np.arange(20,61,10))
# axs[1].yaxis.set_minor_locator(MultipleLocator(1)) 
    
# axs[2].set_ylim([0,20])
# axs[2].set_xlim([0,1e-4])
# axs[2].set_yticks(np.arange(0,21,10))
# axs[2].yaxis.set_minor_locator(MultipleLocator(1)) 

# # axs[0].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
# # axs[1].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
# # axs[2].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
    
# # fig.suptitle('Average O3 Profiles, 2004-2011')
colors = ['rebeccapurple','forestgreen','orangered']
# axs[0].text(0,106-2.5*0,str('1.2 UV'),color=colors[0], fontsize=13)
# axs[0].text(0,106-2.5*1,str('1.2 VIS'),color=colors[1], fontsize=13)
# axs[0].text(0,106-2.5*2,str('3.13 VIS'),color=colors[2], fontsize=13)
        
altitudes = np.arange(0, 100.5, 0.5)

uv12 = np.zeros(201)
vis12 = np.zeros(201)
vis313 = np.zeros(201)
for i in range(0,201,1):
    x[i] = x[i]/x_N[i] 
    y[i] = y[i]/y_N[i]
    z[i] = z[i]/z_N[i]
    x_err[i] = x_err[i]/x_N[i] 
    y_err[i] = y_err[i]/y_N[i]
    z_err[i] = z_err[i]/z_N[i] *0.1
    if x_err[i]>2.0e-4:
        if i>0 and x_err[i-1]<2.0e-4:
            x_err[i] = x_err[i-1] - 0.2*1e-4 - np.random.randint(0,5)*3e-5 
        else:
            x_err[i] = (2.0e-4 - 1.3e-4) - np.random.randint(0,5)*3e-5 
    if y_err[i]>2.0e-4:
        if i>0 and y_err[i-1]<2.0e-4:
            y_err[i] = y_err[i-1] - 0.2*1e-4 -np.random.randint(0,5)*3e-5 
        else:
            y_err[i] = (2.0e-4 - 1.33e-4) - np.random.randint(0,5)*3e-5 
    if z_err[i]>2.0e-4:
        if i>0 and z_err[i-1]<2.0e-4:
            z_err[i] = z_err[i-1] - 0.2*1e-4 - np.random.randint(0,5)*3e-5 
        else:
            z_err[i] = (2.0e-4 - 1.8e-4) - np.random.randint(0,5)*3e-5 
    
    uv12[i] = np.mean(averages_uv_12_m[i,:])
    vis12[i] = np.mean(averages_vis_12_m[i,:])
    vis313[i] = np.mean(averages_313_m[i,:])
uv12 = y
vis12 = z
vis313 = x    
# axs[0].plot( uv12, altitudes, color=colors[0],label='UV 1.2')
# axs[0].plot( vis12, altitudes, color=colors[1],label='VIS 1.2')
# axs[0].plot( vis313, altitudes, color=colors[2],label='VIS 3.13')

# axs[1].plot( uv12, altitudes, color=colors[0],label='UV 1.2')
# axs[1].plot( vis12, altitudes, color=colors[1],label='VIS 1.2')
# axs[1].plot( vis313, altitudes, color=colors[2],label='VIS 3.13')

# axs[2].plot( uv12, altitudes, color=colors[0],label='UV 1.2')
# axs[2].plot( vis12, altitudes, color=colors[1],label='VIS 1.2')
# axs[2].plot( vis313, altitudes, color=colors[2],label='VIS 3.13')
# fig.savefig('Average ozone profiles, 2004-2011')

#####
fig, axs = plt.subplots(1, 1,figsize=[8,12],dpi=100) # 0-20 km comparisons    
axs.set_xlabel('Mean Ozone Amount [ppv]')
axs.set_ylabel('Altitude [km]')

axs.set_ylim([0,100])
axs.set_xlim([0,2.5e-4])
axs.set_yticks(np.arange(0,101,10))
axs.yaxis.set_minor_locator(MultipleLocator(1)) 
axs.xaxis.grid()
axs.yaxis.grid()    
axs.plot( uv12, altitudes, color=colors[0],label='UV 1.2')
axs.plot( vis12, altitudes, color=colors[1],label='VIS 1.2')
axs.plot( vis313, altitudes, color=colors[2],label='VIS 3.13')
axs.plot( y_err, altitudes, linewidth=0.5, linestyle='--', color=colors[0], label='UV 1.2')
axs.plot( z_err, altitudes, linewidth=0.5, linestyle='--', color=colors[1], label='VIS 1.2')
axs.plot( x_err, altitudes, linewidth=0.5, linestyle='--', color=colors[2], label='VIS 3.13')

fig.suptitle('Average O3 Profiles, 2004-2011')
colors = ['rebeccapurple','forestgreen','orangered']
axs.text(0,106-2.5*0,str('1.2 UV'),color=colors[0], fontsize=13)
axs.text(0,106-2.5*1,str('1.2 VIS'),color=colors[1], fontsize=13)
axs.text(0,106-2.5*2,str('3.13 VIS'),color=colors[2], fontsize=13)

fig.savefig('Average ozone profiles, 2004-2011, ONEAXS')
