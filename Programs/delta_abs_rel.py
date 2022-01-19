# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 10:18:40 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: July 29 2020.
"""
# delta_abs_rel
# INPUT:
# x, y: these are the two input variables, type float array, length n.
# xerr, yerr: these are the corresponding errors/uncertainties for the input variables, type float array, length n.

# OUTPUT:  The output is a list of significant values for the input pair. 
# [ [delta_abs, err_abs], [delta_rel, err_rel], differences, differences_err ]
# [ delta_abs, err_abs ]: This two-element list contains two floats: the first is the mean absolute difference
# of the input dataset (same units as input data) and it's associated uncertainty.
# [ delta_rel, err_rel ]: This two-element list contains two floats: the first is the mean relative difference
# of the input dataset (%) and it's associated uncertainty.
# differences, differences_err: These two outputs are float arrays. The first, 'differences' is a list of the n differences
# between x and y points (ie : [ x[0]-y[0], x[1]-y[2], ..., x[n-1]-y[n-1]]).
# 'differences_err' is the propagated error of each point in 'differences.

from numpy import * 
import numpy 

def delta_abs_rel(x,y,xerr,yerr):
   sum_diff=0
   sum_diff_diff=0
   differences = []
   differences_err=[]
   err_rel = 0
   err_abs = 0
   var = 0
   stddev = 0
   
   if (len(x)==len(y)) and (len(x)!=0) and (len(xerr)==len(yerr)) and (len(xerr)==len(x)):
       n=len(x)
       count=0 # Count number of valid indices.
       for i in range(0,n,1):
         if (numpy.isnan(x[i])==False) and (numpy.isnan(y[i])==False):
            sum_diff = sum_diff + (x[i]-y[i])
            sum_diff_diff = sum_diff_diff + ((x[i]-y[i])/ ((x[i]+y[i])/2) )*100
            count+=1
            differences = differences + [(x[i]-y[i])]
            differences_err = differences_err + [ sqrt( (xerr[i])**2 + (yerr[i])**2 ) ] # Error of current difference.
       delta_abs = ( (1/count)*sum_diff) 
       delta_rel = ( (1/count)*sum_diff_diff)
       # also report standard error of the differences
       for i in range (0,count,1):
           var = var + (1/count)*(differences[i] - delta_abs)**2 # Note that delta_abs is the mean difference
       stddev = sqrt(var)
       err_abs = stddev/sqrt(count)
       error_rel = (err_abs*delta_rel)/delta_abs
       
   return  [ [delta_abs, err_abs], [delta_rel, (err_abs*delta_rel)/delta_abs], differences,differences_err]       
