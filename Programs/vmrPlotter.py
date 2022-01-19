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
import numpy 
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm_mat
import os

# vmrPlotter:
# INPUT:
# cm: Array of 2-length arrays. In each 2-length array is a measurement object for each of the two instruments being compared.
# regression_title: String. Title of the regression plot.
# abs_diff_title: String. Title of absolute difference scatter plot of .
# regression_labels: Array with two indices: [ xlabel, ylabel], where xlabel and ylabel are strings.
# folder: String; the name of the directory where we would like to save the figures. 
# OUTPUT: This function produces and saves figures of volume mixing ratio linear regression (shown as (a) a scatter plot, and (b) a histogram)
#  and absolute differences over time (scatter plot) over time. The three figures are saved into 'folder'.

# vmrColorbar:
# INPUT:
# cm: Array of 2-length arrays. In each 2-length array is a measurement object for each of the two instruments being compared.
# regression_title: String. Title of the regression plot.
# regression_labels: Array with two indices: [ xlabel, ylabel], where xlabel and ylabel are strings.
# folder: String; the name of the directory where we would like to save the figures. 
# OUTPUT: This function produces and saves figures of volume mixing ratio linear regression (shown as a scatter plot) 
# with a colorbar indicating point altitude. The figure is saved into 'folder'.


def vmrPlotter(cm_pair,cm,regression_title,abs_diff_title,regression_labels,year):
    # Unpack the cm_pair input pair object. 
    R2 = cm_pair.o3_vmr_R2 
    RMSD = cm_pair.o3_vmr_RMSD 
    o3_vmr_mean_absolute_diff = cm_pair.o3_vmr_mean_absolute_diff
    o3_vmr_mean_absolute_diff_err = cm_pair.o3_vmr_mean_absolute_diff_err
    o3_vmr_mean_relative_diff = cm_pair.o3_vmr_mean_relative_diff 
    o3_vmr_mean_relative_diff_err = cm_pair.o3_vmr_mean_relative_diff_err  
    m , b = cm_pair.o3_vmr_ols[0], cm_pair.o3_vmr_ols[1]  # Slope m, y-intercept b OLS
    m0, b0 = cm_pair.o3_vmr_rma[0], cm_pair.o3_vmr_rma[1]  # Slope m, y-intercept b OLS
    x_ols, y_ols = cm_pair.o3_vmr_ols_arr[0], cm_pair.o3_vmr_ols_arr[1]  # [ [xarray], [yarray]]
    x_rma, y_rma = cm_pair.o3_vmr_rma_arr[0], cm_pair.o3_vmr_rma_arr[1] 
    x_ideal, y_ideal = cm_pair.ideal_arr[0], cm_pair.ideal_arr[1] # Ideal 1-1 relationship 
    o3_vmr_N = cm_pair.o3_vmr_N 
    
    a0,a1 = cm_pair.o3_vmr_meas[0], cm_pair.o3_vmr_meas[1]
    a0e,a1e = cm_pair.o3_vmr_meas_errors[0], cm_pair.o3_vmr_meas_errors[1]
    a0t,a1t = cm_pair.o3_vmr_meas_datetime[0], cm_pair.o3_vmr_meas_datetime[1]

    print('VMR RMSD',RMSD)
    print('VMR R^2',R2)
    print('VMR Mean Relative Difference',o3_vmr_mean_relative_diff,'+-',o3_vmr_mean_relative_diff_err)
    print('VMR Mean Absolute Difference',o3_vmr_mean_absolute_diff,'+-',o3_vmr_mean_absolute_diff_err)    
    print('N VMR points',o3_vmr_N) # The length of the list of absolute differences is the number of coincident measurements.
    print('OLS',m,b,'RMA',m0,b0)
    
    # Create a scatter plot (linear regression).
    fig1 = plt.figure()  # create a figure object
    ax1 = fig1.add_subplot(1, 1, 1)  # create an axes object in the figure

    ax1.scatter(x=a0,y=a1,marker='o',c='green',s=0.5)
    ax1.plot(x_ideal,y_ideal,'k',lw=4)
    ax1.plot(x_rma,y_rma,'--b',lw=2)
    ax1.plot(x_ols,y_ols,'--r',lw=2)
    if type(regression_title==str): # Add labels to the regression plot.
        ax1.set_title(regression_title, y=1.05)
    if type(regression_labels[0])==str:
        ax1.set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:
        ax1.set_ylabel(regression_labels[1])
         
    ols = 'y = '+str( "%.3f" % m )+'x + '+str( "{:.3e}".format(b)) # Write OLS linear fit in y = mx + b form.
    rma= 'y = '+str( "%.3f" % m0 )+'x + '+str( "{:.3e}".format(b0) ) # Write RMA linear fit in y = mx + b form.
    Rp = 'R.^2 = ' + str( "%.4f" % R2 ) # Pearson coefficient.      
    ax1.text(0.1e-5,3.1e-5,ols,color='red') # Add text labels for regression.
    ax1.text(0.1e-5,2.8e-5,rma,color='blue')
    ax1.text(0.1e-5,2.5e-5,Rp,color='black')
    ax1.set_xlim([0,3.5e-5])
    ax1.set_ylim([0,3.5e-5])
    filenamepng = regression_title + ' Regression '+str(year)+'.png' # Create name for png plot file.
    print('Saving relation plot of VMR pairs')
    fig1.savefig(filenamepng) # Save figure.

    ###
    # Create a plot of VMR absolute differences.   
    y_= numpy.ones(len(a0t))*o3_vmr_mean_absolute_diff
    z_= numpy.zeros(len(a0t))
    differences = numpy.array(a0) - numpy.array(a1)
    differences_error = numpy.array(a0e) - numpy.array(a1e)

    fig2 = plt.figure()  # create a figure object
    ax2 = fig2.add_subplot(1, 1, 1)  # create an axes object in the figure
    ax2.plot(a0t,y_,c='b',lw=1) # delta_abs
    ax2.plot(a0t,z_,'k',linewidth=1.0) # 0 DU difference line (ideal).
    ax2.scatter(a0t,differences,marker='o',s=2,c='blueviolet')
    #ax2.errorbar(x=a0t,y=differences,yerr=differences_error,marker='o',markersize=2,linestyle='none',capsize=1,elinewidth=0.5,ecolor='black',markerfacecolor='blueviolet',markeredgecolor='black')
    ax2.set_xlabel('Date') # Add x and y labels.
    fig2.autofmt_xdate()
    ax2.set_ylabel('Absolute Difference [ppv]')
    if regression_labels[0]!='ACE-MAESTRO-VIS (3.13) (ppv)':
        ax2.set_ylim([-1e-2,1e-1])
    else:
        ax2.set_ylim([-1e-1,1e-2])

    filenamepng = 'Absolute Differences time series '+str(year)+'.png'
         
    print('Saving absolute differences time series')
    fig2.savefig(filenamepng) # Save figure.
          
    return # Return updates comparison pair. 


