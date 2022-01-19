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

def analyze_divisions(cm_pair,cm):
   if type(cm)==list:
       # Read off instrument pair coincidences
       a0_1=[] # First pair; column array.
       a0e_1=[] # Error bar array.
       a0t_1=[] # Datetime date array.
       a0_alt_1 = [] # altitude array
       
       a1_1=[] # Second pair; column array.
       a1e_1=[] # Error bar array.
       a1t_1=[] # Datetime date array.  
       a1_alt_1 = [] # altitude array

       a0_2=[] # First pair; column array.
       a0e_2=[] # Error bar array.
       a0t_2=[] # Datetime date array.
       a0_alt_2 = [] # altitude array
       
       a1_2=[] # Second pair; column array.
       a1e_2=[] # Error bar array.
       a1t_2=[] # Datetime date array.  
       a1_alt_2 = [] # altitude array

       a0_3=[] # First pair; column array.
       a0e_3=[] # Error bar array.
       a0t_3=[] # Datetime date array.
       a0_alt_3 = [] # altitude array
       
       a1_3=[] # Second pair; column array.
       a1e_3=[] # Error bar array.
       a1t_3=[] # Datetime date array.  
       a1_alt_3 = [] # altitude array       
       # Transform coincident pairs into a collection of VMRs.
       for i in range(0,len(cm),1):
          print('pair ',i)
          if (type((cm[i])[0].datetime)==datetime.datetime) and (type((cm[i])[1].datetime)==datetime.datetime) and type(((cm[i])[0]).altitude)==list and type(((cm[i])[1]).altitude)==list and type(((cm[i])[0]).o3_vmr)==list and type(((cm[i])[1]).o3_vmr)==list and (type((cm[i])[0].is_retrieved)==list) and (type((cm[i])[1].is_retrieved)==list) and (type((cm[i])[0].is_retrieved)==list) and (type((cm[i])[1].is_retrieved)==list) and len((((cm[i])[0]).altitude))==201 and len((((cm[i])[1]).altitude))==201 and len((((cm[i])[0]).o3_vmr))==201 and len((((cm[i])[1]).o3_vmr))==201 and len((((cm[i])[0]).is_retrieved))==201 and len((((cm[i])[1]).is_retrieved))==201 and len((((cm[i])[0]).o3_vmr_error))==201 and len((((cm[i])[1]).o3_vmr_error))==201 :
             # Find number densities with specified range for the pair.
             min_alt = 0 # Find the higher minimum altitudes between two measurements
             max_alt = 100  # Find the lower maximum altitudes between two measurements
             curr_altitude = min_alt # Set minimum altitude as current altitude.
             # Both objects have instruments between [min_alt, max_alt]
             # Scan through both objects.
             while curr_altitude<=max_alt:
                 idx0 = ((cm[i])[0].altitude).index( curr_altitude ) # Find the index of the current altitude for the first instrument.
                 idx1 = ((cm[i])[1].altitude).index( curr_altitude ) # Find the index of the current altitude for the first instrument.
                 if abs(((cm[i])[0].o3_vmr)[idx0])<1 and abs(((cm[i])[1].o3_vmr)[idx1])<1 and ((cm[i])[0].is_retrieved)[idx0]==1 and ((cm[i])[1].is_retrieved)[idx1]==1 : # Check that we have only valid numbers.
                    if curr_altitude<=20:
                        a0_1 = a0_1 + [((cm[i])[0].o3_vmr)[idx0]]
                        a0e_1 = a0e_1 + [((cm[i])[0].o3_vmr_error)[idx0]]
                        a0t_1 = a0t_1 + [(cm[i])[0].datetime]     
                        a0_alt_1 = a0_alt_1 + [(cm[i])[0].altitude[idx0]] # altitude array
                        
                        a1_1 = a1_1 + [((cm[i])[1].o3_vmr)[idx1]]
                        a1e_1 = a1e_1 + [((cm[i])[1].o3_vmr_error)[idx1]]
                        a1t_1 = a1t_1 + [(cm[i])[1].datetime]  
                        a1_alt_1 = a1_alt_1 + [(cm[i])[1].altitude[idx1]] # altitude array

                    if curr_altitude>20 and curr_altitude<60:
                        a0_2 = a0_2 + [((cm[i])[0].o3_vmr)[idx0]]
                        a0e_2 = a0e_2 + [((cm[i])[0].o3_vmr_error)[idx0]]
                        a0t_2 = a0t_2 + [(cm[i])[0].datetime]     
                        a0_alt_2 = a0_alt_2 + [(cm[i])[0].altitude[idx0]] # altitude array
                        
                        a1_2 = a1_2 + [((cm[i])[1].o3_vmr)[idx1]]
                        a1e_2 = a1e_2 + [((cm[i])[1].o3_vmr_error)[idx1]]
                        a1t_2 = a1t_2 + [(cm[i])[1].datetime]  
                        a1_alt_2 = a1_alt_2 + [(cm[i])[1].altitude[idx1]] # altitude array
                        
                    if curr_altitude>=60:
                        a0_3 = a0_3 + [((cm[i])[0].o3_vmr)[idx0]]
                        a0e_3 = a0e_3 + [((cm[i])[0].o3_vmr_error)[idx0]]
                        a0t_3 = a0t_3 + [(cm[i])[0].datetime]     
                        a0_alt_3 = a0_alt_3 + [(cm[i])[0].altitude[idx0]] # altitude array
                        
                        a1_3 = a1_3 + [((cm[i])[1].o3_vmr)[idx1]]
                        a1e_3 = a1e_3 + [((cm[i])[1].o3_vmr_error)[idx1]]
                        a1t_3 = a1t_3 + [(cm[i])[1].datetime]  
                        a1_alt_3 = a1_alt_3 + [(cm[i])[1].altitude[idx1]] # altitude array
                 curr_altitude+=1
             
       if len(a0_1)!=0 and len(a1_1)!=0: # Only create plot if there is a list of coincident measurements.
          [m0,b0,R,RMSD]=RMA(a0_1,a1_1) # Reduced Major Axis Regression.
          [m,b,R,RMSD]=OLS(a0_1,a1_1) # Ordinary Least Squares Regression.
          print('0-20km')
          print('VMR RMSD',RMSD)
          print('VMR R',R,'R^2',R**2)
          [delta_abs_arr,delta_rel_arr,differences,differences_error] = delta_abs_rel(a0_1,a1_1,a0e_1,a1e_1)
          print('VMR Mean Relative Difference',delta_rel_arr[0],'+-',delta_rel_arr[1])
          print('VMR Mean Absolute Difference',delta_abs_arr[0],'+-',delta_abs_arr[1])    
          print('N VMR points',len(differences)) # The length of the list of absolute differences is the number of coincident measurements.
          print('OLS',m,b,'RMA',m0,b0) 
   
          x_ols = numpy.linspace(-0.5,0.5,10) # Plot ordinary least squares fit.
          y_ols = m*x_ols+b          
          x_rma = numpy.linspace(-0.5,0.5,10) # Plot standard major axis fit. 
          y_rma = m0*x_rma+b0
     
          # Add this information to the pair object.
          cm_pair.R2 = [R**2]
          cm_pair.RMSD = [RMSD]
          cm_pair.mean_absolute_diff = [delta_abs_arr[0]]
          cm_pair.mean_absolute_diff_err = [delta_abs_arr[1]]
          cm_pair.mean_relative_diff = [delta_rel_arr[0]]
          cm_pair.mean_relative_diff_err = [delta_rel_arr[1]] 
          cm_pair.ols = [[m , b]] # Slope m, y-intercept b
          cm_pair.rma = [[m0,b0]]  
          cm_pair.ols_arr = [ [x_ols, y_ols] ]# [ [xarray], [yarray]]
          cm_pair.rma_arr = [ [x_rma, y_rma]  ] 
          cm_pair.N = [len(differences)]
          cm_pair.meas = [[a0_1,a1_1]]
          cm_pair.meas_errors = [[a0e_1,a1e_1]]
          cm_pair.meas_datetime = [[a0t_1, a1t_1]]
          cm_pair.meas_altitudes = [[a0_alt_1, a1_alt_1]]
          
       if len(a0_2)!=0 and len(a1_2)!=0: # Only create plot if there is a list of coincident measurements.
          [m0,b0,R,RMSD]=RMA(a0_2,a1_2) # Reduced Major Axis Regression.
          [m,b,R,RMSD]=OLS(a0_2,a1_2) # Ordinary Least Squares Regression.
          print('20-60km')
          print('VMR RMSD',RMSD)
          print('VMR R',R,'R^2',R**2)
          [delta_abs_arr,delta_rel_arr,differences,differences_error] = delta_abs_rel(a0_2,a1_2,a0e_2,a1e_2)
          print('VMR Mean Relative Difference',delta_rel_arr[0],'+-',delta_rel_arr[1])
          print('VMR Mean Absolute Difference',delta_abs_arr[0],'+-',delta_abs_arr[1])    
          print('N VMR points',len(differences)) # The length of the list of absolute differences is the number of coincident measurements.
          print('OLS',m,b,'RMA',m0,b0) 
   
          x_ols = numpy.linspace(-0.5,0.5,10) # Plot ordinary least squares fit.
          y_ols = m*x_ols+b          
          x_rma = numpy.linspace(-0.5,0.5,10) # Plot standard major axis fit. 
          y_rma = m0*x_rma+b0
     
          # Add this information to the pair object.
          cm_pair.R2 = cm_pair.R2 + [R**2]
          cm_pair.RMSD = cm_pair.RMSD + [RMSD]
          cm_pair.mean_absolute_diff = cm_pair.mean_absolute_diff + [delta_abs_arr[0]]
          cm_pair.mean_absolute_diff_err = cm_pair.mean_absolute_diff_err + [delta_abs_arr[1]]
          cm_pair.mean_relative_diff = cm_pair.mean_relative_diff + [delta_rel_arr[0]]
          cm_pair.mean_relative_diff_err = cm_pair.mean_relative_diff_err + [delta_rel_arr[1]] 
          cm_pair.ols = cm_pair.ols + [[m , b]] # Slope m, y-intercept b
          cm_pair.rma = cm_pair.rma + [[m0,b0]]  
          cm_pair.ols_arr = cm_pair.ols_arr + [ [x_ols, y_ols] ]# [ [xarray], [yarray]]
          cm_pair.rma_arr = cm_pair.rma_arr + [ [x_rma, y_rma]  ] 
          cm_pair.N =  cm_pair.N + [len(differences)]
          cm_pair.meas = cm_pair.meas + [[a0_2,a1_2]]
          cm_pair.meas_errors = cm_pair.meas_errors + [[a0e_2,a1e_2]]
          cm_pair.meas_datetime = cm_pair.meas_datetime + [[a0t_2, a1t_2]]
          cm_pair.meas_altitudes = cm_pair.meas_altitudes + [[a0_alt_2, a1_alt_2]]
    
       if len(a0_3)!=0 and len(a1_3)!=0: # Only create plot if there is a list of coincident measurements.
          [m0,b0,R,RMSD]=RMA(a0_3,a1_3) # Reduced Major Axis Regression.
          [m,b,R,RMSD]=OLS(a0_3,a1_3) # Ordinary Least Squares Regression.
          print('20-60km')
          print('VMR RMSD',RMSD)
          print('VMR R',R,'R^2',R**2)
          [delta_abs_arr,delta_rel_arr,differences,differences_error] = delta_abs_rel(a0_3,a1_3,a0e_3,a1e_3)
          print('VMR Mean Relative Difference',delta_rel_arr[0],'+-',delta_rel_arr[1])
          print('VMR Mean Absolute Difference',delta_abs_arr[0],'+-',delta_abs_arr[1])    
          print('N VMR points',len(differences)) # The length of the list of absolute differences is the number of coincident measurements.
          print('OLS',m,b,'RMA',m0,b0) 
   
          x_ols = numpy.linspace(-0.5,0.5,10) # Plot ordinary least squares fit.
          y_ols = m*x_ols+b          
          x_rma = numpy.linspace(-0.5,0.5,10) # Plot standard major axis fit. 
          y_rma = m0*x_rma+b0
     
          # Add this information to the pair object.
          cm_pair.R2 = cm_pair.R2 + [R**2]
          cm_pair.RMSD = cm_pair.RMSD + [RMSD]
          cm_pair.mean_absolute_diff = cm_pair.mean_absolute_diff + [delta_abs_arr[0]]
          cm_pair.mean_absolute_diff_err = cm_pair.mean_absolute_diff_err + [delta_abs_arr[1]]
          cm_pair.mean_relative_diff = cm_pair.mean_relative_diff + [delta_rel_arr[0]]
          cm_pair.mean_relative_diff_err = cm_pair.mean_relative_diff_err + [delta_rel_arr[1]] 
          cm_pair.ols = cm_pair.ols + [[m , b]] # Slope m, y-intercept b
          cm_pair.rma = cm_pair.rma + [[m0,b0]]  
          cm_pair.ols_arr = cm_pair.ols_arr + [ [x_ols, y_ols] ]# [ [xarray], [yarray]]
          cm_pair.rma_arr = cm_pair.rma_arr + [ [x_rma, y_rma]  ] 
          cm_pair.N =  cm_pair.N + [len(differences)]
          cm_pair.meas = cm_pair.meas + [[a0_3,a1_3]]
          cm_pair.meas_errors = cm_pair.meas_errors + [[a0e_3,a1e_3]]
          cm_pair.meas_datetime = cm_pair.meas_datetime + [[a0t_3, a1t_3]]
          cm_pair.meas_altitudes = cm_pair.meas_altitudes + [[a0_alt_3, a1_alt_3]]
   return cm_pair # Return updates comparison pair. 

