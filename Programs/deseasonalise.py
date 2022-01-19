# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 20:07:20 2021

@author: victo
"""
import numpy as np
import scipy
import matplotlib.pyplot as plt

def deseasonalise(ozone):
    # Dates and ozone are vector arrays 
    # where dates[i] \elem [1,12]
    # and ozone[i] > 0
    averages = np.zeros(12)
    for i in range(1,13,1): # Cycle through each month
        N = 0
        for j in range(0,len(ozone),1):
            if (j+1)%i==0:
                averages[i-1]+=ozone[j]
                N+=1
        if N>0:
            averages[i-1] = averages[i-1]/N
    return averages 