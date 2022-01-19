# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 15:17:59 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: Feb 18 2021.
"""
# timeScatter
# This function takes in 4 'pair' class objects, and scatters their mean relative differences
# over the years. The figure is neither closed nor saved.
# INPUT:
# a,b,c,d: 'Pair' class objects, whose 'mean relative difference' attributes are to be plotted.
# OUTPUT: N/A

import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

def timeScatter(pairs): # Input a list of pair objects
    years = np.linspace(2004,2004+len(pairs),1) # Years included in the study
    altitudes = np.linspace(0,100,0.5) # Altitude grid for ACE-MAESTRO
    C = []# Average difference of UV-VIS O3 VMR measurements
    for i in range(0,len(pairs),1): # Cycle through each pair
        cm_pair = pairs[i]
        average_differences = np.zeros(len(altitudes))
        N = np.zeros(len(altitudes))
        # Unpack the cm_pair input pair object. 
        o3_vmr_mean_absolute_diff = cm_pair.o3_vmr_mean_absolute_diff
        o3_vmr_mean_absolute_diff_err = cm_pair.o3_vmr_mean_absolute_diff_err
        o3_vmr_mean_relative_diff = cm_pair.o3_vmr_mean_relative_diff 
        o3_vmr_mean_relative_diff_err = cm_pair.o3_vmr_mean_relative_diff_err  
        o3_vmr_N = cm_pair.o3_vmr_N 
    
        a0,a1 = cm_pair.o3_vmr_meas[0], cm_pair.o3_vmr_meas[1]
        a0e,a1e = cm_pair.o3_vmr_meas_errors[0], cm_pair.o3_vmr_meas_errors[1]
        a0t,a1t = cm_pair.o3_vmr_meas_datetime[0], cm_pair.o3_vmr_meas_datetime[1]
        a0_alt, a1_alt = cm_pair.o3_vmr_meas_altitudes[0], cm_pair.o3_vmr_meas_altitudes[1]
        for j in range(0,len(a0),1): # Sum all the differences being considered. 
            curr_altitude = a0_alt[j]
            # Corresponding index in average_differences is curr_altitude/0.5
            idx = curr_altitude/0.5
            average_differences[idx] = average_differences[idx] + (a0[j]-a1[j]) 
            N[idk] = N[idk] + 1
        for k in range(0,len(N),1): # Finish computing average by dividing by number of samples.
            if N[k]!=0:
                average_differences[k] = average_differences[k]/N[k]
        C = C + [average_differences]
    ######
    # Create grid of differences
    differences = np.array([C[0]; C[1]; C[2]; C[3]; C[4]; C[5]; C[6]; C[7]; C[8]])
    
    fig = plt.figure(dpi=80)
    ax = fig.add_subplot(1,1,1)
    ax.pcolormesh([years, altitudes], differences)
    # ax.errorbar(a_diff, a0t, a_diff_err,marker='o',linestyle='none',capsize=1,elinewidth=1,ecolor='black',markerfacecolor='green',markeredgecolor='black')
    return 