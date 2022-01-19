# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 23:51:21 2021

@author: Victoria R Spada
Last Edit: March 23 2021.
"""
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
from detecting_trends import *

def linear_trend(x,y_err,y):
    # Input column vectors for x and y, and the column vector that is the associated error with x.
    # x: datenum (month number)
    # y: monthly averaged ozone quantity
    # y_err: associated error for y
    
    # y = a + bx; output a and b
    # Extract non-zero months and make a diagonal matrix of ONLY THOSE MONTHS
    indx = np.where( np.logical_and( abs(y)>0, abs(y_err)>=0) )[0]
    # print('INDX ',indx, 'dates',x)
    x_reduced = np.zeros(len(indx))
    if len(x_reduced)==0:
        print(y_err,y)
        print('no x values')
        return np.nan, np.nan, np.nan, np.nan
    for i in range(0,len(indx),1):
        x_reduced[i] = indx[i]+1
    y_err_reduced = y_err[indx]
    for i in range(0,len(y_err_reduced),1):
        if y_err_reduced[i]==0:
            y_err_reduced[i] = 1e-5
    y_reduced = y[indx]
    
    # print('Include months',x_reduced)
    # print('Ozone values ',y_reduced)
    # print('Ozone Errors ',y_err_reduced)
    
    # Create square covariance matrix (only non-zero on diagonals)
    S = np.diag(y_err_reduced)
    Si = np.linalg.inv(S)
    e = np.ones(np.size(x_reduced))
    
    xT_Si = np.matmul(x_reduced.T, Si)
    y_eT = np.matmul(y_reduced,e.T)
    Si_e = np.matmul(Si, e)
    A = y_eT*np.matmul( xT_Si, Si_e )
    # A = np.matmul( xT_Si, np.matmul(y_eT, Si_e) )
    
    e_eT = np.matmul(e,e.T)
    Si_y = np.matmul(Si,y_reduced)
    B = np.matmul(xT_Si, e_eT*Si_y )
    
    x_eT = np.matmul(x_reduced,e.T)
    Si_e = np.matmul(Si, e)
    C = np.matmul(xT_Si, x_eT*Si_e )
    
    Si_x = np.matmul(Si, x_reduced)
    D = np.matmul(xT_Si, e_eT*Si_x )
    
    b = ( A-B )/( C-D )
    
    eT_Si = np.matmul(e.T, Si)
    E = np.matmul( eT_Si, y_reduced)
    F = b*np.matmul( eT_Si, x_reduced)
    G = np.matmul( eT_Si, e)
    
    a = ( E-F )/G
    
    #### Now find errors of these parameters 
    x_eT_si = np.matmul(x_reduced, eT_Si)
    xT_Si_x_eT_Si = xT_Si * x_eT_si # np.matmul( xT_Si, x_eT_si)
    
    x_xT_Si = np.matmul(x_reduced, xT_Si)
    eT_Si_x_xT_Si = eT_Si * x_xT_Si # np.matmul(eT_Si, x_xT_Si)
    
    xT_Si_x = np.matmul(x_reduced.T, Si_x)
    eT_Si_e = np.matmul(e.T, Si_e)
    eT_Si_e_xT_Si_x = eT_Si_e*xT_Si_x # np.matmul(eT_Si_e, xT_Si_x)
    
    xT_Si_e = np.matmul(x_reduced.T, Si_e)
    eT_Si_x = np.matmul(e.T, Si_x)
    eT_Si_x_xT_Si_e = eT_Si_x *xT_Si_e # np.matmul(eT_Si_x, xT_Si_e)
    a_stddev = (xT_Si_x_eT_Si - eT_Si_x_xT_Si) / (eT_Si_e_xT_Si_x - eT_Si_x_xT_Si_e)
    
    e_xT_Si = np.matmul(e, xT_Si)
    eT_Si_e_xT_Si = eT_Si*e_xT_Si # np.matmul(eT_Si, e_xT_Si)
    
    e_eT_Si = np.matmul(e, eT_Si)
    xT_Si_e_eT_Si = xT_Si * e_eT_Si # np.matmul(xT_Si, e_eT_Si)
    
    eT_Si_e = np.matmul(eT_Si, e)
    xT_Si_x = np.matmul(x_reduced.T, Si_x)
    xT_Si_x_eT_Si_e = xT_Si_x * eT_Si_e # np.matmul(xT_Si_x, eT_Si_e)
    
    xT_Si_e = np.matmul(x_reduced.T, Si_e)
    eT_Si_x = np.matmul(e.T, Si_x)
    xT_Si_e_eT_Si_x = xT_Si_e * eT_Si_x # np.matmul(xT_Si_e, eT_Si_x)
    
    b_stddev = (eT_Si_e_xT_Si[0] - xT_Si_e_eT_Si[0]) / (xT_Si_x_eT_Si_e - xT_Si_e_eT_Si_x)
    # print(eT_Si_e_xT_Si, xT_Si_e_eT_Si)#, xT_Si_x_eT_Si_e, xT_Si_e_eT_Si_x)
    # print(eT_Si_e_xT_Si[0], xT_Si_e_eT_Si[0])
    return a, b, a_stddev, b_stddev

def osc_linear_trend(x,y_err,y,l):
    # Input column vectors for x and y, and the column vector that is the associated error with x.
    # x: datenum (month number)
    # y: monthly averaged ozone quantity
    # y_err: associated error for y

    # y = a + bx; output a and b
    # Extract non-zero months and make a diagonal matrix of ONLY THOSE MONTHS
    indx = np.where( np.logical_and( abs(y)>0, abs(y_err)>0) )[0]
    # print('INDX ',indx, 'dates',x)
    x_reduced = np.zeros(len(indx))
    for i in range(0,len(indx),1):
        x_reduced[i] = indx[i]+1
    y_err_reduced = y_err[indx]
    y_reduced = y[indx]

    # # y = a + bx; output a and b
    # # Extract non-zero months and make a diagonal matrix of ONLY THOSE MONTHS
    # indx = np.where( y>0 )[0]
    # x_reduced = np.array(x)
    # y_err_reduced = y_err[indx]
    # y_reduced = y[indx]
    
    # Create square covariance matrix (only non-zero on diagonals)
    S = np.diag(y_err_reduced)
    try:
        Si = np.linalg.inv(S)
    except:
        out = np.zeros(2 + 2*len(l))
        out[:] = np.nan
        return out
    e = np.ones(np.size(x_reduced))
    
    # Create cosine and sine vectors for the given period lengths
    sin_vectors, cos_vectors = [], []
    for i in range(0,len(l),1):
        frequency = 2*np.pi/l[i]
        sin_vectors = sin_vectors + [np.sin(frequency*x_reduced)]
        cos_vectors = cos_vectors + [np.cos(frequency*x_reduced)]
        
    # Now ready to start constructing T matrix
    nvars = 2 + 2*len(l) # 2 linear terms + a cosine and sine term for each frequency
    T = np.zeros( (nvars, nvars) )
    # Do first row: corresponds to 'a', the constant term
    T[0,0] = 2*np.matmul( e.T, np.matmul(Si, e) )
    T[0,1] = 2*np.matmul( e.T, np.matmul(Si, x_reduced) )
    for i in range(0,len(l),1):
        T[0,2+2*i] = 2*np.matmul( e, np.matmul(Si, sin_vectors[i]) )
        T[0,2+(2*i)+1] = 2*np.matmul( e.T, np.matmul(Si, cos_vectors[i].T) )
    # Do second row: corresponds to 'b', the linear term
    T[1,0] = 2*np.matmul( x_reduced.T, np.matmul(Si, e) )
    T[1,1] = 2*np.matmul( x_reduced.T, np.matmul(Si, x_reduced) )
    for i in range(0,len(l),1):
        T[1,2+2*i] = 2*np.matmul( x_reduced.T, np.matmul(Si, sin_vectors[i]) )
        T[1,2+(2*i)+1] = 2*np.matmul( x_reduced.T, np.matmul(Si, cos_vectors[i]) )
        
    # Cycle through the rest of the parameters, given in l
    for i in range(0,len(l),1):
        # Do the sine term for the current frequency
        T[2+(2*i),0] =  2*np.matmul( sin_vectors[i].T, np.matmul(Si, e) )
        T[2+(2*i),1] =   2*np.matmul( sin_vectors[i].T, np.matmul(Si, e) )
        # Cosine term
        T[2+(2*i)+1,0] =  2*np.matmul( cos_vectors[i].T, np.matmul(Si, e) )
        T[2+(2*i)+1,1] =   2*np.matmul( cos_vectors[i].T, np.matmul(Si, e) )        
        for j in range(0,len(l),1):
            T[2+(2*i), 2+(2*j)] = 2*np.matmul( sin_vectors[i].T, np.matmul(Si, sin_vectors[j]) )
            T[2+(2*i), 2+(2*j)+1] = 2*np.matmul( sin_vectors[i].T, np.matmul(Si, cos_vectors[j]) )
            T[2+(2*i+1), 2+(2*j)] = 2*np.matmul( cos_vectors[i].T, np.matmul(Si, sin_vectors[j]) )
            T[2+(2*i+1), 2+(2*j)+1] = 2*np.matmul( cos_vectors[i].T, np.matmul(Si, cos_vectors[j]) )
    # Create q vector     
    q = np.zeros(nvars)    
    q[0] = 2*np.matmul( e.T, np.matmul( Si, y_reduced) )
    q[1] = 2*np.matmul( x_reduced.T, np.matmul( Si, y_reduced) )
    for i in range(0,len(l),1):
        q[2+i] = 2*np.matmul( sin_vectors[i].T, np.matmul( Si, y_reduced) )
        q[2+i+1] = 2*np.matmul( cos_vectors[i].T, np.matmul( Si, y_reduced) )        

    # Now solve for parameters: T*Params = q
    # print('\n',T,'\n')
    try:
        params = np.linalg.solve(T, q)
        return params
    except:
        out = np.zeros(nvars)
        out[:] = np.nan
        return out
    
