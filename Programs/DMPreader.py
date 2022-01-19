# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:49:42 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: August 14 2020.
"""
# This file contains a function that is used in any function that reads off measurements for instruments that 
# have DMPs in the ACE/OSIRIS Campaign Data Archive. The function is given a measurement object, which describes
# one measurement made by a trace-gas measuring instrument during the ACE/OSIRIS Campaign, as well as the filename 
# of the DMP to be read. Important values such as:
# longitude/latitude,
# sPV profile
# are recorded and stored to the measurement object. The modified measurement object is then returned as the output.

# INPUT:
# measurement: 'measurement' class object containing information regarding a particular measurement from an instrument
# during the ACE/OSIRIS Campaign. This input can have no information in it as long as it is a 'measurement' class object.
# filename: String object. The name of the  DMP file to be read.

# OUTPUT:
# measurement: An updated 'measurement' class object is returned. It contains new information regrading latitude, longitude,
# and sPV once the DMP file has been read.

import os
import numpy 

def DMPreader(filename,measurement):
   check_path = os.getcwd() 
   check_path = check_path + '\\' + filename # First check that the file exists. 
   if ((os.path.exists(check_path))==True):
      f=open(filename) # Open and read the data file.
      columns=[]
      _lines = f.readlines()
      for line in _lines: 
         columns = columns + [line.split()] # Read file to 'columns'

      altitude=[]
      spv=[]
      # Now find header line end.
      if (columns!=[]):
         for start in range(0,len(columns),1): # Scan for a valid header line.
            if columns[start]==['z', 'ACE-T', 'ACE-p', 'ACE-lon', 'ACE-lat', 'GEOS5-theta', 'GEOS5-T', 'delh-T', 'GPH', 'Zon-Wind', 'Mer-Wind', 'PV', 'sPV', 'EqL', 'delh-PV', 'EqL-edge', 'EqL-inner', 'EqL-outer']:
               break
            if columns[start]==['z', 'ACE-T', 'ACE-p', 'ACE-lon', 'ACE-lat', 'GEOS4-theta', 'GEOS4-T', 'delh-T', 'GPH', 'Zon-Wind', 'Mer-Wind', 'PV', 'sPV', 'EqL', 'delh-PV', 'EqL-edge', 'EqL-inner', 'EqL-outer']:
               break
            if columns[start]==['year', 'mon', 'day', 'time', 'lat', 'lon', 'alt', 'press', 'GEOS5-theta', 'GEOS5-T', 'delh-T', 'Zon-Wind', 'Mer-Wind', 'PV', 'sPV', 'EqL', 'delh-PV', 'EqL-edge', 'EqL-inner', 'EqL-outer']:
               break
            if columns[start]==['year', 'mon', 'day', 'time', 'lat', 'lon', 'alt', 'press', 'GEOS4-theta', 'GEOS4-T', 'delh-T', 'Zon-Wind', 'Mer-Wind', 'PV', 'sPV', 'EqL', 'delh-PV', 'EqL-edge', 'EqL-inner', 'EqL-outer']:
               break
      # Search for sPV, so we can extract latitude, longitude, beta angle, date, time
         for i in range(start+1,len(columns),1):
            if (measurement.occultation_ID!=''): # If this is an ACE satellite measurement
               if float((columns[i])[12])!=-999:
                  spv = spv + [ float((columns[i])[12]) ] # sPV
               else:
                  spv = spv + [numpy.NaN]
               if float((columns[i])[0])!=-999:
                  altitude = altitude + [ float((columns[i])[0]) ] # Altitude [km]
               else:
                   altitude = altitude + [numpy.NaN] # If an error, default to numpy.NaN
            else: # If this is not an ACE-satellite measurement.
               if float((columns[i])[14])!=-999:
                  spv = spv + [ float((columns[i])[14]) ] # sPV [10.^4 S.^-1]
               else:
                   spv = spv + [numpy.NaN] # If there was an error.
               if float((columns[i])[6])!=-999:
                  altitude = altitude + [ float((columns[i])[6]) ] # altitude 
               else:
                   altitude = altitude + [numpy.NaN]
            
         # Check for measurements closest to 14, 18, 20, & 22 km, for later choosing coincident measurements.
         _layers = [] # Empty array for sPV at desired layers.
         a=[] # Empty altitude array/
         dl=[] # Array for filling in 1 (inside polar vortex),0 (outside), or -999 (in between) for each layer
         s=[]    
         layers=[14,18,20,22]
         for l in layers:
            difference = 999
            index=0
            for i in range(0,len(altitude),1):
               check= abs(altitude[i]-l) # Difference in desired layer (ie, 14) and current element in altitude
               if (check < difference) and (spv[i]!=-999): # If this is the closest (spatially) measurement we have seen so far.
                  index = i
                  difference = check                               
            a=a+[float(altitude[index])]
            s=s+[float(spv[index])]         
            if spv[index]<=1.2:
               dl=dl+[0] # 0 signifies outside of the polar vortex
            elif spv[index]>=1.6:
               dl=dl+[1] # 1 signifies both inside the polar vortex.
            else: # Grey area.
               dl=dl+[-999]
         _layers = _layers + [s,dl,a]
         measurement.sPV_layers = _layers # sPV at desired altitudes [14, 18, 20, 22 km]
         measurement.sPV = [spv, altitude] # Attach data to the measurement object.
   return measurement
         
