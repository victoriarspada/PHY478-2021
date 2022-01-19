# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:55:41 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: Feb 18 2021
"""
# This class requires no inputs.
# This class represents a comparison between two instruments and carries the data/measurements necessary
# for instrument comparisons (atmospheric columns, number density, and volume mixing ratios). For each type of comparison, the compared data points are listed as arrays.
# Ordinary Least Squares and Reduced Major Axis linear regression fits are also included. 

import numpy 

class pair:
    # Measurement object with data as properties  
    def __init__(self):
        self.instrument_1 = [] #  Array of arrays [ [measurements from 2004], [measurements from 2005], ... ]
        self.instrument_2 = [] #  Array of arrays [ [measurements from 2004], [measurements from 2005], ... ]
                
        self.coincident_pairs = [] # Array of measurement pairs [ [a, b], [a, b], ...]
        self.coincident_pairs_by_year = []
        
        self.coin_sonde = numpy.NaN # The matches with a coincident sonde go here (as a pair object)
        self.closest_sonde = numpy.NaN # Measurements from the closest sonde fill the missing entries.
        self.a_priori = numpy.NaN # A priori measurements fill missing entries.
        
        self.N = numpy.NaN # Number of coincident pairs
        self.pc_range = '' # Range of partial columns we compare.
        self.years = '' # Range of years. 
        
        ###### Values corresponding to comparisons of O3 partial/total columns.
        self.columns_1 = numpy.NaN # To be a float array [DU]
        self.columns_2 = numpy.NaN # There arrays are arrays of partial or total columns used for comparison of the two instruments. Plot colums_1 and columns_2 against each other for a regression plot.
        self.columns_error_1 = numpy.NaN # To be a float arrat, [DU].
        self.columns_error_2 = numpy.NaN # These arrays are to be the propagated errors of the columns in columns_1 and columns_2.
        
        self.mean_absolute_diff  = numpy.NaN # Mean abs. diff. for all pairs [DU]
        self.mean_absolute_diff_arr = [] # Array of floats, [a, b, c...] mean absolute error for each year
        
        self.mean_relative_diff = numpy.NaN # Mean rel. diff. for all pairs, float [%]
        self.mean_relative_diff_arr = [] # Array of floats, [a, b, c...] mean rel. error for each year

        self.mean_absolute_diff_err  = numpy.NaN # Mean abs. diff. err. for all pairs
        self.mean_absolute_diff_err_arr = [] # Array of floats, [a, b, c...] mean absolute diff. error for each year
        
        self.mean_relative_diff_err = numpy.NaN # Mean rel. diff. err. for all pairs
        self.mean_relative_diff_err_arr = [] # Array of floats, [a, b, c...] mean rel. diff. error for each year

        self.R2 = numpy.NaN # Pearson coefficient for all coincident pairs
        self.R2_arr = [] # Array of floats, [a, b, c...] R.^2 for each year
        
        self.RMSD = numpy.NaN # RMSD for all pairs
        self.RMSD_arr = [] # Array of floats, [a, b, c...] RMSD for each year
        
        self.ols = [numpy.NaN, numpy.NaN] # Slope m, y-intercept b
        self.rma = [numpy.NaN, numpy.NaN]
        
        self.ols_arr = [] # [ [xarray], [yarray]]
        self.rma_arr = [] 
        #########
        
        ######### Values corresponding to comparisons of O3 Number Densities.
        self.o3_nd_N=numpy.NaN
        self.o3_nd_mean_absolute_diff  = numpy.NaN # Mean abs. err. for all pairs
        self.o3_nd_mean_absolute_diff_arr = [] # Array of floats, [a, b, c...] mean absolute error for each year
        
        self.o3_nd_mean_relative_diff = numpy.NaN # Mean rel. err. for all pairs
        self.o3_nd_mean_relative_diff_arr = [] # Array of floats, [a, b, c...] mean rel. error for each year

        self.o3_nd_mean_absolute_diff_err  = numpy.NaN # Mean abs. diff. err. for all pairs
        self.o3_nd_mean_absolute_diff_err_arr = [] # Array of floats, [a, b, c...] mean absolute diff. error for each year
        
        self.o3_nd_mean_relative_diff_err = numpy.NaN # Mean rel.diff. err. for all pairs
        self.o3_nd_mean_relative_diff_err_arr = [] # Array of floats, [a, b, c...] mean rel. diff. error for each year

        self.o3_nd_R2 = numpy.NaN # Pearson coefficient for all coincident pairs
        self.o3_nd_R2_arr = [] # Array of floats, [a, b, c...] R.^2 for each year
        
        self.o3_nd_RMSD = numpy.NaN # RMSD for all pairs
        self.o3_nd_RMSD_arr = [] # Array of floats, [a, b, c...] RMSD for each year
        
        self.o3_nd_ols = [numpy.NaN, numpy.NaN] # Slope m, y-intercept b for ordinary least squares and reduced major axis linear fits.
        self.o3_nd_rma = [numpy.NaN, numpy.NaN]
        
        self.o3_nd_ols_arr = [] # [ [xarray], [yarray] ]
        self.o3_nd_rma_arr = [] # nd_ols_arr and nd_rma_arr are the linear fits of the number densities between the two instruments, using ordianry least squares linear regression and reduced major axis regression respectively. 
        #########
        ######### Values corresponding to comparisons of O3 VMR.
        self.o3_vmr_N=numpy.NaN
        self.o3_vmr_mean_absolute_diff  = numpy.NaN # Mean abs. err. for all pairs
        self.o3_vmr_mean_absolute_diff_arr = [] # Array of floats, [a, b, c...] mean absolute error for each altitude
        
        self.o3_vmr_mean_relative_diff = numpy.NaN # Mean rel. err. for all pairs
        self.o3_vmr_mean_relative_diff_arr = [] # Array of floats, [a, b, c...] mean rel. error for each altitude

        self.o3_vmr_mean_absolute_diff_err  = numpy.NaN # Mean abs. diff. err. for all pairs
        self.o3_vmr_mean_absolute_diff_err_arr = [] # Array of floats, [a, b, c...] mean absolute diff. error for each altitude
        
        self.o3_vmr_mean_relative_diff_err = numpy.NaN # Mean rel.diff. err. for all pairs
        self.o3_vmr_mean_relative_diff_err_arr = [] # Array of floats, [a, b, c...] mean rel. diff. error for each altitude

        self.o3_vmr_R2 = numpy.NaN # Pearson coefficient for all coincident pairs
        self.o3_vmr_R2_arr = [] # Array of floats, [a, b, c...] R.^2 for each year
        
        self.o3_vmr_RMSD = numpy.NaN # RMSD for all pairs
        self.o3_vmr_RMSD_arr = [] # Array of floats, [a, b, c...] RMSD for each year
        
        self.o3_vmr_ols = [numpy.NaN, numpy.NaN] # Slope m, y-intercept b for ordinary least squares and reduced major axis linear fits.
        self.o3_vmr_rma = [numpy.NaN, numpy.NaN]
        
        self.o3_vmr_ols_arr = [] # [ [xarray], [yarray] ]
        self.o3_vmr_rma_arr = [] # nd_ols_arr and nd_rma_arr are the linear fits of the number densities between the two instruments, using ordianry least squares linear regression and reduced major axis regression respectively. 
        self.o3_vmr_meas_altitudes = []
        #########
        
        self.ideal_arr = [] # Ideal 1-1 relationship (ie, [ [0,1,2,3,4,5...], [0,1,2,3,4,5,...]])
        
        def plotter(self):
           plt.plot(self.ols_arr[0],self.ols_arr[1],'--r')
           plt.plot(self.rma_arr[0],self.rma_arr[1],'--b')
           plt.plot(self.ideal_arr[0],self.ideal_arr[1],'k')
           ols = 'y = '+str( "%.3f" % self.ols[0] )+'x + '+str( "%.3f" % self.ols[1]) 
           rma= 'y = '+str( "%.3f" % self.rma[0] )+'x + '+str( "%.3f" % self.rma[1])
           Rp = 'R.^2 = ' + str( "%.3f" % self.R2 )
           plt.text(225,485,ols,color='red')
           plt.text(225,475,rma,color='blue')
           plt.text(225,460,Rp,color='black')
           return 
      
        
    