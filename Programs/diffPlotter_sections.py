# -*- coding: utf-8 -*-
"""
Created on Thurs Jul 16 10:19:00 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: Feb 18 2021.
"""
from OLS import *
from RMA import *
from delta_abs_rel import *
import numpy as np
import datetime
import pandas as pd
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm_mat
import os

def diffPlotter_all(cm_pairs,regression_title,regression_labels):
    # PLOT ALL ALTITUDES (PROFILE) OF DIFFERENCES FOR ALL YEARS
    # NOT GOOD FOR SHOWING A PROFILE WITH A LOT OF VARIATION
    
    # Unpack the cm_pair input pair object. 
    length = len(cm_pairs)
    # Create a scatter plot (linear regression), no colorbar.
    fig, axs = plt.subplots(1, 2,figsize=[7,7],dpi=100,sharey=True) # 0-20 km comparisons    
    
    axs[0].set_xlabel('Mean Absolute Difference [ppv]',fontsize=8)
    axs[1].set_xlabel('Mean Relative Difference [%]',fontsize=8)

    axs[0].set_ylabel('Altitude [km]')    
    axs[0].set_ylim([0,105])

    axs[0].set_xlim([-5e-6,5e-6])
    axs[1].set_xlim([-50,50])

    axs[1].set_yticks(np.arange(0,105,10))

    fig.suptitle(regression_title,x=0.51,y=1.03,fontsize=9)

    o3_vmr_mean_absolute_diff, o3_vmr_mean_absolute_diff_err = [], []
    o3_vmr_mean_relative_diff, o3_vmr_mean_relative_diff_err  = [],[]
    altitudes = numpy.arange(0, 100.5, 0.5)
    for i in range(0,length,1):
        cm_pair = cm_pairs[i]
        o3_vmr_mean_absolute_diff += [cm_pair.o3_vmr_mean_absolute_diff_arr]
        o3_vmr_mean_absolute_diff_err += [cm_pair.o3_vmr_mean_absolute_diff_err_arr]
        o3_vmr_mean_relative_diff += [cm_pair.o3_vmr_mean_relative_diff_arr] 
        o3_vmr_mean_relative_diff_err += [cm_pair.o3_vmr_mean_relative_diff_err_arr]  
        
    years = np.arange(2004-1,2004+length+1,1)
    size = len(years)
    axs[0].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')
    axs[1].plot(np.zeros(10), np.linspace(0,150,10),linewidth=2, linestyle='--',color='k',label='_nolegend_')

    for i in range(0,length,1):        
        axs[0].plot(o3_vmr_mean_absolute_diff[i], altitudes, linestyle='-',label=str(2004+i))
        axs[1].plot(o3_vmr_mean_relative_diff[i], altitudes, linestyle='-',label=str(2004+i))
    axs[0].legend(fontsize=7)
    axs[1].legend(fontsize=7)
    plt.tight_layout()
    fig.savefig('Mean ab and rel differences by altitude.png') # Save figure.
    return 
   