def vmrColorbar(cm_pair,cm,regression_title,regression_labels,folder,year):
    # Unpack the cm_pair input pair object. 
    R2 = cm_pair.o3_vmr_R2 
    RMSD = cm_pair.o3_vmr_RMSD 
    o3_vmr_mean_absolute_diff = cm_pair.o3_vmr_mean_absolute_diff
    o3_vmr_mean_absolute_diff_err = cm_pair.o3_vmr_mean_absolute_diff_err
    o3_vmr_mean_relative_diff = cm_pair.o3_vmr_mean_relative_diff 
    o3_vmr_mean_relative_diff_err = cm_pair.o3_vmr_mean_relative_diff_err  
    m1 , b1 = cm_pair.o3_vmr_ols[0], cm_pair.o3_vmr_ols[1]  # Slope m, y-intercept b OLS
    m0, b0 = cm_pair.o3_vmr_rma[0], cm_pair.o3_vmr_rma[1]  # Slope m, y-intercept b OLS
    x_ols, y_ols = cm_pair.o3_vmr_ols_arr[0], cm_pair.o3_vmr_ols_arr[1]  # [ [xarray], [yarray]]
    x_rma, y_rma = cm_pair.o3_vmr_rma_arr[0], cm_pair.o3_vmr_rma_arr[1] 
    x_ideal, y_ideal = cm_pair.ideal_arr[0], cm_pair.ideal_arr[1] # Ideal 1-1 relationship 
    o3_vmr_N = cm_pair.o3_vmr_N 
    
    a0,a1 = cm_pair.o3_vmr_meas[0], cm_pair.o3_vmr_meas[1]
    a0e,a1e = cm_pair.o3_vmr_meas_errors[0], cm_pair.o3_vmr_meas_errors[1]
    a0t,a1t = cm_pair.o3_vmr_meas_altitudes[0], cm_pair.o3_vmr_meas_altitudes[1]
    if type(cm)==list: # Check that the coincident measurement (cm) input is a list.
        # Plot instrument pair coincidences   
        if len(a0)!=0 and len(a1)!=0: # Only create plot if there is a list of coincident measurements.
           x=a0
           y=a1
           z=a0t
           
           fig, ax = plt.subplots(1, 1)
           df=pd.DataFrame(data={'A':x,'B':y,'C':z})
           points = ax.scatter(df.A, df.B, c=df.C,cmap="jet", vmin=0, vmax=100, lw=0, s=1)
           # Colorbar Legend
           cbar = fig.colorbar(points).set_label('Altitude [km]', rotation=270,x=1.5,labelpad=13)

           m = cm_mat.ScalarMappable(cmap=cm_mat.jet,)
           ax.set_ylim([0,3.5e-5]) # Set x and y axis limits.
           ax.set_xlim([0,3.5e-5])
           ax.ticklabel_format(axis='both',style='sci')
           # Plot ideal 1:1 fit. 
           ax.plot(x_ideal,y_ideal,'k',lw=4)
           # Plot ordinary least squares fit.
           ax.plot(x_ols,y_ols,'--r',lw=2)
           # Plot standard major axis fit. 
           ax.plot(x_rma,y_rma,'--b',lw=2)
     
           ols = 'y = '+str( "%.3f" % m1 )+'x + '+str( "{:.3e}".format(b1)) # Write OLS linear fit in y = mx + b form.
           rma= 'y = '+str( "%.3f" % m0 )+'x + '+str( "{:.3e}".format(b0) ) # Write RMA linear fit in y = mx + b form.
           Rp = 'R.^2 = ' + str( "%.4f" % R2 ) # Pearson coefficient.      
           ax.text(0.1e-5,3.1e-5,ols,color='red') # Add text labels for regression.
           ax.text(0.1e-5,2.8e-5,rma,color='blue')
           ax.text(0.1e-5,2.5e-5,Rp,color='black')

           if type(regression_title==str): # Add labels to the regression plot.
               ax.set_title(regression_title, y=1.05)
           if type(regression_labels[0])==str: # X label is in 0 index.
               ax.set_xlabel(regression_labels[0])
           if type(regression_labels[1])==str:# Y label is in 1 index.
               ax.set_ylabel(regression_labels[1])
          
           filenamepng = regression_title + ' Altitude Colorbar '+str(year)+'.png' # Create name for png plot file.
           fig.savefig(filenamepng) # Save figure.
    return 
   