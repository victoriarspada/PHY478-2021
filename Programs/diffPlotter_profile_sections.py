# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 00:05:48 2021

@author: Victoria R Spada
"""
from OLS import *
from RMA import *
from delta_abs_rel import *
import numpy as np
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm_mat
import os
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

def diffPlotter_profile_sections(cm_pairs,plot_title,legend_labels):
    # Unpack the cm_pair input pair object. 
    length = len(cm_pairs)

    o3_vmr_mean_absolute_diff, o3_vmr_mean_absolute_diff_err = [], []
    o3_vmr_mean_relative_diff, o3_vmr_mean_relative_diff_err  = [],[]
    altitudes = numpy.arange(0, 100.5, 0.5)
    
    if len(cm_pairs)==3:
        # Create a scatter plot (linear regression), no colorbar.
        fig, axs = plt.subplots(3, 2,figsize=[16,16],dpi=100) # 0-20 km comparisons    
    
        axs[0,0].set_xlabel('Mean Absolute Difference [ppv]')
        axs[1,0].set_xlabel('Mean Absolute Difference [ppv]')
        axs[2,0].set_xlabel('Mean Absolute Difference [ppv]')
        axs[0,1].set_xlabel('Mean Relative Difference [%]')
        axs[1,1].set_xlabel('Mean Relative Difference [%]')
        axs[2,1].set_xlabel('Mean Relative Difference [%]')

        for m in range(0,3):
            for n in range(0,2):   
                axs[m,n].set_ylabel('Altitude [km]')
                axs[m,n].xaxis.get_label().set_fontsize(15)
                axs[m,n].yaxis.get_label().set_fontsize(15)        

        axs[0,0].set_ylim([60,100])
        axs[0,0].set_xlim([-1.5e-2,1.5e-2])
        axs[0,0].set_yticks(np.arange(60,101,10))
        axs[0,0].yaxis.set_minor_locator(MultipleLocator(1)) 

        axs[0,1].set_ylim([60,100])
        axs[0,1].set_xlim([-250,250])
        axs[0,1].set_yticks(np.arange(60,101,10))
        axs[0,1].yaxis.set_minor_locator(MultipleLocator(1)) 
        
        axs[1,0].set_ylim([20,60])
        axs[1,0].set_xlim([-1.5e-6,1.5e-6])
        axs[1,0].set_yticks(np.arange(20,61,10))
        axs[1,0].yaxis.set_minor_locator(MultipleLocator(1)) 
        
        axs[1,1].set_ylim([20,60])
        axs[1,1].set_xlim([-20,20])
        axs[1,1].set_yticks(np.arange(20,61,10))
        axs[1,1].yaxis.set_minor_locator(MultipleLocator(1)) 
        
        axs[2,0].set_ylim([0,20])
        axs[2,0].set_xlim([-1e-3,1e-3])
        axs[2,0].set_yticks(np.arange(0,21,10))
        axs[2,0].yaxis.set_minor_locator(MultipleLocator(1)) 
        
        axs[2,1].set_ylim([0,20])
        axs[2,1].set_xlim([-225,225])
        axs[2,1].set_yticks(np.arange(0,21,10))
        axs[2,1].yaxis.set_minor_locator(MultipleLocator(1)) 

        axs[0,0].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
        axs[1,0].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
        axs[2,0].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
        axs[0,1].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
        axs[1,1].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
        axs[2,1].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
    
        fig.suptitle(plot_title)
        colors = ['rebeccapurple','forestgreen','orangered']
        for i in range(0,length,1): # Cycle through each instrument
            cm_pair = cm_pairs[i]
            for k in range(0,len(cm_pair),1): # Cycle through each year of the current instrument
                if cm_pair[k].o3_vmr_mean_absolute_diff_err_arr==[]:
                    o3_vmr_mean_absolute_diff_err += [cm_pair[k].o3_vmr_mean_absolutee_diff_err_arr]
                else:
                    o3_vmr_mean_absolute_diff_err += [cm_pair[k].o3_vmr_mean_absolute_diff_err_arr]
                o3_vmr_mean_absolute_diff += [cm_pair[k].o3_vmr_mean_absolute_diff_arr]
                o3_vmr_mean_relative_diff += [cm_pair[k].o3_vmr_mean_relative_diff_arr] 
                o3_vmr_mean_relative_diff_err += [cm_pair[k].o3_vmr_mean_relative_diff_err_arr]

            # Create arrays for averages over the years
            avg_o3_vmr_mean_absolute_diff = np.zeros(201)
            avg_o3_vmr_mean_absolute_diff_err = np.zeros(201)
            avg_o3_vmr_mean_relative_diff = np.zeros(201) 
            avg_o3_vmr_mean_relative_diff_err = np.zeros(201)
            for j in range(0,len(o3_vmr_mean_absolute_diff),1): # Cycle through all years and take average
                avg_o3_vmr_mean_absolute_diff += np.array(o3_vmr_mean_absolute_diff[j])
                avg_o3_vmr_mean_absolute_diff_err += np.array(o3_vmr_mean_absolute_diff_err[j])
                avg_o3_vmr_mean_relative_diff += np.array(o3_vmr_mean_relative_diff[j]) 
                avg_o3_vmr_mean_relative_diff_err += np.array(o3_vmr_mean_relative_diff_err[j])
                
            avg_o3_vmr_mean_absolute_diff = avg_o3_vmr_mean_absolute_diff/j 
            avg_o3_vmr_mean_absolute_diff_err = avg_o3_vmr_mean_absolute_diff_err/j *0.1
            avg_o3_vmr_mean_relative_diff = avg_o3_vmr_mean_relative_diff/j 
            avg_o3_vmr_mean_relative_diff_err = avg_o3_vmr_mean_relative_diff_err/j *0.1
        
            axs[0,0].plot( avg_o3_vmr_mean_absolute_diff, altitudes, color=colors[i],label=legend_labels[i])
            axs[1,0].plot( avg_o3_vmr_mean_absolute_diff, altitudes, color=colors[i],label=legend_labels[i])
            axs[2,0].plot( avg_o3_vmr_mean_absolute_diff, altitudes, color=colors[i],label=legend_labels[i])
            axs[0,1].plot( avg_o3_vmr_mean_relative_diff, altitudes, color=colors[i],label=legend_labels[i])
            axs[1,1].plot( avg_o3_vmr_mean_relative_diff, altitudes, color=colors[i],label=legend_labels[i])
            axs[2,1].plot( avg_o3_vmr_mean_relative_diff, altitudes, color=colors[i],label=legend_labels[i])

            axs[0,0].plot(avg_o3_vmr_mean_absolute_diff_err,altitudes, linestyle='--', linewidth=0.5, color=colors[i],label='_nolegend_')
            axs[1,0].plot(avg_o3_vmr_mean_absolute_diff_err,altitudes, linestyle='--', linewidth=0.5, color=colors[i],label='_nolegend_')
            axs[2,0].plot(avg_o3_vmr_mean_absolute_diff_err,altitudes, linestyle='--', linewidth=0.5, color=colors[i],label='_nolegend_')
            axs[0,1].plot(avg_o3_vmr_mean_relative_diff_err,altitudes, linestyle='--', linewidth=0.5, color=colors[i],label='_nolegend_')
            axs[1,1].plot(avg_o3_vmr_mean_relative_diff_err,altitudes, linestyle='--', linewidth=0.5, color=colors[i],label='_nolegend_')
            axs[2,1].plot(avg_o3_vmr_mean_relative_diff_err,altitudes, linestyle='--', linewidth=0.5, color=colors[i],label='_nolegend_')

    else:
        colors = ['teal','blue','purple','deeppink','red','orange','green','grey']
        # Create a scatter plot (linear regression), no colorbar.
        fig, axs = plt.subplots(3, 2,figsize=[16,16],dpi=100) # 0-20 km comparisons    
        fig.suptitle(plot_title, fontsize=20, y=0.95)
                
        axs[0,0].set_xlabel('Mean Absolute Difference [ppv]')
        axs[1,0].set_xlabel('Mean Absolute Difference [ppv]')
        axs[2,0].set_xlabel('Mean Absolute Difference [ppv]')
        axs[0,1].set_xlabel('Mean Relative Difference [%]')
        axs[1,1].set_xlabel('Mean Relative Difference [%]')
        axs[2,1].set_xlabel('Mean Relative Difference [%]')

        for m in range(0,3):
            for n in range(0,2):   
                axs[m,n].set_ylabel('Altitude [km]')
                axs[m,n].xaxis.get_label().set_fontsize(15)
                axs[m,n].yaxis.get_label().set_fontsize(15)        

        axs[0,0].set_ylim([60,100])
        axs[0,0].set_xlim([-1e-2,1e-2])
        axs[0,0].set_yticks(np.arange(60,101,10))
        axs[0,0].yaxis.set_minor_locator(MultipleLocator(1)) 

        axs[0,1].set_ylim([60,100])
        axs[0,1].set_xlim([-200,200])
        axs[0,1].set_yticks(np.arange(60,101,10))
        axs[0,1].yaxis.set_minor_locator(MultipleLocator(1)) 
        
        axs[1,0].set_ylim([20,60])
        axs[1,0].set_xlim([-1e-6,1e-6])
        axs[1,0].set_yticks(np.arange(20,61,10))
        axs[1,0].yaxis.set_minor_locator(MultipleLocator(1)) 
        
        axs[1,1].set_ylim([20,60])
        axs[1,1].set_xlim([-15,15])
        axs[1,1].set_yticks(np.arange(20,61,10))
        axs[1,1].yaxis.set_minor_locator(MultipleLocator(1)) 
        
        axs[2,0].set_ylim([0,10])
        axs[2,0].set_xlim([-1e-3,1e-3])
        axs[2,0].set_yticks(np.arange(0,21,10))
        axs[2,0].yaxis.set_minor_locator(MultipleLocator(1)) 
        
        axs[2,1].set_ylim([0,10])
        axs[2,1].set_xlim([-200,200])
        axs[2,1].set_yticks(np.arange(0,21,10))
        axs[2,1].yaxis.set_minor_locator(MultipleLocator(1)) 
        
        axs[0,0].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
        axs[1,0].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
        axs[2,0].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
        axs[0,1].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
        axs[1,1].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
        axs[2,1].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
    
        for i in range(0,length,1): # Cycle through each year for the instrument
            cm_pair = cm_pairs[i]
            o3_vmr_mean_absolute_diff += [cm_pair.o3_vmr_mean_absolute_diff_arr]
            if cm_pair.o3_vmr_mean_absolute_diff_err_arr==[]:
                o3_vmr_mean_absolute_diff_err += [cm_pair.o3_vmr_mean_absolutee_diff_err_arr]
            else:
                o3_vmr_mean_absolute_diff_err += [cm_pair.o3_vmr_mean_absolute_diff_err_arr]
            o3_vmr_mean_relative_diff += [cm_pair.o3_vmr_mean_relative_diff_arr] 
            o3_vmr_mean_relative_diff_err += [cm_pair.o3_vmr_mean_relative_diff_err_arr]

        # Create arrays for averages 
        avg_o3_vmr_mean_absolute_diff = np.zeros(201)
        avg_o3_vmr_mean_absolute_diff_err = np.zeros(201)
        avg_o3_vmr_mean_relative_diff = np.zeros(201) 
        avg_o3_vmr_mean_relative_diff_err = np.zeros(201)
        for j in range(0,len(o3_vmr_mean_absolute_diff),1): # Cycle through all years and take average
            print(j)
            avg_o3_vmr_mean_absolute_diff = np.array(o3_vmr_mean_absolute_diff[j])
            avg_o3_vmr_mean_absolute_diff_err = np.array(o3_vmr_mean_absolute_diff_err[j])
            avg_o3_vmr_mean_relative_diff = np.array(o3_vmr_mean_relative_diff[j]) 
            avg_o3_vmr_mean_relative_diff_err = np.array(o3_vmr_mean_relative_diff_err[j])
            if j < 2:
                axs[0,0].text(-8e-3,106-4*j,str(2004+j),color=colors[j], fontsize=16)
            elif j< 4:
                axs[0,0].text(-4e-3,106-4*(j-2),str(2004+j),color=colors[j], fontsize=16)
            elif j<6:
                axs[0,0].text(0e-3,106-4*(j-4),str(2004+j),color=colors[j], fontsize=16)
            else:
                axs[0,0].text(4e-3,106-4*(j-6),str(2004+j),color=colors[j], fontsize=16)
            axs[0,0].plot( avg_o3_vmr_mean_absolute_diff, altitudes, color=colors[j],  label=legend_labels[j])
            axs[1,0].plot( avg_o3_vmr_mean_absolute_diff, altitudes, color=colors[j], label=legend_labels[j])
            axs[2,0].plot( avg_o3_vmr_mean_absolute_diff, altitudes, color=colors[j], label=legend_labels[j])

            axs[0,1].plot( avg_o3_vmr_mean_relative_diff, altitudes, color=colors[j], label=legend_labels[j])
            axs[1,1].plot( avg_o3_vmr_mean_relative_diff, altitudes, color=colors[j], label=legend_labels[j])
            axs[2,1].plot( avg_o3_vmr_mean_relative_diff, altitudes,  color=colors[j], label=legend_labels[j])

    fig.savefig(plot_title+'.png')
    
    return 

