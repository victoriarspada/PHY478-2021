# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:41:45 2021

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last Edit: February 28 2021
"""
import numpy as np
import matplotlib.pyplot as plt
import pickle
import datetime 

# This program is used to fit an RLM straight line through the data over the years 
# at each altitude slice.

def AltitudeModeller(all_measurements,year,uvvis):
    # INPUT: A list of lists. Each list contains the measurements for a given year.
    n=311
    retrievals = np.zeros((n,len(all_measurements)))
    o3_vmr = np.zeros((n,len(all_measurements)))
    o3_vmr_error = np.zeros((n,len(all_measurements)))
    dates = []
    longitude = []
    latitude = []
    for i in range(0,len(all_measurements),1): 
        dates += [0]
        longitude += [0]
        latitude += [0]

    for i in range(0,len(all_measurements),1):
        print('scanning measurements for ',year)
        measurement = all_measurements[i]
        if type(measurement.datetime)==datetime.datetime and len(measurement.o3_vmr)==n and len(measurement.o3_vmr_error)==n and len(measurement.is_retrieved)==n:
            print('adding meas to infoarray')
            o3_vmr[:,i] = np.array(measurement.o3_vmr)
            o3_vmr_error[:,i] = np.array(measurement.o3_vmr_error)
            retrievals[:,i] = np.array(measurement.is_retrieved)
            dates[i] = measurement.datetime
            longitude[i] = measurement.longitude
            latitude[i] = measurement.latitude
        else: 
            print('BAD')
            o3_vmr = o3_vmr[:,:-1]
            o3_vmr_error = o3_vmr_error[:-1]
            retrievals = retrievals[:-1]
            dates = dates[0:len(dates)-1]   
            latitude = latitude[0:len(latitude)-1]
            longitude = longitude[0:len(longitude)-1]
                            
    name = 'C:\\Users\\victo\\Downloads\\Engsci Year 3 Sem 2\\PHY478 RESEARCH PROJECT\\Code\\acemaestro_uvvis_'+str(year)+'_'+str(uvvis)+'_info_arrays.pickle'
    a = {'o3_vmr' : o3_vmr,
         'o3_vmr_error' : o3_vmr_error,
         'retrievals' : retrievals,
         'longitudes' : longitude,
         'latitudes' : latitude,
         'dates' : dates }
    pickle_out = open(name,"wb")
    pickle.dump(a, pickle_out)
    pickle_out.close()
    
    return
