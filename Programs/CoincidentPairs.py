# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 13:00:41 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: August 17 2020.
"""
# CoincidentPairs
# INPUT:
# Setting option for coincidence criteria: setting
#0 : within 12 hr and 500 km
#1 : within 12 hr, 500 km, same spv range ( <1.2 10^-4 s^01 or <1.6 10^-4 s^-1)
#2 : within 12 hr, 500 km, same spv range ( <1.2 10^-4 s^01 or <1.6 10^-4 s^-1), or somewhere in between
#3 : within 12 h4, 500 km, and within a margin (input) of sPV at selected layers.

#OUTPUT:
# The function outputs several lists of coincident measurements. 
# Lists of lists of coincident measurements for the following instruments are given:
# ACE-FTS & Ozonesondes/PEARL-GBS/UT-GBS/DIAL/FTIR
# ACE-MAESTRO-UV & & Ozonesondes/PEARL-GBS/UT-GBS/DIAL/FTIR
# ACEMAESTRO-VIS & & Ozonesondes/PEARL-GBS/UT-GBS/DIAL/FTIR

from OzonePlotter import *
from ACEFTSPlotter import *
from distance import *
import numpy
from datetime import *
from ACEMAESTROPlotter import *
from OLS import *
from RMA import *
from pairAnalyzer import *

def CoincidentPairs(dial,sondes,acefts,acemaestro,brewer,pearlgbs,utgbs,ftir,setting,margin):
# CoincidentPairs is a program to sort through input structures and sort them into coincident measurements.
# METRICS
# Temporal: For twilight measuring instruments (ACE FTS/MAESTRO, ZSL-DOAS), comparisons are restricted
# to the same twilight. Additionally, ACE FTS/MAESTRO comparisons are within the same occultation. For 
# all other instruments, pairs were found by pairing measurements from both datasets to the nearest
# measurement from the other dataset, within a 12 hour window.
# Spatial: Within 500 km of PEARL to reduce impact of spring/fall latitudinal NO2 gradient. 

# Input: sondes, acefts, and acemaestro are structs containing any number of measurement classes, where
# a measurement object corresponds to one occultation or ozonesonde launch. 
# Output: cm is a list of lists of each set of coincident measurements.

# Eureka is located on Ellesmere Island, Nunavut (80N, 86W).
   PEARLlat = 80
   PEARLlong = -86.4
   
   cm_acefts_utgbs=[]
   cm_acefts_pearlgbs=[]
   cm_acemaestro_utgbs=[]
   cm_acemaestro_pearlgbs=[]
   cm_acemaestro_uv_utgbs=[]
   cm_acemaestro_vis_utgbs=[]
   cm_acemaestro_uv_pearlgbs=[]
   cm_acemaestro_vis_pearlgbs=[]
   cm_acefts_acemaestro=[]
   cm_acefts_acemaestro_uv = []
   cm_acefts_acemaestro_vis = []   
   
   cm_acefts_brewer=[]
   cm_acemaestro_brewer=[]

   cm_acefts_sondes=[]   
   cm_acemaestro_sondes=[]
   cm_acemaestro_uv_sondes=[]
   cm_acemaestro_vis_sondes=[]
   
   cm_acefts_dial=[]
   cm_acemaestro_dial=[]
   cm_acemaestro_uv_dial=[]
   cm_acemaestro_vis_dial=[]
   
   cm_acefts_ftir=[]
   cm_acemaestro_ftir=[]
   cm_acemaestro_uv_ftir=[]
   cm_acemaestro_vis_ftir=[]

   # Extract number of measurements for the ozonesondes.
   number_of_sondes = len(sondes)
   # Extract number of measurements for the ACEFTS.
   number_of_acefts = len(acefts)
   # Extract number of measurements for the ACEMAESTRO.
   number_of_acemaestro = len(acemaestro)
   # Extract number of measurement for the Brewer.
   number_of_brewer = len(brewer)
   number_of_utgbs = len(utgbs)
   number_of_pearlgbs = len(pearlgbs)
   # Extract number of measurement for DIAL.
   number_of_dial = len(dial)
   # Extract number of measurement for FTIR.
   number_of_ftir = len(ftir)

   p_sonde = [] # This is an empty list that, for each instrument pair, will contain all possible coincident pairs.
   p_brewer = [] 
   p_utgbs = []
   p_pearlgbs = []
   p_dial = []
   p_ftir = []
   for i in range(0,len(sondes),1):
       p_sonde = p_sonde + [[]]
   for i in range(0,len(brewer),1):
       p_brewer = p_brewer + [[]]
   for i in range(0,len(utgbs),1):
       p_utgbs = p_utgbs + [[]]
   for i in range(0,len(pearlgbs),1):
       p_pearlgbs = p_pearlgbs + [[]]
   for i in range(0,len(dial),1):
       p_dial = p_dial + [[]]
   for i in range(0,len(ftir),1):
       p_ftir = p_ftir + [[]]

# Sort through all ACE-FTS/MAESTRO readings, pairing corresponding occultations (noting each version).
# Note that ACE-FTS and ACE-MAESTRO have coincident occultations, so if an instrument is coincident with
# ACE-FTS, it is also coincident with ACE-MAESTRO for that same occultation ID.
   # For each occultation there is 1 ACE-MAESTRO & one ACE-FTS measurement, so no need to check for 1-1 pairings.
   for i in range(0,number_of_acefts,1):
      curr_acefts = acefts[i] # measurement object
      if (numpy.isnan(curr_acefts.o3_partial_column)==False):
         upper_bound = min(curr_acefts.altitude) # Extract minimum of altitude
      
      times = [] # Create list of time differences between ACE-MAESTRO & O3sonde measurements to determine closest (temporally) pair.
      match = 0
      for j in range(0,number_of_acemaestro,1):
         curr_acemaestro = acemaestro[j] # measurement object 
         if (curr_acemaestro.occultation_ID == curr_acefts.occultation_ID):
            cm_acefts_acemaestro = cm_acefts_acemaestro + [[curr_acefts, curr_acemaestro]] # Add coincident occultations (same ID).
            if curr_acemaestro.uvvis==0: # UV MEASUREMENT
               cm_acefts_acemaestro_uv =  cm_acefts_acemaestro_uv + [[curr_acefts, curr_acemaestro]] # Add comparison for UV. Spectrum.
            if curr_acemaestro.uvvis==1: # VIS MEASUREMENT
               cm_acefts_acemaestro_vis =  cm_acefts_acemaestro_vis + [[curr_acefts, curr_acemaestro]] # Add comparison for UV. Spectrum.                            

      # Search for corresponding ozonesondes
      for j in range(0,number_of_sondes,1):
         curr_sonde = sondes[j]
         radius = distance([curr_acefts.latitude,curr_acefts.longitude],[curr_sonde.latitude,curr_sonde.longitude])
         # Check that the measurements are within a 500 km radius.
         if (radius <= 500):
            # Check for temporal coincidence.
            e = (curr_sonde.datetime - curr_acefts.datetime).total_seconds()
            times = times + [abs(e)]
            if (abs(e) < 86400): # If less than 12 hours have elapsed.
                altitude = []
                for m in range(0,len(curr_sonde.altitude),1):
                   altitude = altitude + [100*1000*curr_sonde.altitude[m]] # Convert to cm,
                # Now integrate sonde from 0 altitude to minimum ACE-FTS altitude. 
                # If the O3sonde does not cover this range we get an error.
                if (numpy.isnan(curr_acefts.o3_partial_column)==False): # Remembering to check that the ACE-FTS reading is not an error message.
                   [C, err] = rectrange(altitude, curr_sonde.o3_number_density,100, curr_sonde.o3_number_density_error,[0,upper_bound]) # [Molecules.cm^-2].
                   if (numpy.isnan(C)==False)  and (numpy.isnan(err)==False):
                      match = 1
                      curr_acefts.o3_column_plus_coin_sonde = C/(2.6867*10**16) + curr_acefts.o3_partial_column # Assign to measurement before storing coincident pair.
                      curr_acefts.o3_column_plus_coin_sonde_error =sqrt(  (err/(2.6867*10**16))**2 + (curr_acefts.o3_partial_column_error)**2 )                                      
                      
                      curr_acefts.o3_column_plus_sonde = C/(2.6867*10**16) + curr_acefts.o3_partial_column # Assign to measurement before storing coincident pair.
                      curr_acefts.o3_column_plus_sonde_error =sqrt(  (err/(2.6867*10**16))**2 + (curr_acefts.o3_partial_column_error)**2 )                
                if (setting==0): # No sPV criteria
                   p_sonde[j] = p_sonde[j] + [[curr_acefts, curr_sonde]] # Add to list of coincidences for this sonde.
    
                if (setting==1) and (type(curr_sonde.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( ( (curr_sonde.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 0 ) or ( (curr_sonde.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 2 ) ) and ( ( (curr_sonde.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 0 ) or ( (curr_sonde.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 2 ) ) and ( ( (curr_sonde.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 0 ) or ( (curr_sonde.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 2 ) ) and ( ( (curr_sonde.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 0 ) or ( (curr_sonde.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 2 ) ):
                   p_sonde[j] = p_sonde[j] + [[curr_acefts, curr_sonde]] # Add to list of coincidences for this sonde.
                if (setting==2) and (type(curr_sonde.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( ( (curr_sonde.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 0 ) or ( (curr_sonde.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 2 ) or ( (curr_sonde.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == -1998 ) ) and ( ( (curr_sonde.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 0 ) or ( (curr_sonde.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 2 ) or ( (curr_sonde.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == -1998 ) ) and ( ( (curr_sonde.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 0 ) or ( (curr_sonde.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 2 ) or ( (curr_sonde.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == -1998 ) ) and ( ( (curr_sonde.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 0 ) or ( (curr_sonde.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 2 ) or ( (curr_sonde.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == -1998 ) ):
                   p_sonde[j] = p_sonde[j] + [[curr_acefts, curr_sonde]] # Add to list of coincidences for this sonde.
                if (setting==3) and (type(curr_sonde.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( abs((curr_sonde.sPV_layers)[0][0] - (curr_acefts.sPV_layers)[0][0]) <= margin )  and ( abs((curr_sonde.sPV_layers)[0][1] - (curr_acefts.sPV_layers)[0][1]) <= margin ) and ( abs((curr_sonde.sPV_layers)[0][2] - (curr_acefts.sPV_layers)[0][2]) <= margin ) and ( abs((curr_sonde.sPV_layers)[0][3] - (curr_acefts.sPV_layers)[0][3]) <= margin ):
                   p_sonde[j] = p_sonde[j] + [[curr_acefts, curr_sonde]] # Add to list of coincidences for this sonde.
               
      if (match==0) and (numpy.isnan(curr_acefts.o3_partial_column)==False): # If we did not find  coincident sonde, find closest sonde for ACE-FTS + ozonesonde total column.
          while (match==0) and (times!=[]): # Keep checking for closest sonde as long as there is no match and there are sondes to choose from.
              sonde = min(times) # Extract minimum time difference in sonde list.
              for i in range(0,len(times),1):
                  if times[i]==sonde: # If we have located the index of the sonde with the lowest temporal separation from the ACE-FTS measurement.
                      break
              curr_sonde = sondes[i]
              altitude = []
              for m in range(0,len(curr_sonde.altitude),1):
                 altitude = altitude + [100*1000*curr_sonde.altitude[m]] # Convert to cm, for integration over number density.
                 # Now integrate sonde from 0 altitude to minimum ACE-FTS altitude. 
                 # If the O3sonde does not cover this range we get an error.
                 [C, err] = rectrange(altitude, curr_sonde.o3_number_density,100, curr_sonde.o3_number_density_error,[0,upper_bound]) # [Molecules.cm^-2].
              if (numpy.isnan(C)==False)  and (numpy.isnan(err)==False) and (numpy.isnan(curr_acefts.o3_partial_column)==False): # Remembering to check that the ACE-MAESTRO reading is not an error message.
                 match = 1
                 curr_acefts.o3_column_plus_sonde = C/(2.6867*10**16) + curr_acefts.o3_partial_column # Assign to measurement before storing coincident pair.
                 curr_acefts.o3_column_plus_sonde_error =sqrt(  (err/(2.6867*10**16))**2 + (curr_acefts.o3_partial_column_error)**2 )
              else:
                 if i==0:
                    times = times[1:len(times)]
                 elif i==len(times):
                    times = times[0:len(times)-1]
                 else:
                    times = times[0:i] + times[i+1:len(times)]
             
      # Search for corresponding PEARL-GBS
      for j in range(0,number_of_pearlgbs,1):
         curr_pearlgbs = pearlgbs[j]
         radius = distance([curr_acefts.latitude,curr_acefts.longitude],[curr_pearlgbs.latitude,curr_pearlgbs.longitude])
         # Check that the measurements are within a 500 km radius.
         if (radius <= 500):
            # Check for temporal coincidence.
            e = (curr_pearlgbs.datetime - curr_acefts.datetime).total_seconds()
            if (abs(e) < 86400): # If less than 12 hours have elapsed.
               if setting==0:
                  p_pearlgbs[j] = p_pearlgbs[j] +  [[curr_acefts, curr_pearlgbs]] 
               if (setting==1) and (type(curr_pearlgbs.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( ( (curr_pearlgbs.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 2 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 2 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 2 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 2 ) ):
                  p_pearlgbs[j] = p_pearlgbs[j] +  [[curr_acefts, curr_pearlgbs]] 
               if (setting==2) and (type(curr_pearlgbs.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( ( (curr_pearlgbs.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 2 ) or ( (curr_pearlgbs.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == -1998 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 2 ) or ( (curr_pearlgbs.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == -1998 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 2 ) or ( (curr_pearlgbs.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == -1998 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 2 ) or ( (curr_pearlgbs.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == -1998 ) ):
                  p_pearlgbs[j] = p_pearlgbs[j] +  [[curr_acefts, curr_pearlgbs]] 
               if (setting==3) and (type(curr_pearlgbs.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( abs((curr_pearlgbs.sPV_layers)[0][0] - (curr_acefts.sPV_layers)[0][0]) <= margin )  and ( abs((curr_pearlgbs.sPV_layers)[0][1] - (curr_acefts.sPV_layers)[0][1]) <= margin ) and ( abs((curr_pearlgbs.sPV_layers)[0][2] - (curr_acefts.sPV_layers)[0][2]) <= margin ) and ( abs((curr_pearlgbs.sPV_layers)[0][3] - (curr_acefts.sPV_layers)[0][3]) <= margin ):
                  p_pearlgbs[j] = p_pearlgbs[j] +  [[curr_acefts, curr_pearlgbs]] 
                  
      # Search for corresponding UT-GBS
      for j in range(0,number_of_utgbs,1):
         curr_utgbs = utgbs[j]
         radius = distance([curr_acefts.latitude,curr_acefts.longitude],[curr_utgbs.latitude,curr_utgbs.longitude])
         # Check that the measurements are within a 500 km radius.
         if (radius <= 500):
            # Check for temporal coincidence.
            e = (curr_utgbs.datetime - curr_acefts.datetime).total_seconds()
            if (abs(e) < 86400): # If less than 12 hours have elapsed.
               if setting==0:
                  p_utgbs[j] = p_utgbs[j] +  [[curr_acefts, curr_utgbs]] 
               if (setting==1) and (type(curr_utgbs.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( ( (curr_utgbs.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 0 ) or ( (curr_utgbs.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 2 ) ) and ( ( (curr_utgbs.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 0 ) or ( (curr_utgbs.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 2 ) ) and ( ( (curr_utgbs.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 0 ) or ( (curr_utgbs.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 2 ) ) and ( ( (curr_utgbs.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 0 ) or ( (curr_utgbs.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 2 ) ):
                  p_utgbs[j] = p_utgbs[j] +  [[curr_acefts, curr_utgbs]] 
               if (setting==2) and (type(curr_utgbs.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( ( (curr_utgbs.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 0 ) or ( (curr_utgbs.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 2 ) or ( (curr_utgbs.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == -1998 ) ) and ( ( (curr_utgbs.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 0 ) or ( (curr_utgbs.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 2 ) or ( (curr_utgbs.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == -1998 ) ) and ( ( (curr_utgbs.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 0 ) or ( (curr_utgbs.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 2 ) or ( (curr_utgbs.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == -1998 ) ) and ( ( (curr_utgbs.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 0 ) or ( (curr_utgbs.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 2 ) or ( (curr_utgbs.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == -1998 ) ):
                  p_utgbs[j] = p_utgbs[j] +  [[curr_acefts, curr_utgbs]] 
               if (setting==3) and (type(curr_utgbs.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( abs((curr_utgbs.sPV_layers)[0][0] - (curr_acefts.sPV_layers)[0][0]) <= margin )  and ( abs((curr_utgbs.sPV_layers)[0][1] - (curr_acefts.sPV_layers)[0][1]) <= margin ) and ( abs((curr_utgbs.sPV_layers)[0][2] - (curr_acefts.sPV_layers)[0][2]) <= margin ) and ( abs((curr_utgbs.sPV_layers)[0][3] - (curr_acefts.sPV_layers)[0][3]) <= margin ):
                  p_utgbs[j] = p_utgbs[j] +  [[curr_acefts, curr_utgbs]]              
            
      # Search for corresponding DIAL
      for j in range(0,number_of_dial,1):
         curr_dial = dial[j]
         radius = distance([curr_acefts.latitude,curr_acefts.longitude],[curr_dial.latitude,curr_dial.longitude])
         # Check that the measurements are within a 500 km radius.
         if (radius <= 500):
            # Check for temporal coincidence.
            e = (curr_dial.datetime - curr_acefts.datetime).total_seconds()
            if (abs(e) < 86400): # If less than 12 hours have elapsed.
               if setting==0:
                  p_dial[j] = p_dial[j] + [[curr_acefts, curr_dial]]
               if (setting==1) and (type(curr_dial.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( ( (curr_dial.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 0 ) or ( (curr_dial.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 2 ) ) and ( ( (curr_dial.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 0 ) or ( (curr_dial.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 2 ) ) and ( ( (curr_dial.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 0 ) or ( (curr_dial.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 2 ) ) and ( ( (curr_dial.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 0 ) or ( (curr_dial.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 2 ) ):
                  p_dial[j] = p_dial[j] + [[curr_acefts, curr_dial]]
               if (setting==2) and (type(curr_dial.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( ( (curr_dial.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 0 ) or ( (curr_dial.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 2 ) or ( (curr_dial.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == -1998 ) ) and ( ( (curr_dial.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 0 ) or ( (curr_dial.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 2 ) or ( (curr_dial.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == -1998 ) ) and ( ( (curr_dial.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 0 ) or ( (curr_dial.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 2 ) or ( (curr_dial.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == -1998 ) ) and ( ( (curr_dial.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 0 ) or ( (curr_dial.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 2 ) or ( (curr_dial.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == -1998 ) ):
                  p_dial[j] = p_dial[j] + [[curr_acefts, curr_dial]]
               if (setting==3) and (type(curr_dial.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( abs((curr_dial.sPV_layers)[0][0] - (curr_acefts.sPV_layers)[0][0]) <= margin )  and ( abs((curr_dial.sPV_layers)[0][1] - (curr_acefts.sPV_layers)[0][1]) <= margin ) and ( abs((curr_dial.sPV_layers)[0][2] - (curr_acefts.sPV_layers)[0][2]) <= margin ) and ( abs((curr_dial.sPV_layers)[0][3] - (curr_acefts.sPV_layers)[0][3]) <= margin ):
                  p_dial[j] = p_dial[j] + [[curr_acefts, curr_dial]]

      # Search for corresponding FTIR
      for j in range(0,number_of_ftir,1):
         curr_ftir = ftir[j]
         radius = distance([curr_acefts.latitude,curr_acefts.longitude],[curr_ftir.latitude,curr_ftir.longitude])
         # Check that the measurements are within a 500 km radius.
         if (radius <= 500):
            # Check for temporal coincidence.
            e = (curr_ftir.datetime - curr_acefts.datetime).total_seconds()
            if (abs(e) < 86400): # If less than 12 hours have elapsed.
               if setting==0:
                  p_ftir[j] = p_ftir[j] + [[curr_acefts, curr_ftir]]
               if (setting==1) and (type(curr_ftir.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( ( (curr_ftir.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 0 ) or ( (curr_ftir.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 2 ) ) and ( ( (curr_ftir.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 0 ) or ( (curr_ftir.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 2 ) ) and ( ( (curr_ftir.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 0 ) or ( (curr_ftir.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 2 ) ) and ( ( (curr_ftir.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 0 ) or ( (curr_ftir.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 2 ) ):
                  p_ftir[j] = p_ftir[j] + [[curr_acefts, curr_ftir]]
               if (setting==2) and (type(curr_ftir.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( ( (curr_ftir.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 0 ) or ( (curr_ftir.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == 2 ) or ( (curr_ftir.sPV_layers)[1][0] + (curr_acefts.sPV_layers)[1][0] == -1998 ) ) and ( ( (curr_ftir.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 0 ) or ( (curr_ftir.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == 2 ) or ( (curr_ftir.sPV_layers)[1][1] + (curr_acefts.sPV_layers)[1][1] == -1998 ) ) and ( ( (curr_ftir.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 0 ) or ( (curr_ftir.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == 2 ) or ( (curr_ftir.sPV_layers)[1][2] + (curr_acefts.sPV_layers)[1][2] == -1998 ) ) and ( ( (curr_ftir.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 0 ) or ( (curr_ftir.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == 2 ) or ( (curr_ftir.sPV_layers)[1][3] + (curr_acefts.sPV_layers)[1][3] == -1998 ) ):
                  p_ftir[j] = p_ftir[j] + [[curr_acefts, curr_ftir]]
               if (setting==3) and (type(curr_ftir.sPV_layers)==list) and (type(curr_acefts.sPV_layers)==list) and ( abs((curr_ftir.sPV_layers)[0][0] - (curr_acefts.sPV_layers)[0][0]) <= margin )  and ( abs((curr_ftir.sPV_layers)[0][1] - (curr_acefts.sPV_layers)[0][1]) <= margin ) and ( abs((curr_ftir.sPV_layers)[0][2] - (curr_acefts.sPV_layers)[0][2]) <= margin ) and ( abs((curr_ftir.sPV_layers)[0][3] - (curr_acefts.sPV_layers)[0][3]) <= margin ):
                  p_ftir[j] = p_ftir[j] + [[curr_acefts, curr_ftir]]

   # We are now done looking for comparisons between ACE-FTS and other instruments.
   # For each measurement, if we have more than one coincident pair, choose the 'best' coincident pair using pairAnalyzer.
   #print('ACE-FTS O3SONDE \n')
   for i in range(0,len(p_sonde),1): # For all sonde measurements.
      index = pairAnalyzer(p_sonde[i]) # Find the best coincident pair for this sonde measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_sonde[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acefts_sondes = pairAdder(cm_acefts_sondes,p_sonde[i][index][0],p_sonde[i][index][1])
          # Update comparison list.
   #print('ACE-FTS PEARL-GBS \n')
   for i in range(0,len(p_pearlgbs),1): # For all sonde measurements.
      index = pairAnalyzer(p_pearlgbs[i]) # Find the best coincident pair for this PGBS measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_pearlgbs[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list. 
          cm_acefts_pearlgbs = pairAdder(cm_acefts_pearlgbs,p_pearlgbs[i][index][0],p_pearlgbs[i][index][1])
          # Update comparison list.
   #print('ACE-FTS UT-GBS \n')
   for i in range(0,len(p_utgbs),1): # For all sonde measurements.
      index = pairAnalyzer(p_utgbs[i]) # Find the best coincident pair for this PGBS measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_utgbs[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acefts_utgbs = pairAdder(cm_acefts_utgbs,p_utgbs[i][index][0],p_utgbs[i][index][1])
          # Update comparison list.
   #print('ACE-FTS DIAL \n')
   for i in range(0,len(p_dial),1): # For all sonde measurements.
      index = pairAnalyzer(p_dial[i]) # Find the best coincident pair for this PGBS measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_dial[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acefts_dial = pairAdder(cm_acefts_dial,p_dial[i][index][0],p_dial[i][index][1])
          # Update comparison list.
   #print('ACE-FTS FTIR \n')
   for i in range(0,len(p_ftir),1): # For all sonde measurements.
      index = pairAnalyzer(p_ftir[i]) # Find the best coincident pair for this FTIR measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_ftir[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acefts_ftir = pairAdder(cm_acefts_ftir,p_ftir[i][index][0],p_ftir[i][index][1])
          # Update comparison list.

   # Reset coincident pair holders for ACE-MAESTRO comparisons.
   p_uv_sonde = [] # This is an empty list that, for each instrument pair, will contain all possible coincident pairs.
   p_vis_sonde=[] # Separate into UV & VIS because we are dealing with ACE-MAESTRO.
   p_brewer = [] 
   p_uv_pearlgbs = []
   p_vis_pearlgbs = []
   p_uv_utgbs = []
   p_vis_utgbs = []
   p_uv_dial = []
   p_vis_dial = []
   p_uv_ftir = []
   p_vis_ftir = []

   for i in range(0,len(sondes),1):
       p_uv_sonde = p_uv_sonde + [[]]
       p_vis_sonde = p_vis_sonde + [[]]
   for i in range(0,len(brewer),1):
       p_brewer = p_brewer + [[]]
   for i in range(0,len(utgbs),1):
       p_uv_utgbs = p_uv_utgbs + [[]]
       p_vis_utgbs = p_vis_utgbs + [[]]
   for i in range(0,len(pearlgbs),1):
       p_uv_pearlgbs = p_uv_pearlgbs + [[]]
       p_vis_pearlgbs = p_vis_pearlgbs + [[]]
   for i in range(0,len(dial),1):
       p_uv_dial = p_uv_dial + [[]]
       p_vis_dial = p_vis_dial + [[]]
   for i in range(0,len(ftir),1):
       p_uv_ftir = p_uv_ftir + [[]]
       p_vis_ftir = p_vis_ftir + [[]]
               
   # Now sift through all ACE-MAESTRO measurements/
   for i in range(0,number_of_acemaestro,1):
      curr_acemaestro=acemaestro[i]
      if (numpy.isnan(curr_acemaestro.o3_partial_column)==False):
         upper_bound = min(curr_acemaestro.altitude) # Extract minimum of altitude

      times = [] # Create list of time differences between ACE-MAESTRO & O3sonde measurements to determine closest (temporally) pair.
      match = 0
      for j in range(0,number_of_sondes,1): # Search for ACE-MAESTRO/Ozonesonde pairs
         curr_sonde = sondes[j]
         radius = distance([curr_acemaestro.latitude,curr_acemaestro.longitude],[curr_sonde.latitude,curr_sonde.longitude])
         # Check that the measurements are within a 500 km radius.
         if (radius <= 500):
            # Check for temporal coincidence.
            e = (curr_sonde.datetime - curr_acemaestro.datetime).total_seconds()
            times = times + [abs(e)]
            if (abs(e) < 86400): # If less than 12 hours have elapsed.
                altitude = []
                for m in range(0,len(curr_sonde.altitude),1): # Now check if we can use this o3sonde for the ACE-MAESTRO + ozonesonde total column. 
                   altitude = altitude + [100*1000*curr_sonde.altitude[m]] # Convert to cm, for integration over number density.
                # Now integrate sonde from 0 altitude to minimum ACE-MAESTRO altitude. 
                # If the O3sonde does not cover this range we get an error.
                if (numpy.isnan(curr_acemaestro.o3_partial_column)==False): # Remembering to check that the ACE-MAESTRO reading is not an error message.
                  [C, err] = rectrange(altitude, curr_sonde.o3_number_density,100, curr_sonde.o3_number_density_error,[0,upper_bound]) # [Molecules.cm^-2].
                  if (numpy.isnan(C)==False)  and (numpy.isnan(err)==False):
                      match = 1
                      curr_acemaestro.o3_column_plus_coin_sonde = C/(2.6867*10**16) + curr_acemaestro.o3_partial_column # Assign to measurement before storing coincident pair.
                      curr_acemaestro.o3_column_plus_coin_sonde_error =sqrt(  (err/(2.6867*10**16))**2 + (curr_acemaestro.o3_partial_column_error)**2 )                      
                      
                      curr_acemaestro.o3_column_plus_sonde = C/(2.6867*10**16) + curr_acemaestro.o3_partial_column # Assign to measurement before storing coincident pair.
                      curr_acemaestro.o3_column_plus_sonde_error =sqrt(  (err/(2.6867*10**16))**2 + (curr_acemaestro.o3_partial_column_error)**2 )
                if setting==0: # No sPV criteria
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_sonde[j] = p_uv_sonde[j] +  [[curr_acemaestro, curr_sonde]]     
                   elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_sonde[j] = p_vis_sonde[j] +  [[curr_acemaestro, curr_sonde]]     
                if (setting==1) and (type(curr_acemaestro.sPV_layers)==list) and (type(curr_sonde.sPV_layers)==list) and ( ( (curr_acemaestro.sPV_layers)[1][0] + (curr_sonde.sPV_layers)[1][0] == 0 ) or ( (curr_acemaestro.sPV_layers)[1][0] + (curr_sonde.sPV_layers)[1][0] == 2 ) ) and ( ( (curr_acemaestro.sPV_layers)[1][1] + (curr_sonde.sPV_layers)[1][1] == 0 ) or ( (curr_acemaestro.sPV_layers)[1][1] + (curr_sonde.sPV_layers)[1][1] == 2 ) ) and ( ( (curr_acemaestro.sPV_layers)[1][2] + (curr_sonde.sPV_layers)[1][2] == 0 ) or ( (curr_acemaestro.sPV_layers)[1][2] + (curr_sonde.sPV_layers)[1][2] == 2 ) ) and ( ( (curr_acemaestro.sPV_layers)[1][3] + (curr_sonde.sPV_layers)[1][3] == 0 ) or ( (curr_acemaestro.sPV_layers)[1][3] + (curr_sonde.sPV_layers)[1][3] == 2 ) ):
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_sonde[j] = p_uv_sonde[j] +  [[curr_acemaestro, curr_sonde]]     
                   elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_sonde[j] = p_vis_sonde[j] +  [[curr_acemaestro, curr_sonde]]  
                if (setting==2) and (type(curr_acemaestro.sPV_layers)==list) and (type(curr_sonde.sPV_layers)==list) and ( ( (curr_acemaestro.sPV_layers)[1][0] + (curr_sonde.sPV_layers)[1][0] == 0 ) or ( (curr_acemaestro.sPV_layers)[1][0] + (curr_sonde.sPV_layers)[1][0] == 2 ) or ( (curr_acemaestro.sPV_layers)[1][0] + (curr_sonde.sPV_layers)[1][0] == -1998 ) ) and ( ( (curr_acemaestro.sPV_layers)[1][1] + (curr_sonde.sPV_layers)[1][1] == 0 ) or ( (curr_acemaestro.sPV_layers)[1][1] + (curr_sonde.sPV_layers)[1][1] == 2 ) or ( (curr_acemaestro.sPV_layers)[1][1] + (curr_sonde.sPV_layers)[1][1] == -1998 ) ) and ( ( (curr_acemaestro.sPV_layers)[1][2] + (curr_sonde.sPV_layers)[1][2] == 0 ) or ( (curr_acemaestro.sPV_layers)[1][2] + (curr_sonde.sPV_layers)[1][2] == 2 ) or ( (curr_acemaestro.sPV_layers)[1][2] + (curr_sonde.sPV_layers)[1][2] == -1998 ) ) and ( ( (curr_acemaestro.sPV_layers)[1][3] + (curr_sonde.sPV_layers)[1][3] == 0 ) or ( (curr_acemaestro.sPV_layers)[1][3] + (curr_sonde.sPV_layers)[1][3] == 2 ) or ( (curr_acemaestro.sPV_layers)[1][3] + (curr_sonde.sPV_layers)[1][3] == -1998 ) ):
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_sonde[j] = p_uv_sonde[j] +  [[curr_acemaestro, curr_sonde]]     
                   elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_sonde[j] = p_vis_sonde[j] +  [[curr_acemaestro, curr_sonde]]  
                if (setting==3) and (type(curr_acemaestro.sPV_layers)==list) and (type(curr_sonde.sPV_layers)==list) and ( abs((curr_sonde.sPV_layers)[0][0] - (curr_acemaestro.sPV_layers)[0][0]) <= margin )  and ( abs((curr_sonde.sPV_layers)[0][1] - (curr_acemaestro.sPV_layers)[0][1]) <= margin ) and ( abs((curr_sonde.sPV_layers)[0][2] - (curr_acemaestro.sPV_layers)[0][2]) <= margin ) and ( abs((curr_sonde.sPV_layers)[0][3] - (curr_acemaestro.sPV_layers)[0][3]) <= margin ):
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_sonde[j] = p_uv_sonde[j] +  [[curr_acemaestro, curr_sonde]]     
                   elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_sonde[j] = p_vis_sonde[j] +  [[curr_acemaestro, curr_sonde]]  

      if (match==0) and (numpy.isnan(curr_acemaestro.o3_partial_column)==False):
          while (match==0) and (times!=[]):
              sonde = min(times) # Find the sonde with the minimal time separation from the ACE-MAESTRO measurement.
              for i in range(0,len(times),1):
                  if times[i]==sonde: # Find the index of the sonde.
                      break
              curr_sonde = sondes[i]
              altitude = []
              for m in range(0,len(curr_sonde.altitude),1):
                 altitude = altitude + [100*1000*curr_sonde.altitude[m]] # Convert to cm,
                 # Now integrate sonde from 0 altitude to minimum ACE-MAESTRO altitude. 
                 # If the O3sonde does not cover this range we get an error.
                 [C, err] = rectrange(altitude, curr_sonde.o3_number_density,100, curr_sonde.o3_number_density_error,[0,upper_bound]) # [Molecules.cm^-2].
              if (numpy.isnan(C)==False)  and (numpy.isnan(err)==False) and (numpy.isnan(curr_acemaestro.o3_partial_column)==False): # Remembering to check that the ACE-MAESTRO reading is not an error message.
                 match = 1
                 curr_acemaestro.o3_column_plus_sonde = C/(2.6867*10**16) + curr_acemaestro.o3_partial_column # Assign to measurement before storing coincident pair.
                 curr_acemaestro.o3_column_plus_sonde_error =sqrt(  (err/(2.6867*10**16))**2 + (curr_acemaestro.o3_partial_column_error)**2 )
              else:
                 if i==0:
                    times = times[1:len(times)]
                 elif i==len(times):
                    times = times[0:len(times)-1]
                 else:
                    times = times[0:i] + times[i+1:len(times)]

      # Search for corresponding PEARL-GBS
      for j in range(0,number_of_pearlgbs,1):
         curr_pearlgbs = pearlgbs[j]
         radius = distance([curr_acemaestro.latitude,curr_acemaestro.longitude],[curr_pearlgbs.latitude,curr_pearlgbs.longitude])
         # Check that the measurements are within a 500 km radius.
         if (radius <= 500):
            # Check for temporal coincidence.
            e = (curr_pearlgbs.datetime - curr_acemaestro.datetime).total_seconds()
            if (abs(e) < 86400): # If less than 12 hours have elapsed.
               if setting==0:
                  if curr_acemaestro.uvvis==0: # UV Spectrum:
                     p_uv_pearlgbs[j] = p_uv_pearlgbs[j] +  [[curr_acemaestro, curr_pearlgbs]]     
                  elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                     p_vis_pearlgbs[j] = p_vis_pearlgbs[j] +  [[curr_acemaestro, curr_pearlgbs]]
               if (setting==1) and (type(curr_pearlgbs.sPV_layers)==list) and (type(curr_acemaestro.sPV_layers)==list) and ( ( (curr_pearlgbs.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 2 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 2 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 2 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 2 ) ):
                  if curr_acemaestro.uvvis==0: # UV Spectrum:
                     p_uv_pearlgbs[j] = p_uv_pearlgbs[j] +  [[curr_acemaestro, curr_pearlgbs]]    
                  elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                     p_vis_pearlgbs[j] = p_vis_pearlgbs[j] +  [[curr_acemaestro, curr_pearlgbs]]
               if (setting==2) and (type(curr_pearlgbs.sPV_layers)==list) and (type(curr_acemaestro.sPV_layers)==list) and ( ( (curr_pearlgbs.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 2 ) or ( (curr_pearlgbs.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == -1998 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 2 ) or ( (curr_pearlgbs.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == -1998 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 2 ) or ( (curr_pearlgbs.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == -1998 ) ) and ( ( (curr_pearlgbs.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 0 ) or ( (curr_pearlgbs.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 2 ) or ( (curr_pearlgbs.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == -1998 ) ):
                  if curr_acemaestro.uvvis==0: # UV Spectrum:
                     p_uv_pearlgbs[j] = p_uv_pearlgbs[j] +  [[curr_acemaestro, curr_pearlgbs]]    
                  elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                     p_vis_pearlgbs[j] = p_vis_pearlgbs[j] +  [[curr_acemaestro, curr_pearlgbs]]
               if (setting==3) and (type(curr_pearlgbs.sPV_layers)==list) and (type(curr_acemaestro.sPV_layers)==list) and ( abs((curr_pearlgbs.sPV_layers)[0][0] - (curr_acemaestro.sPV_layers)[0][0]) <= margin )  and ( abs((curr_pearlgbs.sPV_layers)[0][1] - (curr_acemaestro.sPV_layers)[0][1]) <= margin ) and ( abs((curr_pearlgbs.sPV_layers)[0][2] - (curr_acemaestro.sPV_layers)[0][2]) <= margin ) and ( abs((curr_pearlgbs.sPV_layers)[0][3] - (curr_acemaestro.sPV_layers)[0][3]) <= margin ):
                  if curr_acemaestro.uvvis==0: # UV Spectrum:
                     p_uv_pearlgbs[j] = p_uv_pearlgbs[j] +  [[curr_acemaestro, curr_pearlgbs] ]    
                  elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                     p_vis_pearlgbs[j] = p_vis_pearlgbs[j] +  [[curr_acemaestro, curr_pearlgbs]]
                     
      # Search for corresponding UT-GBS measurements.
      for j in range(0,number_of_utgbs,1):
         curr_utgbs = utgbs[j]
         radius = distance([curr_acemaestro.latitude,curr_acemaestro.longitude],[curr_utgbs.latitude,curr_utgbs.longitude])
         # Check that the measurements are within a 500 km radius.
         if (radius <= 500):
            # Check for temporal coincidence.
            e = (curr_utgbs.datetime - curr_acemaestro.datetime).total_seconds()
            if (abs(e) < 86400): # If less than 12 hours have elapsed.
               if setting==0:
                  if curr_acemaestro.uvvis==0: # UV Spectrum:
                     p_uv_utgbs[j] = p_uv_utgbs[j] +  [[curr_acemaestro, curr_utgbs] ]    
                  elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                     p_vis_utgbs[j] = p_vis_utgbs[j] +  [[curr_acemaestro, curr_utgbs]] 
               if (setting==1) and (type(curr_utgbs.sPV_layers)==list) and (type(curr_acemaestro.sPV_layers)==list) and ( ( (curr_utgbs.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 0 ) or ( (curr_utgbs.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 2 ) ) and ( ( (curr_utgbs.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 0 ) or ( (curr_utgbs.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 2 ) ) and ( ( (curr_utgbs.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 0 ) or ( (curr_utgbs.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 2 ) ) and ( ( (curr_utgbs.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 0 ) or ( (curr_utgbs.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 2 ) ):
                  if curr_acemaestro.uvvis==0: # UV Spectrum:
                     p_uv_utgbs[j] = p_uv_utgbs[j] +  [[curr_acemaestro, curr_utgbs]  ]   
                  elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                     p_vis_utgbs[j] = p_vis_utgbs[j] +  [[curr_acemaestro, curr_utgbs]]
               if (setting==2) and (type(curr_utgbs.sPV_layers)==list) and (type(curr_acemaestro.sPV_layers)==list) and ( ( (curr_utgbs.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 0 ) or ( (curr_utgbs.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 2 ) or ( (curr_utgbs.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == -1998 ) ) and ( ( (curr_utgbs.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 0 ) or ( (curr_utgbs.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 2 ) or ( (curr_utgbs.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == -1998 ) ) and ( ( (curr_utgbs.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 0 ) or ( (curr_utgbs.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 2 ) or ( (curr_utgbs.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == -1998 ) ) and ( ( (curr_utgbs.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 0 ) or ( (curr_utgbs.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 2 ) or ( (curr_utgbs.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == -1998 ) ):
                  if curr_acemaestro.uvvis==0: # UV Spectrum:
                     p_uv_utgbs[j] = p_uv_utgbs[j] +  [[curr_acemaestro, curr_utgbs] ]    
                  elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                     p_vis_utgbs[j] = p_vis_utgbs[j] +  [[curr_acemaestro, curr_utgbs]]
               if (setting==3) and (type(curr_utgbs.sPV_layers)==list) and (type(curr_acemaestro.sPV_layers)==list) and ( abs((curr_utgbs.sPV_layers)[0][0] - (curr_acemaestro.sPV_layers)[0][0]) <= margin )  and ( abs((curr_utgbs.sPV_layers)[0][1] - (curr_acemaestro.sPV_layers)[0][1]) <= margin ) and ( abs((curr_utgbs.sPV_layers)[0][2] - (curr_acemaestro.sPV_layers)[0][2]) <= margin ) and ( abs((curr_utgbs.sPV_layers)[0][3] - (curr_acemaestro.sPV_layers)[0][3]) <= margin ):
                  if curr_acemaestro.uvvis==0: # UV Spectrum:
                     p_uv_utgbs[j] = p_uv_utgbs[j] +  [[curr_acemaestro, curr_utgbs]  ]   
                  elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                     p_vis_utgbs[j] = p_vis_utgbs[j] +  [[curr_acemaestro, curr_utgbs]]

      # Search for corresponding DIAL measurements.
      for j in range(0,number_of_dial,1):
         curr_dial = dial[j]
         radius = distance([curr_acemaestro.latitude,curr_acemaestro.longitude],[curr_dial.latitude,curr_dial.longitude])
         # Check that the measurements are within a 500 km radius.
         if (radius <= 500):
            # Check for temporal coincidence.
            e = 99999999999
            if (type(curr_dial.datetime)==datetime==type(curr_acemaestro.datetime)==datetime):
               e = (curr_dial.datetime - curr_acemaestro.datetime).total_seconds()
            if (abs(e) < 86400): # If less than 12 hours have elapsed.
               if setting==0:
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_dial[j] = p_uv_dial[j] +  [[curr_acemaestro, curr_dial]]     
                   elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_dial[j] = p_vis_dial[j] +  [[curr_acemaestro, curr_dial]]                                                                    
               if (setting==1) and (type(curr_dial.sPV_layers )==list) and (type(curr_acemaestro.sPV_layers)==list) and ( ( (curr_dial.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 0 ) or ( (curr_dial.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 2 ) ) and ( ( (curr_dial.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 0 ) or ( (curr_dial.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 2 ) ) and ( ( (curr_dial.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 0 ) or ( (curr_dial.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 2 ) ) and ( ( (curr_dial.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 0 ) or ( (curr_dial.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 2 ) ):
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_dial[j] = p_uv_dial[j] +  [[curr_acemaestro, curr_dial]]     
                   if curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_dial[j] = p_vis_dial[j] +  [[curr_acemaestro, curr_dial]] 
               if (setting==2) and (type(curr_dial.sPV_layers)==list) and (type(curr_acemaestro.sPV_layers)==list) and ( ( (curr_dial.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 0 ) or ( (curr_dial.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 2 ) or ( (curr_dial.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == -1998 ) ) and ( ( (curr_dial.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 0 ) or ( (curr_dial.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 2 ) or ( (curr_dial.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == -1998 ) ) and ( ( (curr_dial.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 0 ) or ( (curr_dial.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 2 ) or ( (curr_dial.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == -1998 ) ) and ( ( (curr_dial.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 0 ) or ( (curr_dial.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 2 ) or ( (curr_dial.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == -1998 ) ):
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_dial[j] = p_uv_dial[j] +  [[curr_acemaestro, curr_dial]]     
                   elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_dial[j] = p_vis_dial[j] +  [[curr_acemaestro, curr_dial]] 
               if (setting==3) and (type(curr_dial.sPV_layers)==list) and (type(curr_acemaestro.sPV_layers)==list) and ( abs((curr_dial.sPV_layers)[0][0] - (curr_acemaestro.sPV_layers)[0][0]) <= margin )  and ( abs((curr_dial.sPV_layers)[0][1] - (curr_acemaestro.sPV_layers)[0][1]) <= margin ) and ( abs((curr_dial.sPV_layers)[0][2] - (curr_acemaestro.sPV_layers)[0][2]) <= margin ) and ( abs((curr_dial.sPV_layers)[0][3] - (curr_acemaestro.sPV_layers)[0][3]) <= margin ):
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_dial[j] = p_uv_dial[j] +  [[curr_acemaestro, curr_dial]]     
                   elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_dial[j] = p_vis_dial[j] +  [[curr_acemaestro, curr_dial]] 

      # Search for corresponding FTIR measurements.
      for j in range(0,number_of_ftir,1):
         curr_ftir = ftir[j]
         radius = distance([curr_acemaestro.latitude,curr_acemaestro.longitude],[curr_ftir.latitude,curr_ftir.longitude])
         # Check that the measurements are within a 500 km radius.
         if (radius <= 500):
            # Check for temporal coincidence.
            e = 99999999999
            if (type(curr_ftir.datetime)==datetime==type(curr_acemaestro.datetime)==datetime):
               e = (curr_ftir.datetime - curr_acemaestro.datetime).total_seconds()
            if (abs(e) < 86400): # If less than 12 hours have elapsed.
               if setting==0:
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_ftir[j] = p_uv_ftir[j] +  [[curr_acemaestro, curr_ftir]]     
                   elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_ftir[j] = p_vis_ftir[j] +  [[curr_acemaestro, curr_ftir]]                                                                    
               if (setting==1) and (type(curr_ftir.sPV_layers )==list) and (type(curr_acemaestro.sPV_layers)==list) and ( ( (curr_ftir.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 0 ) or ( (curr_ftir.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 2 ) ) and ( ( (curr_ftir.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 0 ) or ( (curr_ftir.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 2 ) ) and ( ( (curr_ftir.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 0 ) or ( (curr_ftir.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 2 ) ) and ( ( (curr_ftir.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 0 ) or ( (curr_ftir.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 2 ) ):
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_ftir[j] = p_uv_ftir[j] +  [[curr_acemaestro, curr_ftir]]     
                   if curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_ftir[j] = p_vis_ftir[j] +  [[curr_acemaestro, curr_ftir]] 
               if (setting==2) and (type(curr_ftir.sPV_layers)==list) and (type(curr_acemaestro.sPV_layers)==list) and ( ( (curr_ftir.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 0 ) or ( (curr_ftir.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == 2 ) or ( (curr_ftir.sPV_layers)[1][0] + (curr_acemaestro.sPV_layers)[1][0] == -1998 ) ) and ( ( (curr_ftir.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 0 ) or ( (curr_ftir.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == 2 ) or ( (curr_ftir.sPV_layers)[1][1] + (curr_acemaestro.sPV_layers)[1][1] == -1998 ) ) and ( ( (curr_ftir.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 0 ) or ( (curr_ftir.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == 2 ) or ( (curr_ftir.sPV_layers)[1][2] + (curr_acemaestro.sPV_layers)[1][2] == -1998 ) ) and ( ( (curr_ftir.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 0 ) or ( (curr_ftir.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == 2 ) or ( (curr_ftir.sPV_layers)[1][3] + (curr_acemaestro.sPV_layers)[1][3] == -1998 ) ):
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_ftir[j] = p_uv_ftir[j] +  [[curr_acemaestro, curr_ftir]]     
                   elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_ftir[j] = p_vis_ftir[j] +  [[curr_acemaestro, curr_ftir]] 
               if (setting==3) and (type(curr_ftir.sPV_layers)==list) and (type(curr_acemaestro.sPV_layers)==list) and ( abs((curr_ftir.sPV_layers)[0][0] - (curr_acemaestro.sPV_layers)[0][0]) <= margin )  and ( abs((curr_ftir.sPV_layers)[0][1] - (curr_acemaestro.sPV_layers)[0][1]) <= margin ) and ( abs((curr_ftir.sPV_layers)[0][2] - (curr_acemaestro.sPV_layers)[0][2]) <= margin ) and ( abs((curr_ftir.sPV_layers)[0][3] - (curr_acemaestro.sPV_layers)[0][3]) <= margin ):
                   if curr_acemaestro.uvvis==0: # UV Spectrum:
                      p_uv_ftir[j] = p_uv_ftir[j] +  [[curr_acemaestro, curr_ftir]]     
                   elif curr_acemaestro.uvvis==1: # VIS Spectrum: 
                      p_vis_ftir[j] = p_vis_ftir[j] +  [[curr_acemaestro, curr_ftir]]         

   # We are now done looking for comparisons between ACE-FTS and other instruments.
   # For each measurement, if we have more than one coincident pair, choose the 'best' coincident pair using pairAnalyzer.
   #print('ACE-MAESTRO O3SONDE \n')
   for i in range(0,len(p_uv_sonde),1): # For all sonde measurements (with ACE-MAESTRO-UV).
      index = pairAnalyzer(p_uv_sonde[i]) # Find the best coincident pair for this sonde measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_uv_sonde[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acemaestro_uv_sondes = pairAdder(cm_acemaestro_uv_sondes,p_uv_sonde[i][index][0],p_uv_sonde[i][index][1])
          # Update comparison list.
   for i in range(0,len(p_vis_sonde),1): # For all sonde measurements (with ACE-MAESTRO-VIS).
      index = pairAnalyzer(p_vis_sonde[i]) # Find the best coincident pair for this sonde measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_vis_sonde[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acemaestro_vis_sondes = pairAdder(cm_acemaestro_vis_sondes,p_vis_sonde[i][index][0],p_vis_sonde[i][index][1])
          # Update comparison list.
          
          
   #print('ACE-MAESTRO PEARL-GBS \n')
   for i in range(0,len(p_uv_pearlgbs),1): # For all PEARL-GBS measurements.
      index = pairAnalyzer(p_uv_pearlgbs[i]) # Find the best coincident pair for this PEARL-GBS measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_uv_pearlgbs[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acemaestro_uv_pearlgbs = pairAdder(cm_acemaestro_uv_pearlgbs,p_uv_pearlgbs[i][index][0],p_uv_pearlgbs[i][index][1])
          # Update comparison list.
   for i in range(0,len(p_vis_pearlgbs),1): # For all PEARL-GBS measurements.
      index = pairAnalyzer(p_vis_pearlgbs[i]) # Find the best coincident pair for this PEARL-GBS measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_vis_pearlgbs[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acemaestro_vis_pearlgbs = pairAdder(cm_acemaestro_vis_pearlgbs,p_vis_pearlgbs[i][index][0],p_vis_pearlgbs[i][index][1])
          # Update comparison list.
   #print('ACE-MAESTRO UT-GBS \n')
   for i in range(0,len(p_uv_utgbs),1): # For all UTGBS measurements.
      index = pairAnalyzer(p_uv_utgbs[i]) # Find the best coincident pair for this UT-GBS measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_uv_utgbs[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acemaestro_uv_utgbs = pairAdder(cm_acemaestro_uv_utgbs,p_uv_utgbs[i][index][0],p_uv_utgbs[i][index][1])
          # Update comparison list.
   for i in range(0,len(p_vis_utgbs),1): # For all UTGBS measurements.
      index = pairAnalyzer(p_vis_utgbs[i]) # Find the best coincident pair for this UT-GBS measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_vis_utgbs[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acemaestro_vis_utgbs = pairAdder(cm_acemaestro_vis_utgbs,p_vis_utgbs[i][index][0],p_vis_utgbs[i][index][1])
          # Update comparison list.                  
   #print('ACE-MAESTRO DIAL \n')
   for i in range(0,len(p_uv_dial),1): # For all DIAL measurements (with ACE-MAESTRO-UV).
      index = pairAnalyzer(p_uv_dial[i]) # Find the best coincident pair for this  measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_uv_dial[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acemaestro_uv_dial = pairAdder(cm_acemaestro_uv_dial,p_uv_dial[i][index][0],p_uv_dial[i][index][1])
          # Update comparison list.
   for i in range(0,len(p_vis_dial),1): # For all DIAL measurements (with ACE-MAESTRO-VIS).
      index = pairAnalyzer(p_vis_dial[i]) # Find the best coincident pair for this measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_vis_dial[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acemaestro_vis_dial = pairAdder(cm_acemaestro_vis_dial,p_vis_dial[i][index][0],p_vis_dial[i][index][1])
          # Update comparison list.           
   #print('ACE-MAESTRO FTIR \n')
   for i in range(0,len(p_uv_ftir),1): # For all FTIR measurements (with ACE-MAESTRO-UV).
      index = pairAnalyzer(p_uv_ftir[i]) # Find the best coincident pair for this  measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_uv_ftir[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acemaestro_uv_ftir = pairAdder(cm_acemaestro_uv_ftir,p_uv_ftir[i][index][0],p_uv_ftir[i][index][1])
          # Update comparison list.
   for i in range(0,len(p_vis_ftir),1): # For all FTIR measurements (with ACE-MAESTRO-VIS).
      index = pairAnalyzer(p_vis_ftir[i]) # Find the best coincident pair for this measurement.
      if numpy.isnan(index)==False: # Check for valid index output.
          best = p_vis_ftir[i][index] # This is the best pair.
          # Now add the pair to the coincident measurement list.
          cm_acemaestro_vis_ftir = pairAdder(cm_acemaestro_vis_ftir,p_vis_ftir[i][index][0],p_vis_ftir[i][index][1])
          # Update comparison list. 
          
   return  [cm_acefts_acemaestro_uv, cm_acefts_acemaestro_vis, cm_acefts_sondes,cm_acemaestro_uv_sondes,cm_acemaestro_vis_sondes,cm_acefts_pearlgbs,cm_acemaestro_uv_pearlgbs,cm_acemaestro_vis_pearlgbs,cm_acefts_utgbs,cm_acemaestro_uv_utgbs,cm_acemaestro_vis_utgbs,cm_acefts_dial,cm_acemaestro_uv_dial,cm_acemaestro_vis_dial,cm_acefts_ftir, cm_acemaestro_uv_ftir, cm_acemaestro_vis_ftir, cm_acefts_brewer,cm_acemaestro_brewer]
