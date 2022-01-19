# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 22:30:24 2021

@author: Victoria R Spada
Last Edit: March 7 2021
"""
import scipy
import numpy as np
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg

def w_estimator(M,sigma2,phi,n_0): 
    # M: number of months in data set
    # sigma: standard deviation of noise in dataset
    # phi: noise in dataset
    # n_0 : number of years in data set.
    def B_uncertainty(M,phi):
        a = 1/(3*np.sqrt(M))
        b = np.sqrt((1+phi)/(1-phi))
        return a*b
    
    w = ( (3.3*np.sqrt(sigma2))*np.sqrt((1+phi)/(1-phi)) )*( n_0**(-2/3) )
    B = B_uncertainty(M,phi)
    start = w* (np.exp(-B) **(-2/3) )
    end = w* (np.exp(B) **(-2/3) )
    return [start/24, end/24]

def n_estimator(M,sigma2,phi,w_0):  
    def B_uncertainty(M,phi):
        a = 1/(3*np.sqrt(M))
        b = np.sqrt((1+phi)/(1-phi))
    return a*b
    n = ( (3.3*np.sqrt(sigma2)/w_0)*np.sqrt((1+phi)/(1-phi)) )**(2/3)
    B = B_uncertainty(M,phi)
    start = n*np.exp(-B)
    end = n*np.exp(B)
    return [start, end]

def extract_noise(an_array,an_array_err):
    # Given a time series of monthly average ozone amounts at several altitude
    # slices, give back the associated noise with each month at each slice.
    def round_down_odd(n):
        if n%2==0:
            return n-1
        else :
            return n
    Nt = np.zeros(np.shape(an_array))
    for i in range(0,np.shape(an_array)[0],1): # Cycle through each altitude slice (row)
        x = an_array[i,:] # Extract non-zero months to detect noise from.
        indx = np.where(np.logical_and(x!=0, np.isnan(x)==False) )[0]
        y = x[indx]
        if len(y)>0:
            #  print(y)
            try:
                smooth_array = scipy.signal.savgol_filter(x, window_length=round_down_odd(len(x)), polyorder=1)
            except:
                smooth_array = np.ones(len(x))*1e-9
            Nt[i,:] = x - smooth_array 
    return Nt

def estimate_phi(an_array):
    # Output the autocorrelation coefficient of an array of noise points
    def AR(train):
        order=1
        model = AutoReg(train, order)
        return model
    def acf(x):
        length = len(x)
        return np.array([1]+[np.corrcoef(x[:-i], x[i:])[0,1]   for i in range(1, length)])

    phi = np.zeros(np.shape(an_array)[0]) 
    # for i in range(0,np.shape(an_array)[0],1): # Cycle through each altitude slice
    #     model = AR(an_array[i,:])
    #     model_fit = model.fit()
    #     PHI = model.fit()
    # PHI = np.mean(phi)
    phi = acf(an_array)
    return np.mean(phi)

def estimate_sigmaN(an_array):    
    # Output the monthly variances of noise points
    sigmaN = np.zeros(np.shape(an_array)[0]) # Create array of variances for each altitude slice
    for i in range(0,np.shape(an_array)[0],1): # Cycle through each altitude slice
        variance = np.var(an_array[i,:])
        sigmaN[i] = variance 
    return sigmaN