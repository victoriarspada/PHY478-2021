# -*- coding: utf-8 -*-
"""
Created on Thurs Jul 16 10:19:00 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: February 19 2021.
"""
from OLS import *
from RMA import *
from delta_abs_rel import *
import numpy 
import matplotlib.pyplot as plt
import matplotlib.cm as cm_mat
import os
import scipy.stats
import datetime
import statsmodels.robust.robust_linear_model
import datetime 

# vmrAnalysis:
# INPUT:
# cm: Array of 2-length arrays. In each 2-length array is a measurement object for each of the two instruments being compared.
# regression_title: String. Title of the regression plot.
# abs_diff_title: String. Title of absolute difference scatter plot of .
# regression_labels: Array with two indices: [ xlabel, ylabel], where xlabel and ylabel are strings.
# folder: String; the name of the directory where we would like to save the figures. 
# OUTPUT: This function produces and saves figures of volume mixing ratio linear regression (shown as (a) a scatter plot, and (b) a histogram)
#  and absolute differences over time (scatter plot) over time. The three figures are saved into 'folder'.

def vmrAnalysis(cm_pair,cm):
   if type(cm)==list:
       # Read off instrument pair coincidences
       a0=[] # First pair; column array.
       a0e=[] # Error bar array.
       a0t=[] # Datetime date array.
       a0_alt = [] # altitude array
       
       a1=[] # Second pair; column array.
       a1e=[] # Error bar array.
       a1t=[] # Datetime date array.  
       a1_alt = [] # altitude array
       
       # Transform coincident pairs into a collection of VMRs.
       for i in range(0,len(cm),1):
          if (type((cm[i])[0].datetime)==datetime.datetime) and (type((cm[i])[1].datetime)==datetime.datetime) and type(((cm[i])[0]).common_altitude)==list and type(((cm[i])[1]).altitude)==list and type(((cm[i])[0]).common_o3_vmr)==list and type(((cm[i])[1]).o3_vmr)==list and (type((cm[i])[0].is_retrieved)==list) and (type((cm[i])[1].is_retrieved)==list) and (type((cm[i])[0].is_retrieved)==list) and (type((cm[i])[1].is_retrieved)==list) and len((((cm[i])[0]).common_altitude))==201 and len((((cm[i])[1]).altitude))==201 and len((((cm[i])[0]).common_o3_vmr))==201 and len((((cm[i])[1]).o3_vmr))==201 and len((((cm[i])[0]).is_retrieved))==201 and len((((cm[i])[1]).is_retrieved))==201 and len((((cm[i])[0]).common_o3_vmr_error))==201 and len((((cm[i])[1]).o3_vmr_error))==201 :
             # Find number densities with specified range for the pair.
             min_alt = 0 # Find the higher minimum altitudes between two measurements
             max_alt = 100  # Find the lower maximum altitudes between two measurements
             curr_altitude = min_alt # Set minimum altitude as current altitude.
             # Both objects have instruments between [min_alt, max_alt]
             # Scan through both objects.
             while curr_altitude<=max_alt:
                 idx0 = ((cm[i])[0].common_altitude).index( curr_altitude ) # Find the index of the current altitude for the first instrument.
                 idx1 = ((cm[i])[1].altitude).index( curr_altitude ) # Find the index of the current altitude for the first instrument.
                 if ((cm[i])[1].is_retrieved)[idx1]==1 : # Check that we have only valid numbers.
                    a0 = a0 + [((cm[i])[0].common_o3_vmr)[idx0]]
                    a0e = a0e + [((cm[i])[0].common_o3_vmr_error)[idx0]]
                    a0t = a0t + [(cm[i])[0].datetime]     
                    a0_alt = a0_alt + [(cm[i])[0].common_altitude[idx0]] # altitude array
                    
                    a1 = a1 + [((cm[i])[1].o3_vmr)[idx1]]
                    a1e = a1e + [((cm[i])[1].o3_vmr_error)[idx1]]
                    a1t = a1t + [(cm[i])[1].datetime]  
                    a1_alt = a1_alt + [(cm[i])[1].altitude[idx1]] # altitude array
                 curr_altitude+=1
             
       if len(a0)!=0 and len(a1)!=0: # Only create plot if there is a list of coincident measurements.
          [m0,b0,R,RMSD]=RMA(a0,a1) # Reduced Major Axis Regression.
          [m,b,R,RMSD]=OLS(a0,a1) # Ordinary Least Squares Regression.
          #m,b,R,p, std_err= scipy.stats.linregress(numpy.array(a0),numpy.array(a1)) # Ordinary Least Squares Regression.
          #RLM() # Robust linear method
          print('VMR RMSD',RMSD)
          print('VMR R',R,'R^2',R**2)

          [delta_abs_arr,delta_rel_arr,differences,differences_error] = delta_abs_rel(a0,a1,a0e,a1e)
          print('VMR Mean Relative Difference',delta_rel_arr[0],'+-',delta_rel_arr[1])
          print('VMR Mean Absolute Difference',delta_abs_arr[0],'+-',delta_abs_arr[1])    
          print('N VMR points',len(differences)) # The length of the list of absolute differences is the number of coincident measurements.
          print('OLS',m,b,'RMA',m0,b0) 
   
          x_ols = numpy.linspace(-0.5,0.5,10) # Plot ordinary least squares fit.
          y_ols = m*x_ols+b
          
          x_rma = numpy.linspace(-0.5,0.5,10) # Plot standard major axis fit. 
          y_rma = m0*x_rma+b0
   
          x_ideal = numpy.linspace(-0.5,0.5,10) # Plot ideal 1:1 fit. 
          y_ideal = x_ideal
     
          # Add this information to the pair object.
          cm_pair.o3_vmr_R2 = R**2
          cm_pair.o3_vmr_RMSD = RMSD
          cm_pair.o3_vmr_mean_absolute_diff = delta_abs_arr[0]
          cm_pair.o3_vmr_mean_absolute_diff_err = delta_abs_arr[1]
          cm_pair.o3_vmr_mean_relative_diff = delta_rel_arr[0]
          cm_pair.o3_vmr_mean_relative_diff_err = delta_rel_arr[1] 
          cm_pair.o3_vmr_ols = [m , b] # Slope m, y-intercept b
          cm_pair.o3_vmr_rma = [m0,b0]  
          cm_pair.o3_vmr_ols_arr = [x_ols, y_ols] # [ [xarray], [yarray]]
          cm_pair.o3_vmr_rma_arr = [x_rma, y_rma]   
          cm_pair.ideal_arr = [x_ideal, y_ideal] # Ideal 1-1 relationship 
          cm_pair.o3_vmr_N = len(differences)
          cm_pair.o3_vmr_meas = [a0,a1]
          cm_pair.o3_vmr_meas_errors = [a0e,a1e]
          cm_pair.o3_vmr_meas_datetime = [a0t, a1t]
          cm_pair.o3_vmr_meas_altitudes = [a0_alt, a1_alt]
   return cm_pair # Return updates comparison pair. 
