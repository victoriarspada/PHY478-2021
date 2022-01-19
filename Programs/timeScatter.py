# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 15:17:59 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: August 14 2020.
"""
# timeScatter
# This function takes in 4 'pair' class objects, and scatters their mean relative differences
# over the years. The figure is neither closed nor saved.
# INPUT:
# a,b,c,d: 'Pair' class objects, whose 'mean relative difference' attributes are to be plotted.
# OUTPUT: N/A

import matplotlib.pyplot as plt

def timeScatter(a): # Input a pair object
    # Unpack the cm_pair input pair object. 
    o3_vmr_mean_absolute_diff = cm_pair.o3_vmr_mean_absolute_diff
    o3_vmr_mean_absolute_diff_err = cm_pair.o3_vmr_mean_absolute_diff_err
    o3_vmr_mean_relative_diff = cm_pair.o3_vmr_mean_relative_diff 
    o3_vmr_mean_relative_diff_err = cm_pair.o3_vmr_mean_relative_diff_err  
    o3_vmr_N = cm_pair.o3_vmr_N 
    
    a0,a1 = cm_pair.o3_vmr_meas[0], cm_pair.o3_vmr_meas[1]
    a0e,a1e = cm_pair.o3_vmr_meas_errors[0], cm_pair.o3_vmr_meas_errors[1]
    a0t,a1t = cm_pair.o3_vmr_meas_datetime[0], cm_pair.o3_vmr_meas_datetime[1]
    ######
    a_diff = list( np.array(a0) - np.array(a1) )
    a_diff_err = []

     years=[2004,2005,2006,2007,2008,2009,2010,2011]
     print(a)
     print((a.mean_relative_diff_arr), (a.mean_relative_diff_err_arr))
     fig = plt.figure(dpi=80)
     ax = fig.add_subplot(1,1,1)
     ax.errorbar(a_diff, a0t, a_diff_err,marker='o',linestyle='none',capsize=1,elinewidth=1,ecolor='black',markerfacecolor='green',markeredgecolor='black')
     return 