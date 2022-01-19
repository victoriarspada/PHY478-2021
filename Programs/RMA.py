# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 09:55:18 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: July 29 2020.
"""
# Reduced Major Axis Method solver.
# Input: X and Y number arrays. 
# Output: slope m, y-intercept b, Pearson correlation coefficient R, Root mean square deviation RMSD for the
# input pair: X and Y.

from numpy import sqrt
import numpy

def RMA(x,y):

   xavg=numpy.NaN
   yavg=numpy.NaN
   xstddev=numpy.NaN
   ystddev=numpy.NaN
   R = numpy.NaN
   m = numpy.NaN
   b = numpy.NaN
   RMSD= numpy.NaN
   delta_abs=numpy.NaN
   delta_rel=numpy.NaN

   if (len(x)==len(y)): # Check that the datasets match.
    m=0
    R=0
    b=0
    RMSD=0 
    #Set m,R,b,RMSD.
    xstddev=0
    ystddev=0
    delta_abs=0
    delta_rel=0
    xavg=0
    yavg=0
    
    n=len(x)
    count=0 # Count the number of valid entries
    # X, Y average
    for i in range(0,n,1):
       #if (numpy.isnan(x[i])==False) and (numpy.isnan(y[i])==False):
       xavg = xavg + x[i]
       yavg = yavg + y[i]
       count+=1
    xavg = xavg/count
    yavg = yavg/count
    
    # X, Y sample standard deviations, correlation coefficient.
    for i in range(0,n,1):
       #if (numpy.isnan(x[i])==False) and (numpy.isnan(y[i])==False):
       xstddev = xstddev + ((x[i] - xavg)**2) #/(n)
       ystddev = ystddev + ((y[i] - yavg)**2) #/(n)
       RMSD = RMSD + (x[i]-y[i])**2

    xstddev = sqrt(xstddev/count)
    ystddev = sqrt(ystddev/count) # Square root to convert from variance to std. dev.
    for i in range(0,n,1):
       #if (numpy.isnan(x[i])==False) and (numpy.isnan(y[i])==False):
       R = R + (x[i]-xavg)*(y[i]-yavg)/(1*(xstddev*ystddev))
    R=R/count
    RMSD = sqrt( (RMSD/count) )
    
    m = ystddev/xstddev
    
    b = yavg - m*xavg

   return [m,b,R,RMSD] 