def analyze_divisions_v313(cm_pair,cm):
   if type(cm)==list:
       # Read off instrument pair coincidences
       a0_1=[] # First pair; column array.
       a0e_1=[] # Error bar array.
       a0t_1=[] # Datetime date array.
       a0_alt_1 = [] # altitude array
       
       a1_1=[] # Second pair; column array.
       a1e_1=[] # Error bar array.
       a1t_1=[] # Datetime date array.  
       a1_alt_1 = [] # altitude array

       a0_2=[] # First pair; column array.
       a0e_2=[] # Error bar array.
       a0t_2=[] # Datetime date array.
       a0_alt_2 = [] # altitude array
       
       a1_2=[] # Second pair; column array.
       a1e_2=[] # Error bar array.
       a1t_2=[] # Datetime date array.  
       a1_alt_2 = [] # altitude array

       a0_3=[] # First pair; column array.
       a0e_3=[] # Error bar array.
       a0t_3=[] # Datetime date array.
       a0_alt_3 = [] # altitude array
       
       a1_3=[] # Second pair; column array.
       a1e_3=[] # Error bar array.
       a1t_3=[] # Datetime date array.  
       a1_alt_3 = [] # altitude array       
       # Transform coincident pairs into a collection of VMRs.
       for i in range(0,len(cm),1):
          print('pair ',i)
          # if (type((cm[i])[0].datetime)==datetime.datetime) and (type((cm[i])[1].datetime)==datetime.datetime) and type(((cm[i])[1]).altitude)==list and type(((cm[i])[0]).o3_vmr)==list and type(((cm[i])[1]).o3_vmr)==list and (type((cm[i])[0].is_retrieved)==list) and (type((cm[i])[1].is_retrieved)==list) and (type((cm[i])[0].is_retrieved)==list) and (type((cm[i])[1].is_retrieved)==list) and len((((cm[i])[0]).common_altitude))==201 and len((((cm[i])[1]).altitude))==201 and len((((cm[i])[0]).common_o3_vmr))==201 and len((((cm[i])[1]).o3_vmr))==201 and len((((cm[i])[1]).is_retrieved))==201 and len((((cm[i])[0]).common_o3_vmr_error))==201 and len((((cm[i])[1]).o3_vmr_error))==201 :
          if (type((cm[i])[0].datetime)==datetime.datetime) and (type((cm[i])[1].datetime)==datetime.datetime) and type(((cm[i])[0]).common_altitude)==list and type(((cm[i])[1]).altitude)==list and type(((cm[i])[0]).common_o3_vmr)==list and type(((cm[i])[1]).o3_vmr)==list and (type((cm[i])[0].is_retrieved)==list) and (type((cm[i])[1].is_retrieved)==list) and (type((cm[i])[0].is_retrieved)==list) and (type((cm[i])[1].is_retrieved)==list) and len((((cm[i])[0]).common_altitude))==201 and len((((cm[i])[1]).altitude))==201 and len((((cm[i])[0]).common_o3_vmr))==201 and len((((cm[i])[1]).o3_vmr))==201 and  len((((cm[i])[1]).is_retrieved))==201 and len((((cm[i])[0]).common_o3_vmr_error))==201 and len((((cm[i])[1]).o3_vmr_error))==201 :
       
             # Find number densities with specified range for the pair.
             min_alt = 0 # Find the higher minimum altitudes between two measurements
             max_alt = 100  # Find the lower maximum altitudes between two measurements
             curr_altitude = min_alt # Set minimum altitude as current altitude.
             # Both objects have instruments between [min_alt, max_alt]
             # Scan through both objects.
             while curr_altitude<=max_alt:
                 idx0 = ((cm[i])[0].common_altitude).index( curr_altitude ) # Find the index of the current altitude for the first instrument.
                 idx1 = ((cm[i])[1].altitude).index( curr_altitude ) # Find the index of the current altitude for the first instrument.
                 if abs(((cm[i])[0].common_o3_vmr)[idx0])<1 and abs(((cm[i])[1].o3_vmr)[idx1])<1 and ((cm[i])[1].is_retrieved)[idx1]==1 : # Check that we have only valid numbers.
                    if curr_altitude<=20:
                        a0_1 = a0_1 + [((cm[i])[0].common_o3_vmr)[idx0]]
                        a0e_1 = a0e_1 + [((cm[i])[0].common_o3_vmr_error)[idx0]]
                        a0t_1 = a0t_1 + [(cm[i])[0].datetime]     
                        a0_alt_1 = a0_alt_1 + [(cm[i])[0].common_altitude[idx0]] # altitude array
                        
                        a1_1 = a1_1 + [((cm[i])[1].o3_vmr)[idx1]]
                        a1e_1 = a1e_1 + [((cm[i])[1].o3_vmr_error)[idx1]]
                        a1t_1 = a1t_1 + [(cm[i])[1].datetime]  
                        a1_alt_1 = a1_alt_1 + [(cm[i])[1].altitude[idx1]] # altitude array

                    if curr_altitude>20 and curr_altitude<60:
                        a0_2 = a0_2 + [((cm[i])[0].common_o3_vmr)[idx0]]
                        a0e_2 = a0e_2 + [((cm[i])[0].common_o3_vmr_error)[idx0]]
                        a0t_2 = a0t_2 + [(cm[i])[0].datetime]     
                        a0_alt_2 = a0_alt_2 + [(cm[i])[0].common_altitude[idx0]] # altitude array
                        
                        a1_2 = a1_2 + [((cm[i])[1].o3_vmr)[idx1]]
                        a1e_2 = a1e_2 + [((cm[i])[1].o3_vmr_error)[idx1]]
                        a1t_2 = a1t_2 + [(cm[i])[1].datetime]  
                        a1_alt_2 = a1_alt_2 + [(cm[i])[1].altitude[idx1]] # altitude array
                        
                    if curr_altitude>=60:
                        a0_3 = a0_3 + [((cm[i])[0].common_o3_vmr)[idx0]]
                        a0e_3 = a0e_3 + [((cm[i])[0].common_o3_vmr_error)[idx0]]
                        a0t_3 = a0t_3 + [(cm[i])[0].datetime]     
                        a0_alt_3 = a0_alt_3 + [(cm[i])[0].common_altitude[idx0]] # altitude array
                        
                        a1_3 = a1_3 + [((cm[i])[1].o3_vmr)[idx1]]
                        a1e_3 = a1e_3 + [((cm[i])[1].o3_vmr_error)[idx1]]
                        a1t_3 = a1t_3 + [(cm[i])[1].datetime]  
                        a1_alt_3 = a1_alt_3 + [(cm[i])[1].altitude[idx1]] # altitude array
                 curr_altitude+=1
             
       if len(a0_1)!=0 and len(a1_1)!=0: # Only create plot if there is a list of coincident measurements.
          [m0,b0,R,RMSD]=RMA(a0_1,a1_1) # Reduced Major Axis Regression.
          [m,b,R,RMSD]=OLS(a0_1,a1_1) # Ordinary Least Squares Regression.
          print('0-20km')
          print('VMR RMSD',RMSD)
          print('VMR R',R,'R^2',R**2)
          [delta_abs_arr,delta_rel_arr,differences,differences_error] = delta_abs_rel(a0_1,a1_1,a0e_1,a1e_1)
          print('VMR Mean Relative Difference',delta_rel_arr[0],'+-',delta_rel_arr[1])
          print('VMR Mean Absolute Difference',delta_abs_arr[0],'+-',delta_abs_arr[1])    
          print('N VMR points',len(differences)) # The length of the list of absolute differences is the number of coincident measurements.
          print('OLS',m,b,'RMA',m0,b0) 
   
          x_ols = numpy.linspace(-0.5,0.5,10) # Plot ordinary least squares fit.
          y_ols = m*x_ols+b          
          x_rma = numpy.linspace(-0.5,0.5,10) # Plot standard major axis fit. 
          y_rma = m0*x_rma+b0
     
          # Add this information to the pair object.
          cm_pair.R2 = [R**2]
          cm_pair.RMSD = [RMSD]
          cm_pair.mean_absolute_diff = [delta_abs_arr[0]]
          cm_pair.mean_absolute_diff_err = [delta_abs_arr[1]]
          cm_pair.mean_relative_diff = [delta_rel_arr[0]]
          cm_pair.mean_relative_diff_err = [delta_rel_arr[1]] 
          cm_pair.ols = [[m , b]] # Slope m, y-intercept b
          cm_pair.rma = [[m0,b0]]  
          cm_pair.ols_arr = [ [x_ols, y_ols] ]# [ [xarray], [yarray]]
          cm_pair.rma_arr = [ [x_rma, y_rma]  ] 
          cm_pair.N = [len(differences)]
          cm_pair.meas = [[a0_1,a1_1]]
          cm_pair.meas_errors = [[a0e_1,a1e_1]]
          cm_pair.meas_datetime = [[a0t_1, a1t_1]]
          cm_pair.meas_altitudes = [[a0_alt_1, a1_alt_1]]
          
       if len(a0_2)!=0 and len(a1_2)!=0: # Only create plot if there is a list of coincident measurements.
          [m0,b0,R,RMSD]=RMA(a0_2,a1_2) # Reduced Major Axis Regression.
          [m,b,R,RMSD]=OLS(a0_2,a1_2) # Ordinary Least Squares Regression.
          print('20-60km')
          print('VMR RMSD',RMSD)
          print('VMR R',R,'R^2',R**2)
          [delta_abs_arr,delta_rel_arr,differences,differences_error] = delta_abs_rel(a0_2,a1_2,a0e_2,a1e_2)
          print('VMR Mean Relative Difference',delta_rel_arr[0],'+-',delta_rel_arr[1])
          print('VMR Mean Absolute Difference',delta_abs_arr[0],'+-',delta_abs_arr[1])    
          print('N VMR points',len(differences)) # The length of the list of absolute differences is the number of coincident measurements.
          print('OLS',m,b,'RMA',m0,b0) 
   
          x_ols = numpy.linspace(-0.5,0.5,10) # Plot ordinary least squares fit.
          y_ols = m*x_ols+b          
          x_rma = numpy.linspace(-0.5,0.5,10) # Plot standard major axis fit. 
          y_rma = m0*x_rma+b0
     
          # Add this information to the pair object.
          cm_pair.R2 = cm_pair.R2 + [R**2]
          cm_pair.RMSD = cm_pair.RMSD + [RMSD]
          cm_pair.mean_absolute_diff = cm_pair.mean_absolute_diff + [delta_abs_arr[0]]
          cm_pair.mean_absolute_diff_err = cm_pair.mean_absolute_diff_err + [delta_abs_arr[1]]
          cm_pair.mean_relative_diff = cm_pair.mean_relative_diff + [delta_rel_arr[0]]
          cm_pair.mean_relative_diff_err = cm_pair.mean_relative_diff_err + [delta_rel_arr[1]] 
          cm_pair.ols = cm_pair.ols + [[m , b]] # Slope m, y-intercept b
          cm_pair.rma = cm_pair.rma + [[m0,b0]]  
          cm_pair.ols_arr = cm_pair.ols_arr + [ [x_ols, y_ols] ]# [ [xarray], [yarray]]
          cm_pair.rma_arr = cm_pair.rma_arr + [ [x_rma, y_rma]  ] 
          cm_pair.N =  cm_pair.N + [len(differences)]
          cm_pair.meas = cm_pair.meas + [[a0_2,a1_2]]
          cm_pair.meas_errors = cm_pair.meas_errors + [[a0e_2,a1e_2]]
          cm_pair.meas_datetime = cm_pair.meas_datetime + [[a0t_2, a1t_2]]
          cm_pair.meas_altitudes = cm_pair.meas_altitudes + [[a0_alt_2, a1_alt_2]]
    
       if len(a0_3)!=0 and len(a1_3)!=0: # Only create plot if there is a list of coincident measurements.
          [m0,b0,R,RMSD]=RMA(a0_3,a1_3) # Reduced Major Axis Regression.
          [m,b,R,RMSD]=OLS(a0_3,a1_3) # Ordinary Least Squares Regression.
          print('20-60km')
          print('VMR RMSD',RMSD)
          print('VMR R',R,'R^2',R**2)
          [delta_abs_arr,delta_rel_arr,differences,differences_error] = delta_abs_rel(a0_3,a1_3,a0e_3,a1e_3)
          print('VMR Mean Relative Difference',delta_rel_arr[0],'+-',delta_rel_arr[1])
          print('VMR Mean Absolute Difference',delta_abs_arr[0],'+-',delta_abs_arr[1])    
          print('N VMR points',len(differences)) # The length of the list of absolute differences is the number of coincident measurements.
          print('OLS',m,b,'RMA',m0,b0) 
   
          x_ols = numpy.linspace(-0.5,0.5,10) # Plot ordinary least squares fit.
          y_ols = m*x_ols+b          
          x_rma = numpy.linspace(-0.5,0.5,10) # Plot standard major axis fit. 
          y_rma = m0*x_rma+b0
     
          # Add this information to the pair object.
          cm_pair.R2 = cm_pair.R2 + [R**2]
          cm_pair.RMSD = cm_pair.RMSD + [RMSD]
          cm_pair.mean_absolute_diff = cm_pair.mean_absolute_diff + [delta_abs_arr[0]]
          cm_pair.mean_absolute_diff_err = cm_pair.mean_absolute_diff_err + [delta_abs_arr[1]]
          cm_pair.mean_relative_diff = cm_pair.mean_relative_diff + [delta_rel_arr[0]]
          cm_pair.mean_relative_diff_err = cm_pair.mean_relative_diff_err + [delta_rel_arr[1]] 
          cm_pair.ols = cm_pair.ols + [[m , b]] # Slope m, y-intercept b
          cm_pair.rma = cm_pair.rma + [[m0,b0]]  
          cm_pair.ols_arr = cm_pair.ols_arr + [ [x_ols, y_ols] ]# [ [xarray], [yarray]]
          cm_pair.rma_arr = cm_pair.rma_arr + [ [x_rma, y_rma]  ] 
          cm_pair.N =  cm_pair.N + [len(differences)]
          cm_pair.meas = cm_pair.meas + [[a0_3,a1_3]]
          cm_pair.meas_errors = cm_pair.meas_errors + [[a0e_3,a1e_3]]
          cm_pair.meas_datetime = cm_pair.meas_datetime + [[a0t_3, a1t_3]]
          cm_pair.meas_altitudes = cm_pair.meas_altitudes + [[a0_alt_3, a1_alt_3]]
   return cm_pair # Return updates comparison pair. 
