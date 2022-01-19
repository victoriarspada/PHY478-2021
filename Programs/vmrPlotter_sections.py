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

def vmrPlotter_sections(cm_pair,cm,regression_title,regression_labels,year):
    # Unpack the cm_pair input pair object. This code only works for one cmpair
    R2 = cm_pair.R2 
    RMSD = cm_pair.RMSD 
    o3_vmr_mean_absolute_diff = cm_pair.mean_absolute_diff
    o3_vmr_mean_absolute_diff_err = cm_pair.mean_absolute_diff_err
    o3_vmr_mean_relative_diff = cm_pair.mean_relative_diff 
    o3_vmr_mean_relative_diff_err = cm_pair.mean_relative_diff_err  
    ols_params = cm_pair.ols  # Slope m, y-intercept b OLS
    rma_params = cm_pair.rma  # Slope m, y-intercept b OLS
    xy_ols = cm_pair.ols_arr  # [ [xarray], [yarray]]
    xy_rma = cm_pair.rma_arr
    x_ideal, y_ideal = cm_pair.ideal_arr[0], cm_pair.ideal_arr[1] # Ideal 1-1 relationship 
    o3_vmr_N = cm_pair.N 
    
    a0_1,a1_1 = cm_pair.meas[0][0], cm_pair.meas[0][1]
    a0e_1,a1e_1 = cm_pair.meas_errors[0][0], cm_pair.meas_errors[0][1]
    a0_alt_1 = cm_pair.meas_altitudes[0][1]

    a0_2,a1_2 = cm_pair.meas[1][0], cm_pair.meas[1][1]
    a0e_2,a1e_2 = cm_pair.meas_errors[1][0], cm_pair.meas_errors[1][1]
    a0_alt_2 = cm_pair.meas_altitudes[1][1]

    a0_3,a1_3 = cm_pair.meas[2][0], cm_pair.meas[2][1]
    a0e_3,a1e_3 = cm_pair.meas_errors[2][0], cm_pair.meas_errors[2][1]
    a0_alt_3 = cm_pair.meas_altitudes[2][1]

    print('0-20 km')
    print('VMR RMSD',RMSD[0])
    print('VMR R^2',R2[0])  
    print('VMR Mean Relative Difference',o3_vmr_mean_relative_diff[0],'+-',o3_vmr_mean_relative_diff_err[0])
    print('VMR Mean Absolute Difference',o3_vmr_mean_absolute_diff[0],'+-',o3_vmr_mean_absolute_diff_err[0])    
    print('N VMR points',o3_vmr_N[0]) # The length of the list of absolute differences is the number of coincident measurements.
    print('OLS',ols_params[0][0],ols_params[0][1],'RMA',rma_params[0][0],rma_params[0][1])

    print('20-60 km')
    print('VMR RMSD',RMSD[1])
    print('VMR R^2',R2[1])  
    print('VMR Mean Relative Difference',o3_vmr_mean_relative_diff[1],'+-',o3_vmr_mean_relative_diff_err[1])
    print('VMR Mean Absolute Difference',o3_vmr_mean_absolute_diff[1],'+-',o3_vmr_mean_absolute_diff_err[1])    
    print('N VMR points',o3_vmr_N[1]) # The length of the list of absolute differences is the number of coincident measurements.
    print('OLS',ols_params[1][0],ols_params[1][1],'RMA',rma_params[1][0],rma_params[1][1])

    print('60-100 km')
    print('VMR RMSD',RMSD[2])
    print('VMR R^2',R2[2])  
    print('VMR Mean Relative Difference',o3_vmr_mean_relative_diff[2],'+-',o3_vmr_mean_relative_diff_err[2])
    print('VMR Mean Absolute Difference',o3_vmr_mean_absolute_diff[2],'+-',o3_vmr_mean_absolute_diff_err[2])    
    print('N VMR points',o3_vmr_N[2]) # The length of the list of absolute differences is the number of coincident measurements.
    print('OLS',ols_params[2][0],ols_params[2][1],'RMA',rma_params[2][0],rma_params[2][1])
    
    # Create a scatter plot (linear regression), no colorbar.
    fig, axs = plt.subplots(1, 3,figsize=[14, 4],dpi=100) # Non-colorbar regression plot
    fig1, axs1 = plt.subplots(1, 3,figsize=[14, 4],dpi=100) # Colorbar plot
    
    i=0
    axs[i].scatter(x=a0_1,y=a1_1,marker='o',c='green',s=0.5)
    axs[i].plot(x_ideal,y_ideal,'k',lw=4)
    axs[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    axs[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    axs[i].set_title('Altitudes 0-20 km', y=1.05)
    if type(regression_labels[0])==str:
        axs[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:
        axs[i].set_ylabel(regression_labels[1])      
    ols = 'y = '+str( "%.3f" % ols_params[i][0] )+'x + '+str( "{:.3e}".format(ols_params[i][1])) # Write OLS linear fit in y = mx + b form.
    rma= 'y = '+str( "%.3f" % rma_params[i][0] )+'x + '+str( "{:.3e}".format(rma_params[i][1]) ) # Write RMA linear fit in y = mx + b form.
    Rp = 'R.^2 = ' + str( "%.4f" % R2[i] ) # Pearson coefficient.      
    axs[i].text(0.1e-5,3.1e-5,ols,color='red') # Add text labels for regression.
    axs[i].text(0.1e-5,2.8e-5,rma,color='blue')
    axs[i].text(0.1e-5,2.5e-5,Rp,color='black')
    axs[i].set_xlim([0,3.5e-5])
    axs[i].set_ylim([0,3.5e-5])
    
    
    df=pd.DataFrame(data={'A':a0_1,'B':a1_1,'C':a0_alt_1})
    points = axs1[i].scatter(df.A, df.B, c=df.C,cmap="jet", vmin=0, vmax=100, lw=0, s=1)
    axs1[i].ticklabel_format(axis='both',style='sci')
    # Plot ideal 1:1 fit. 
    axs1[i].plot(x_ideal,y_ideal,'k',lw=4)
    # Plot ordinary least squares fit.
    axs1[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    # Plot standard major axis fit. 
    axs1[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    axs1[i].text(0.1e-5,3.1e-5,ols,color='red') # Add text labels for regression.
    axs1[i].text(0.1e-5,2.8e-5,rma,color='blue')
    axs1[i].text(0.1e-5,2.5e-5,Rp,color='black')
    axs1[i].set_title('Altitudes 0-20 km', y=1.05)
    if type(regression_labels[0])==str: # X label is in 0 index.
        axs1[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:# Y label is in 1 index.
        axs1[i].set_ylabel(regression_labels[1])
    axs1[i].set_ylim([0,3.5e-5]) # Set x and y axis limits.
    axs1[i].set_xlim([0,3.5e-5])

    
    i=1
    axs[i].scatter(x=a0_2,y=a1_2,marker='o',c='green',s=0.5)
    axs[i].plot(x_ideal,y_ideal,'k',lw=4)
    axs[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    axs[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    axs[i].set_title('Altitudes 20-60 km', y=1.05)
    if type(regression_labels[0])==str:
        axs[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:
        axs[i].set_ylabel(regression_labels[1])      
    ols = 'y = '+str( "%.3f" % ols_params[i][0] )+'x + '+str( "{:.3e}".format(ols_params[i][1])) # Write OLS linear fit in y = mx + b form.
    rma= 'y = '+str( "%.3f" % rma_params[i][0] )+'x + '+str( "{:.3e}".format(rma_params[i][1]) ) # Write RMA linear fit in y = mx + b form.
    Rp = 'R.^2 = ' + str( "%.4f" % R2[i] ) # Pearson coefficient.      
    axs[i].text(0.1e-5,3.1e-5,ols,color='red') # Add text labels for regression.
    axs[i].text(0.1e-5,2.8e-5,rma,color='blue')
    axs[i].text(0.1e-5,2.5e-5,Rp,color='black')
    axs[i].set_xlim([0,3.5e-5])
    axs[i].set_ylim([0,3.5e-5])


    df=pd.DataFrame(data={'A':a0_2,'B':a1_2,'C':a0_alt_2})
    points = axs1[i].scatter(df.A, df.B, c=df.C,cmap="jet", vmin=0, vmax=100, lw=0, s=1)
    # Colorbar Legend
    axs1[i].set_ylim([0,3.5e-5]) # Set x and y axis limits.
    axs1[i].set_xlim([0,3.5e-5])
    axs1[i].ticklabel_format(axis='both',style='sci')
    # Plot ideal 1:1 fit. 
    axs1[i].plot(x_ideal,y_ideal,'k',lw=4)
    # Plot ordinary least squares fit.
    axs1[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    # Plot standard major axis fit. 
    axs1[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    axs1[i].text(0.1e-5,3.1e-5,ols,color='red') # Add text labels for regression.
    axs1[i].text(0.1e-5,2.8e-5,rma,color='blue')
    axs1[i].text(0.1e-5,2.5e-5,Rp,color='black')
    axs1[i].set_title('Altitudes 20-60 km', y=1.05)
    if type(regression_labels[0])==str: # X label is in 0 index.
        axs1[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:# Y label is in 1 index.
        axs1[i].set_ylabel(regression_labels[1])

    
    i=2
    axs[i].scatter(x=a0_3,y=a1_3,marker='o',c='green',s=0.5)
    axs[i].plot(x_ideal,y_ideal,'k',lw=4)
    axs[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    axs[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    axs[i].set_title('Altitudes 60-100 km', y=1.05)
    if type(regression_labels[0])==str:
        axs[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:
        axs[i].set_ylabel(regression_labels[1])      
    ols = 'y = '+str( "%.3f" % ols_params[i][0] )+'x + '+str( "{:.3e}".format(ols_params[i][1])) # Write OLS linear fit in y = mx + b form.
    rma= 'y = '+str( "%.3f" % rma_params[i][0] )+'x + '+str( "{:.3e}".format(rma_params[i][1]) ) # Write RMA linear fit in y = mx + b form.
    Rp = 'R.^2 = ' + str( "%.5f" % R2[i] ) # Pearson coefficient.      
    axs[i].text(0.5e-5,3.1e-5,ols,color='red',fontsize=8) # Add text labels for regression.
    axs[i].text(0.5e-5,2.8e-5,rma,color='blue',fontsize=8)
    axs[i].text(0.5e-5,2.5e-5,Rp,color='black',fontsize=8)
    axs[i].set_xlim([0,3.5e-5])
    axs[i].set_ylim([0,3.5e-5])


    df=pd.DataFrame(data={'A':a0_3,'B':a1_3,'C':a0_alt_3})
    points = axs1[i].scatter(df.A, df.B, c=df.C,cmap="jet", vmin=0, vmax=100, lw=0, s=1)
    # Colorbar Legend
    cbar = fig1.colorbar(points).set_label('Altitude [km]', rotation=270,x=1.5,labelpad=13)
    m = cm_mat.ScalarMappable(cmap=cm_mat.jet,)
    axs1[i].set_ylim([0,3.5e-5]) # Set x and y axis limits.
    axs1[i].set_xlim([0,3.5e-5])
    axs1[i].ticklabel_format(axis='both',style='sci')
    # Plot ideal 1:1 fit. 
    axs1[i].plot(x_ideal,y_ideal,'k',lw=4)
    # Plot ordinary least squares fit.
    axs1[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    # Plot standard major axis fit. 
    axs1[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    axs[i].text(0.5e-5,3.1e-5,ols,color='red',fontsize=5) # Add text labels for regression.
    axs[i].text(0.5e-5,2.8e-5,rma,color='blue',fontsize=5)
    axs[i].text(0.5e-5,2.5e-5,Rp,color='black',fontsize=5)
    axs1[i].set_title('Altitudes 60-100 km', y=1.05)
    if type(regression_labels[0])==str: # X label is in 0 index.
        axs1[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:# Y label is in 1 index.
        axs1[i].set_ylabel(regression_labels[1])

    fig.tight_layout()
    filenamepng = regression_title + ' Regression (sections) '+str(year)+'.png' # Create name for png plot file.
    print('Saving relation plot of VMR pairs')
    fig.savefig(filenamepng) # Save figure.
    
    filenamepng = regression_title + ' Altitude Colorbar (sections) '+str(year)+'.png' # Create name for png plot file
    fig1.savefig(filenamepng) # Save figure.
    return 
   
def vmrPlotter_sections_ALL(cm_pair,regression_title,regression_labels):
    # Unpack the cm_pair input pair object. 
    R2 = []
    RMSD = []
    o3_vmr_mean_absolute_diff = []
    o3_vmr_mean_absolute_diff_err = []
    o3_vmr_mean_relative_diff = []
    o3_vmr_mean_relative_diff_err = []  
    ols_params = [0,0]  # Slope m, y-intercept b OLS
    rma_params = [0,0]  # Slope m, y-intercept b OLS
    # xy_ols = cm_pair[0].ols_arr  # [ [xarray], [yarray]]
    # xy_rma = cm_pair[0].rma_arr
    x_ideal, y_ideal = cm_pair[0].ideal_arr[0], cm_pair[0].ideal_arr[1] # Ideal 1-1 relationship 
    o3_vmr_N = [] 
    
    a0_1,a1_1=[],[]
    a0e_1,a1e_1 = [], []
    a0_alt_1 = []
    a0_2,a1_2 = [],[]
    a0e_2,a1e_2 = [], []
    a0_alt_2 = []
    a0_3,a1_3 = [],[]
    a0e_3,a1e_3 = [],[]
    a0_alt_3 = []
    
    for i in range(0,len(cm_pair),1):
        a0_1 = a0_1 + cm_pair[i].meas[0][0]
        a1_1 = a1_1 + cm_pair[i].meas[0][1]
        a0e_1 = a0e_1 + cm_pair[i].meas_errors[0][0]
        a1e_1 = a1e_1 + cm_pair[i].meas_errors[0][1]
        a0_alt_1 = a0_alt_1 + cm_pair[i].meas_altitudes[0][1]

        a0_2 = a0_2 + cm_pair[i].meas[1][0]
        a1_2 = a1_2 + cm_pair[i].meas[1][1]
        a0e_2 = a0e_2 + cm_pair[i].meas_errors[1][0]
        a1e_2 = a1e_2 + cm_pair[i].meas_errors[1][1]
        a0_alt_2 = a0_alt_2 + cm_pair[i].meas_altitudes[1][1]

        a0_3 = a0_3 + cm_pair[i].meas[2][0]
        a1_3 = a1_3 + cm_pair[i].meas[2][1]
        a0e_3 = a0e_3 + cm_pair[i].meas_errors[2][0]
        a1e_3 = a1e_3 + cm_pair[i].meas_errors[2][1]
        a0_alt_3 = a0_alt_3 + cm_pair[i].meas_altitudes[2][1]

        # R2 += cm_pair[i].R2 * cm_pair[i].N
        # RMSD += cm_pair[i].RMSD * cm_pair[i].N
        # o3_vmr_mean_absolute_diff += cm_pair[i].mean_absolute_diff * cm_pair[i].N
        # o3_vmr_mean_absolute_diff_err += cm_pair[i].mean_absolute_diff_err * cm_pair[i].N
        # o3_vmr_mean_relative_diff += cm_pair[i].mean_relative_diff * cm_pair[i].N
        # o3_vmr_mean_relative_diff_err += cm_pair[i].mean_relative_diff_err  * cm_pair[i].N
        # ols_params[0] += cm_pair[i].ols[0] * cm_pair[i].N  # Slope m, y-intercept b OLS
        # rma_params[0] += cm_pair[i].rma[0] * cm_pair[i].N  # Slope m, y-intercept b OLS
        # ols_params[1] += cm_pair[i].ols[1] * cm_pair[i].N  # Slope m, y-intercept b OLS
        # rma_params[1] += cm_pair[i].rma[1] * cm_pair[i].N  # Slope m, y-intercept b OLS
        
        # o3_vmr_N += [cm_pair[i].N] 

    R2 = R2 / sum(o3_vmr_N)
    RMSD = RMSD / sum(o3_vmr_N)
    o3_vmr_mean_absolute_diff = o3_vmr_mean_absolute_diff / sum(o3_vmr_N)
    o3_vmr_mean_absolute_diff_err = o3_vmr_mean_absolute_diff_err / sum(o3_vmr_N)
    o3_vmr_mean_relative_diff = o3_vmr_mean_relative_diff / sum(o3_vmr_N)
    o3_vmr_mean_relative_diff_err = o3_vmr_mean_relative_diff_err / sum(o3_vmr_N)
    ols_params[0] = ols_params[0] / sum(o3_vmr_N)  # Slope m, y-intercept b OLS
    rma_params[0] = rma_params[0] / sum(o3_vmr_N)  # Slope m, y-intercept b OLS
    ols_params[1] = ols_params[1] / sum(o3_vmr_N)  # Slope m, y-intercept b OLS
    rma_params[1] = rma_params[1] / sum(o3_vmr_N)  # Slope m, y-intercept b OLS
    
    # Create a scatter plot (linear regression), no colorbar.
    fig, axs = plt.subplots(1, 3,figsize=[14, 4],dpi=100) # Non-colorbar regression plot
    fig1, axs1 = plt.subplots(1, 3,figsize=[14, 4],dpi=100) # Colorbar plot
    
    i=0
    axs[i].scatter(x=a0_1,y=a1_1,marker='o',c='green',s=0.5)
    axs[i].plot(x_ideal,y_ideal,'k',lw=4)
    # axs[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    # axs[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    axs[i].set_title('Altitudes 0-20 km', y=1.05)
    if type(regression_labels[0])==str:
        axs[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:
        axs[i].set_ylabel(regression_labels[1])      
    # ols = 'y = '+str( "%.3f" % ols_params[i][0] )+'x + '+str( "{:.3e}".format(ols_params[i][1])) # Write OLS linear fit in y = mx + b form.
    # rma= 'y = '+str( "%.3f" % rma_params[i][0] )+'x + '+str( "{:.3e}".format(rma_params[i][1]) ) # Write RMA linear fit in y = mx + b form.
    # Rp = 'R.^2 = ' + str( "%.4f" % R2[i] ) # Pearson coefficient.      
    # axs[i].text(0.1e-5,3.1e-5,ols,color='red') # Add text labels for regression.
    # axs[i].text(0.1e-5,2.8e-5,rma,color='blue')
    # axs[i].text(0.1e-5,2.5e-5,Rp,color='black')
    axs[i].set_xlim([0,3.5e-5])
    axs[i].set_ylim([0,3.5e-5])
    
    
    df=pd.DataFrame(data={'A':a0_1,'B':a1_1,'C':a0_alt_1})
    points = axs1[i].scatter(df.A, df.B, c=df.C,cmap="jet", vmin=0, vmax=100, lw=0, s=1)
    axs1[i].ticklabel_format(axis='both',style='sci')
    # Plot ideal 1:1 fit. 
    axs1[i].plot(x_ideal,y_ideal,'k',lw=4)
    axs1[i].set_title('Altitudes 0-20 km', y=1.05)
    # Plot ordinary least squares fit.
    # axs1[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    # # Plot standard major axis fit. 
    # axs1[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    # axs1[i].text(0.1e-5,3.1e-5,ols,color='red') # Add text labels for regression.
    # axs1[i].text(0.1e-5,2.8e-5,rma,color='blue')
    # axs1[i].text(0.1e-5,2.5e-5,Rp,color='black')
    # axs1[i].set_title('Altitudes 0-20 km', y=1.05)
    if type(regression_labels[0])==str: # X label is in 0 index.
        axs1[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:# Y label is in 1 index.
        axs1[i].set_ylabel(regression_labels[1])
    axs1[i].set_ylim([0,3.5e-5]) # Set x and y axis limits.
    axs1[i].set_xlim([0,3.5e-5])

    
    i=1
    axs[i].scatter(x=a0_2,y=a1_2,marker='o',c='green',s=0.5)
    axs[i].plot(x_ideal,y_ideal,'k',lw=4)
    # axs[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    # axs[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    axs[i].set_title('Altitudes 20-60 km', y=1.05)
    if type(regression_labels[0])==str:
        axs[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:
        axs[i].set_ylabel(regression_labels[1])      
    # ols = 'y = '+str( "%.3f" % ols_params[i][0] )+'x + '+str( "{:.3e}".format(ols_params[i][1])) # Write OLS linear fit in y = mx + b form.
    # rma= 'y = '+str( "%.3f" % rma_params[i][0] )+'x + '+str( "{:.3e}".format(rma_params[i][1]) ) # Write RMA linear fit in y = mx + b form.
    # Rp = 'R.^2 = ' + str( "%.4f" % R2[i] ) # Pearson coefficient.      
    # axs[i].text(0.1e-5,3.1e-5,ols,color='red') # Add text labels for regression.
    # axs[i].text(0.1e-5,2.8e-5,rma,color='blue')
    # axs[i].text(0.1e-5,2.5e-5,Rp,color='black')
    axs[i].set_xlim([0,3.5e-5])
    axs[i].set_ylim([0,3.5e-5])


    df=pd.DataFrame(data={'A':a0_2,'B':a1_2,'C':a0_alt_2})
    points = axs1[i].scatter(df.A, df.B, c=df.C,cmap="jet", vmin=0, vmax=100, lw=0, s=1)
    # Colorbar Legend
    axs1[i].set_ylim([0,2.5e-5]) # Set x and y axis limits.
    axs1[i].set_xlim([0,2.5e-5])
    axs1[i].ticklabel_format(axis='both',style='sci')
    # Plot ideal 1:1 fit. 
    axs1[i].plot(x_ideal,y_ideal,'k',lw=4)
    # Plot ordinary least squares fit.
    # axs1[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    # # Plot standard major axis fit. 
    # axs1[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    # # axs1[i].text(0.1e-5,3.1e-5,ols,color='red') # Add text labels for regression.
    # # axs1[i].text(0.1e-5,2.8e-5,rma,color='blue')
    # axs1[i].text(0.1e-5,1.25e-5,Rp,color='black')
    axs1[i].set_title('Altitudes 20-60 km', y=1.05)
    if type(regression_labels[0])==str: # X label is in 0 index.
        axs1[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:# Y label is in 1 index.
        axs1[i].set_ylabel(regression_labels[1])

    
    i=2
    axs[i].scatter(x=a0_3,y=a1_3,marker='o',c='green',s=0.5)
    axs[i].plot(x_ideal,y_ideal,'k',lw=4)
    # axs[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    # axs[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    axs[i].set_title('Altitudes 60-100 km', y=1.05)
    if type(regression_labels[0])==str:
        axs[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:
        axs[i].set_ylabel(regression_labels[1])      
    # ols = 'y = '+str( "%.3f" % ols_params[i][0] )+'x + '+str( "{:.3e}".format(ols_params[i][1])) # Write OLS linear fit in y = mx + b form.
    # rma= 'y = '+str( "%.3f" % rma_params[i][0] )+'x + '+str( "{:.3e}".format(rma_params[i][1]) ) # Write RMA linear fit in y = mx + b form.
    # Rp = 'R.^2 = ' + str( "%.6f" % R2[i] ) # Pearson coefficient.      
    # axs[i].text(0.5e-5,3.1e-5,ols,color='red',fontsize=8) # Add text labels for regression.
    # axs[i].text(0.5e-5,2.8e-5,rma,color='blue',fontsize=8)
    # axs[i].text(0.5e-5,2.5e-5,Rp,color='black',fontsize=8)
    axs[i].set_xlim([0,4.0e-5])
    axs[i].set_ylim([0,4.0e-5])


    df=pd.DataFrame(data={'A':a0_3,'B':a1_3,'C':a0_alt_3})
    points = axs1[i].scatter(df.A, df.B, c=df.C,cmap="jet", vmin=0, vmax=100, lw=0, s=1)
    # Colorbar Legend
    # cbar = fig1.colorbar(points).set_label('Altitude [km]', rotation=270,x=1.5,labelpad=13)
    # m = cm_mat.ScalarMappable(cmap=cm_mat.jet,)    
    cax = plt.axes([0.97, 0.2, 0.4, 0.025])
    sm = plt.cm.ScalarMappable(cmap='jet', norm=plt.Normalize(vmin=0, vmax=100))
    # cbar=plt.colorbar(sm,cax,orientation='vertical')
    # cbar.set_label('Altitude [km]',fontsize=20,labelpad=10)
    
    axs1[i].set_ylim([0,4e-5]) # Set x and y axis limits.
    axs1[i].set_xlim([0,4e-5])
    axs1[i].ticklabel_format(axis='both',style='sci')
    # Plot ideal 1:1 fit. 
    axs1[i].plot(x_ideal,y_ideal,'k',lw=4)
    # Plot ordinary least squares fit.
    # axs1[i].plot(xy_ols[i][0],xy_ols[i][1],'--r',lw=2)
    # # Plot standard major axis fit. 
    # axs1[i].plot(xy_rma[i][0],xy_rma[i][1],'--b',lw=2)
    # axs[i].text(0.5e-5,3.1e-5,ols,color='red',fontsize=5) # Add text labels for regression.
    # axs[i].text(0.5e-5,2.8e-5,rma,color='blue',fontsize=5)
    # axs[i].text(0.5e-5,2.5e-5,Rp,color='black',fontsize=5)
    axs1[i].set_title('Altitudes 60-100 km', y=1.05)
    if type(regression_labels[0])==str: # X label is in 0 index.
        axs1[i].set_xlabel(regression_labels[0])
    if type(regression_labels[1])==str:# Y label is in 1 index.
        axs1[i].set_ylabel(regression_labels[1])

    fig.tight_layout()
    filenamepng = regression_title + ' Regression (sections) .png' # Create name for png plot file.
    print('Saving relation plot of VMR pairs')
    fig.savefig(filenamepng) # Save figure.
    
    filenamepng = regression_title + ' Altitude Colorbar (sections) ALL.png' # Create name for png plot file
    fig1.savefig(filenamepng) # Save figure.
    return 
   