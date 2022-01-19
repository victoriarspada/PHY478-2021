# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 13:00:41 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
"""
# Setting option for coincidence criteria: setting
#0 : within 12 hr and 500 km
#1 : within 12 hr, 500 km, same spv range ( <1.2 10^-4 s^01 or <1.6 10^-4 s^-1)
#2 : within 12 hr, 500 km, same spv range ( <1.2 10^-4 s^01 or <1.6 10^-4 s^-1), or somewhere in between
#3 : within 12 h4, 500 km, and within a margin (input) of sPV at selected layers.

# Setting option for 1-1 plotting
#0: many-to-one plotting
#1: one-to-one plotting

from distance import *
import numpy
import datetime
from ACEMAESTROPlotter import *

def CoincidentPairs(acemaestro_uv,acemaestro_vis):
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
   
   cm_acemaestro_uvvis=[]

   # Extract number of csv files for the ozonesondes.
   number_of_uv = len(acemaestro_uv)
   # Extract number of asc files for the ACEFTS.
   number_of_vis = len(acemaestro_vis)

# Sort through all ACE-MAESTRO UV & VIS readings, pairing corresponding occultations (noting each version).
# Note that ACE-FTS and ACE-MAESTRO have coincident occultations, so if an instrument is coincident with
# ACE-FTS, it is also coincident with ACE-MAESTRO for that same occultation ID.
   for i in range(0,number_of_uv,1):
      curr_acemaestro_uv = acemaestro_uv[i] # measurement object

      for j in range(0,number_of_vis,1):
         curr_acemaestro_vis = acemaestro_vis[j] # measurement object 
         if (curr_acemaestro_vis.occultation_ID == curr_acemaestro_uv.occultation_ID) and type(curr_acemaestro_uv.datetime)==datetime.datetime and type(curr_acemaestro_vis.datetime)==datetime.datetime:
                cm_acemaestro_uvvis = cm_acemaestro_uvvis + [[curr_acemaestro_uv, curr_acemaestro_vis]] # Add coincident occultations (same ID).
             
   return  cm_acemaestro_uvvis