def diffPlotter_sections(cm_pairs,regression_title,regression_labels):
    # Unpack the cm_pair input pair object. 
    # MAKE A FIGURE FOR THE MEAN AND ABSOLUTE DIFFERENCES, AND ALSO BY ALTITUDE SECTION
    # LOTS OF FIGURES LOTS OF INFORMATION 
    
    length = len(cm_pairs)
    # Create a scatter plot (linear regression), no colorbar.
    fig, axs = plt.subplots(2, 1,figsize=[6,4],dpi=100,sharex=True) # 0-20 km comparisons    
    fig020, axs020 = plt.subplots(2, 1,figsize=[6,4],dpi=100,sharex=True) # 0-20 km comparisons
    fig2060, axs2060 = plt.subplots(2, 1,figsize=[6,4],dpi=100,sharex=True) # 20-60 km comparisons
    fig60100, axs60100 = plt.subplots(2, 1,figsize=[6,4],dpi=100,sharex=True) # 60-100 km comparisons

    figabs, axsabs = plt.subplots(4, 1,figsize=[6,6],dpi=100,sharex=True)
    figrel, axsrel = plt.subplots(4, 1,figsize=[6,6],dpi=100,sharex=True)
    
    axs[0].set_ylabel('Mean Absolute Difference [ppv]',fontsize=7)
    axs[1].set_ylabel('Mean Relative Difference [%]',fontsize=7)
    axs020[0].set_ylabel('Mean Absolute Difference [ppv]',fontsize=7)
    axs020[1].set_ylabel('Mean Relative Difference [%]',fontsize=7)
    axs2060[0].set_ylabel('Mean Absolute Difference [ppv]',fontsize=7)
    axs2060[1].set_ylabel('Mean Relative Difference [%]',fontsize=7)
    axs60100[0].set_ylabel('Mean Absolute Difference [ppv]',fontsize=7)
    axs60100[1].set_ylabel('Mean Relative Difference [%]',fontsize=7)

    axsabs[0].set_ylabel('[ppv]')
    axsabs[1].set_ylabel('[ppv]')
    axsabs[2].set_ylabel('[ppv]')
    axsabs[3].set_ylabel('[ppv]')
    axsrel[0].set_ylabel('[%]')
    axsrel[1].set_ylabel('[%]')
    axsrel[2].set_ylabel('[%]')
    axsrel[3].set_ylabel('[%]')

    axs[1].set_xlabel('Year')
    axs2060[1].set_xlabel('Year')
    axs60100[1].set_xlabel('Year')
    axs020[1].set_xlabel('Year')
    axsabs[3].set_xlabel('Year')
    axsrel[3].set_xlabel('Year')
    
    axs[0].set_xlim([2004-1,2004+length])
    axs020[0].set_xlim([2004-1,2004+length])
    axs2060[0].set_xlim([2004-1,2004+length])
    axs60100[0].set_xlim([2004-1,2004+length])
    axsrel[0].set_xlim([2004-1,2004+length])
    axsabs[0].set_xlim([2004-1,2004+length])

    axs[1].set_xticks(np.arange(2004-1,2004+length+1,1))
    axs020[1].set_xticks(np.arange(2004-1,2004+length+1,1))
    axs2060[1].set_xticks(np.arange(2004-1,2004+length+1,1))
    axs60100[1].set_xticks(np.arange(2004-1,2004+length+1,1))
    axsabs[3].set_xticks(np.arange(2004-1,2004+length+1,1))
    axsrel[3].set_xticks(np.arange(2004-1,2004+length+1,1))
    
    fig.suptitle(regression_title,x=0.5,y=0.98,fontsize=9)
    fig020.suptitle(regression_title+', 0-20 km',x=0.5,y=0.98,fontsize=10)
    fig2060.suptitle(regression_title+', 20-60 km',x=0.5,y=0.98,fontsize=10)
    fig60100.suptitle(regression_title+', 60-100 km',x=0.5,y=0.98,fontsize=10)
    figabs.suptitle(regression_title+' O3 VMR Mean Absolute Differences',x=0.5,y=0.99,fontsize=9)
    figrel.suptitle(regression_title+' O3 VMR Mean Relative Differences',x=0.5,y=1.03,fontsize=9)

    axsabs[0].set_title('All Altitudes',fontsize=7)
    axsabs[3].set_title('0 - 20 km',fontsize=7)
    axsabs[2].set_title('20 - 60 km',fontsize=7)
    axsabs[1].set_title('60 - 100 km',fontsize=7)
    axsrel[0].set_title('All Altitudes',fontsize=7)
    axsrel[3].set_title('0 - 20 km',fontsize=7)
    axsrel[2].set_title('20 - 60 km',fontsize=7)
    axsrel[1].set_title('60 -100 km',fontsize=7)

    mean_absolute_diff_020, mean_absolute_diff_err_020, mean_relative_diff_020, mean_relative_diff_err_020 = [], [], [] , []
    mean_absolute_diff_2060, mean_absolute_diff_err_2060,mean_relative_diff_2060,mean_relative_diff_err_2060= [],[],[],[]
    mean_absolute_diff_60100, mean_absolute_diff_err_60100 , mean_relative_diff_60100, mean_relative_diff_err_60100 = [],[],[],[]
    o3_vmr_mean_absolute_diff, o3_vmr_mean_absolute_diff_err, o3_vmr_mean_relative_diff, o3_vmr_mean_relative_diff_err  = [],[],[],[]
    N_020, N_2060, N_60100, N = [],[],[],[]
    for i in range(0,length,1):
        cm_pair = cm_pairs[i]
        o3_vmr_mean_absolute_diff += [cm_pair.o3_vmr_mean_absolute_diff]
        o3_vmr_mean_absolute_diff_err += [cm_pair.o3_vmr_mean_absolute_diff_err]
        o3_vmr_mean_relative_diff += [cm_pair.o3_vmr_mean_relative_diff] 
        o3_vmr_mean_relative_diff_err += [cm_pair.o3_vmr_mean_relative_diff_err]  
        
        mean_absolute_diff_020 += [cm_pair.mean_absolute_diff[0]]
        mean_absolute_diff_err_020 += [cm_pair.mean_absolute_diff_err[0]]
        mean_relative_diff_020 += [cm_pair.mean_relative_diff[0] ]
        mean_relative_diff_err_020 += [cm_pair.mean_relative_diff_err[0]]  
        mean_absolute_diff_2060 += [cm_pair.mean_absolute_diff[1]]
        mean_absolute_diff_err_2060 += [cm_pair.mean_absolute_diff_err[1]]
        mean_relative_diff_2060 += [cm_pair.mean_relative_diff[1] ]
        mean_relative_diff_err_2060 += [cm_pair.mean_relative_diff_err[1]]  
        mean_absolute_diff_60100 += [cm_pair.mean_absolute_diff[2]]
        mean_absolute_diff_err_60100 += [cm_pair.mean_absolute_diff_err[2]]
        mean_relative_diff_60100 += [cm_pair.mean_relative_diff[2] ]
        mean_relative_diff_err_60100 += [cm_pair.mean_relative_diff_err[2]]  
        
        N += [cm_pair.o3_vmr_N]
        N_020 += [cm_pair.N[0]]
        N_2060 += [cm_pair.N[1]]
        N_60100 += [cm_pair.N[2]]
        
    years = np.arange(2004-1,2004+length+1,1)
    size = len(years)
    for i in range(0,4,1):
        if i<=1:
            axs[i].plot(years, np.zeros(size),linestyle='-',color='k')
            axs020[i].plot(years, np.zeros(size),linestyle='-',color='k')
            axs2060[i].plot(years, np.zeros(size),linestyle='-',color='k')
            axs60100[i].plot(years, np.zeros(size),linestyle='-',color='k')
        axsabs[i].plot(years, np.zeros(size),linestyle='-',color='k')
        axsrel[i].plot(years, np.zeros(size),linestyle='-',color='k')
        
    A=(1/sum(N))*sum(np.multiply(o3_vmr_mean_absolute_diff,N)) 
    B=(1/sum(N))*sum(np.multiply(o3_vmr_mean_relative_diff,N)) 
    C=(1/sum(N_020))*sum(np.multiply(mean_absolute_diff_020,N_020)) 
    D=(1/sum(N_020))*sum(np.multiply(mean_relative_diff_020,N_020)) 
    E=(1/sum(N_2060))*sum(np.multiply(mean_absolute_diff_2060,N_2060)) 
    F=(1/sum(N_2060))*sum(np.multiply(mean_relative_diff_2060,N_2060)) 
    G=(1/sum(N_60100))*sum(np.multiply(mean_absolute_diff_60100,N_60100)) 
    H=(1/sum(N_60100))*sum(np.multiply(mean_relative_diff_60100,N_60100)) 

    A_err=abs(((1/sum(N))*sum(np.multiply( (o3_vmr_mean_absolute_diff_err),N)) ) )
    B_err=abs(((1/sum(N))*sum(np.multiply( (o3_vmr_mean_relative_diff_err),N)) ) )
    C_err=abs(((1/sum(N_020))*sum(np.multiply((mean_absolute_diff_err_020),N_020)) ) )
    D_err=abs(((1/sum(N_020))*sum(np.multiply((mean_relative_diff_err_020),N_020)) ) )
    E_err=abs(((1/sum(N_2060))*sum(np.multiply((mean_absolute_diff_err_2060),N_2060)) ) )
    F_err=abs(((1/sum(N_2060))*sum(np.multiply((mean_relative_diff_err_2060),N_2060)) ) )
    G_err=abs(((1/sum(N_60100))*sum(np.multiply((mean_absolute_diff_err_60100),N_60100)) ) )
    H_err=abs(((1/sum(N_60100))*sum(np.multiply((mean_relative_diff_err_60100),N_60100)) ) )
    
    axsabs[0].plot(years, A*np.ones(size),linestyle='--',color='dimgray')
    axsrel[0].plot(years, B*np.ones(size),linestyle='--',color='dimgray')
    axsabs[3].plot(years, C*np.ones(size) ,linestyle='--',color='dimgray')
    axsrel[3].plot(years, D*np.ones(size),linestyle='--',color='dimgray')
    axsabs[2].plot(years, E*np.ones(size),linestyle='--',color='dimgray')
    axsrel[2].plot(years, F*np.ones(size),linestyle='--',color='dimgray')
    axsabs[1].plot(years, G*np.ones(size),linestyle='--',color='dimgray')
    axsrel[1].plot(years, H*np.ones(size),linestyle='--',color='dimgray')

    axsabs[0].fill_between(years, (A-A_err)*np.ones(size), (A+A_err)*np.ones(size),color='lightgrey')
    axsrel[0].fill_between(years, (B-B_err)*np.ones(size), (B+B_err)*np.ones(size),color='lightgrey')
    axsabs[3].fill_between(years, (C-C_err)*np.ones(size), (C+C_err)*np.ones(size),color='lightgrey')
    axsrel[3].fill_between(years, (D-D_err)*np.ones(size), (D+D_err)*np.ones(size),color='lightgrey')
    axsabs[2].fill_between(years, (E-E_err)*np.ones(size), (E+E_err)*np.ones(size),color='lightgrey')
    axsrel[2].fill_between(years, (F-F_err)*np.ones(size), (F+F_err)*np.ones(size),color='lightgrey')
    axsabs[1].fill_between(years, (G-G_err)*np.ones(size), (G+G_err)*np.ones(size),color='lightgrey')
    axsrel[1].fill_between(years, (H-H_err)*np.ones(size), (H+H_err)*np.ones(size),color='lightgrey')

    axs[0].plot(years, A*np.ones(size),linestyle='--',color='dimgray')
    axs[1].plot(years, B*np.ones(size),linestyle='--',color='dimgray')
    axs[0].fill_between(years, (A-A_err)*np.ones(size), (A+A_err)*np.ones(size),color='lightgrey')
    axs[1].fill_between(years, (B-B_err)*np.ones(size), (B+B_err)*np.ones(size),color='lightgrey')

    axs020[0].plot(years, C*np.ones(size),linestyle='--',color='dimgray')
    axs2060[0].plot(years, E*np.ones(size),linestyle='--',color='dimgray')
    axs60100[0].plot(years, G*np.ones(size),linestyle='--',color='dimgray')
    axs020[1].plot(years, D*np.ones(size),linestyle='--',color='dimgray')
    axs2060[1].plot(years, F*np.ones(size),linestyle='--',color='dimgray')
    axs60100[1].plot(years, H*np.ones(size),linestyle='--',color='dimgray')

    axs020[0].fill_between(years, (C-C_err)*np.ones(size), (C+C_err)*np.ones(size),color='lightgrey')
    axs2060[0].fill_between(years, (E-E_err)*np.ones(size), (E+E_err)*np.ones(size),color='lightgrey')
    axs60100[0].fill_between(years, (G-G_err)*np.ones(size), (G+G_err)*np.ones(size),color='lightgrey')
    axs020[1].fill_between(years, (D-D_err)*np.ones(size), (D+D_err)*np.ones(size),color='lightgrey')
    axs2060[1].fill_between(years, (F-F_err)*np.ones(size), (F+F_err)*np.ones(size),color='lightgrey')
    axs60100[1].fill_between(years, (H-H_err)*np.ones(size), (H+H_err)*np.ones(size),color='lightgrey')
                            
    years = np.arange(2004,2004+length,1)
    axs[0].errorbar(years,o3_vmr_mean_absolute_diff,o3_vmr_mean_absolute_diff_err,marker='o',capsize=3,elinewidth=1,ecolor='firebrick',markerfacecolor='tomato',markeredgecolor='firebrick',linestyle='None')
    axs020[0].errorbar(years,mean_absolute_diff_020,mean_absolute_diff_err_020,marker='o',capsize=3,elinewidth=1,ecolor='firebrick',markerfacecolor='tomato',markeredgecolor='firebrick',linestyle='None')
    axs2060[0].errorbar(years,mean_absolute_diff_2060,mean_absolute_diff_err_2060,marker='o',capsize=3,elinewidth=1,ecolor='firebrick',markerfacecolor='tomato',markeredgecolor='firebrick',linestyle='None')
    axs60100[0].errorbar(years,mean_absolute_diff_60100,mean_absolute_diff_err_60100,marker='o',capsize=3,elinewidth=1,ecolor='firebrick',markerfacecolor='tomato',markeredgecolor='firebrick',linestyle='None')
    
    axs[1].errorbar(years,o3_vmr_mean_relative_diff,o3_vmr_mean_relative_diff_err,marker='o',capsize=3,elinewidth=1,ecolor='darkcyan',markerfacecolor='deepskyblue',markeredgecolor='darkcyan',linestyle='None')
    axs020[1].errorbar(years,mean_relative_diff_020,mean_relative_diff_err_020,marker='o',capsize=3,elinewidth=1,ecolor='darkcyan',markerfacecolor='deepskyblue',markeredgecolor='darkcyan',linestyle='None')
    axs2060[1].errorbar(years,mean_relative_diff_2060,mean_relative_diff_err_2060,marker='o',capsize=3,elinewidth=1,ecolor='darkcyan',markerfacecolor='deepskyblue',markeredgecolor='darkcyan',linestyle='None')
    axs60100[1].errorbar(years,mean_relative_diff_60100,mean_relative_diff_err_60100,marker='o',capsize=3,elinewidth=1,ecolor='darkcyan',markerfacecolor='deepskyblue',markeredgecolor='darkcyan',linestyle='None')

    axs[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs020[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs2060[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs60100[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    axsrel[0].errorbar(years,o3_vmr_mean_relative_diff,o3_vmr_mean_relative_diff_err,markersize=2,marker='o',capsize=3,elinewidth=1,ecolor='indigo',markerfacecolor='purple',markeredgecolor='indigo',linestyle='None')
    axsrel[3].errorbar(years,mean_relative_diff_020,mean_relative_diff_err_020,marker='o',markersize=2,capsize=3,elinewidth=1,ecolor='crimson',markerfacecolor='mediumvioletred',markeredgecolor='crimson',linestyle='None')
    axsrel[2].errorbar(years,mean_relative_diff_2060,mean_relative_diff_err_2060,marker='o',markersize=4,capsize=3,elinewidth=1,ecolor='crimson',markerfacecolor='mediumvioletred',markeredgecolor='crimson',linestyle='None')
    axsrel[1].errorbar(years,mean_relative_diff_60100,mean_relative_diff_err_60100,marker='o',markersize=5,capsize=3,elinewidth=1,ecolor='crimson',markerfacecolor='mediumvioletred',markeredgecolor='crimson',linestyle='None')

    axsabs[0].errorbar(years,o3_vmr_mean_absolute_diff,o3_vmr_mean_absolute_diff_err,marker='o',capsize=3,elinewidth=1,ecolor='indigo',markerfacecolor='purple',markeredgecolor='indigo',linestyle='None')
    axsabs[3].errorbar(years,mean_absolute_diff_020,mean_absolute_diff_err_020,marker='o',capsize=3,elinewidth=1,ecolor='crimson',markerfacecolor='mediumvioletred',markeredgecolor='crimson',linestyle='None')
    axsabs[2].errorbar(years,mean_absolute_diff_2060,mean_absolute_diff_err_2060,marker='o',capsize=3,elinewidth=1,ecolor='crimson',markerfacecolor='mediumvioletred',markeredgecolor='crimson',linestyle='None')
    axsabs[1].errorbar(years,mean_absolute_diff_60100,mean_absolute_diff_err_60100,marker='o',capsize=3,elinewidth=1,ecolor='crimson',markerfacecolor='mediumvioletred',markeredgecolor='crimson',linestyle='None')

    axsabs[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axsabs[1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axsabs[2].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axsabs[3].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    yabs_max = abs(max(axsabs[0].get_ylim(), key=abs))
    axsabs[0].set_ylim(ymin=-yabs_max, ymax=yabs_max)
    yabs_max = abs(max(axsabs[1].get_ylim(), key=abs))
    axsabs[1].set_ylim(ymin=-yabs_max, ymax=yabs_max)
    yabs_max = abs(max(axsabs[2].get_ylim(), key=abs))
    axsabs[2].set_ylim(ymin=-yabs_max, ymax=yabs_max)
    yabs_max = abs(max(axsabs[3].get_ylim(), key=abs))
    axsabs[3].set_ylim(ymin=-yabs_max, ymax=yabs_max)
    
    yrel_max = abs(max(axsrel[0].get_ylim(), key=abs))
    axsrel[0].set_ylim(ymin=-yrel_max, ymax=yrel_max)
    yrel_max = abs(max(axsrel[1].get_ylim(), key=abs))
    axsrel[1].set_ylim(ymin=-yrel_max, ymax=yrel_max)
    yrel_max = abs(max(axsrel[2].get_ylim(), key=abs))
    axsrel[2].set_ylim(ymin=-yrel_max, ymax=yrel_max)
    yrel_max = abs(max(axsrel[3].get_ylim(), key=abs))
    axsrel[3].set_ylim(ymin=-yrel_max, ymax=yrel_max)

    axsrel[0].yaxis.set_minor_locator(MultipleLocator(10))
    axsrel[1].yaxis.set_minor_locator(MultipleLocator(25))
    axsrel[2].yaxis.set_minor_locator(MultipleLocator(10))
    axsrel[3].yaxis.set_minor_locator(MultipleLocator(25))

    # fig.tight_layout()
    # fig020.tight_layout()
    # fig2060.tight_layout()
    # fig60100.tight_layout()
    # figabs.tight_layout()
    # figrel.tight_layout()
    
    fig.savefig('Mean ab and rel differences '+regression_title+'.png') # Save figure.
    fig020.savefig('Mean ab and rel differences, '+regression_title+' 0-20km.png') # Save figure.
    fig2060.savefig('Mean ab and rel differences, '+regression_title+' 20-60km.png') # Save figure.
    fig60100.savefig('Mean ab and rel differences, '+regression_title+' 60-100km.png') # Save figure.
    figabs.savefig('Mean ab differences, '+regression_title+'.png') # Save figure.
    figrel.savefig('Mean rel differences, '+regression_title+'.png') # Save figure.

    return 
