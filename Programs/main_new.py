# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 10:16:23 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: Feb 20 2021.
"""
# This file contains a program for the analysis of files for various instruments over the years 2004-2020.
# Comparisons are done between the ACE-FTS & ACE-MAESTRO aboard the SCISAT satellite with ACE Campaign ozonesondes,
# Brewer, DIAL, PEARL-GBS, and UT-GBS.
# The program reads all of the files related to these instruments that exist in subfolders of the current working directory.
# The program looks for subfolders with names of years (ie, '2004', '2005') and looks within these folders for instrument
# files of type .asc, .txt, .csv, and .dat. DMP files are also scanned for, and if they exist, are read for each measurement.
# The measurements are then saved to a .pickle file.
# The measurements are also saved into 'pair' objects into pickle files, and also put into 'instrument' objects and saved into pickle files.

from ACEMAESTROPlotter import * 

import numpy 
from pair import pair
from measurement import measurement
from CoincidentPairs_acemaestroUVVIS import *
from instrument import instrument
import os
import pickle

from AltitudeModeller import *

acemaestro = []
acemaestro_uv = []
acemaestro_vis = [] 

acemaestro_byyear = []
acemaestro_uv_byyear = []
acemaestro_vis_byyear = []

folders = [f for f in os.listdir('.') if os.path.isdir(f)] # Create list of all folders in current working directory.
years = []
parent_directory = os.getcwd() # Find current working directory. We will look at folders inside the CWD.
for f in folders:
    if (f[0:4]=='mae_'):  # If the file has a year title" 
        years = years + [f]
for i in range(6,7,1): # Cycle through all years (2004-2020)
    year = 2010

    u, v = [], []
    curr_year = parent_directory + '\\' + years[i]
    os.chdir(curr_year) 
    print('ACE-MAESTRO',years[i])
    curr_folders = [g for g in os.listdir('.') if os.path.isdir(g)] # Create list of all folders in current working directory.
    print(curr_folders)
      
    ss=open('SunsetTable.txt','r') # Open and read the data file.
    sunset = ss.readlines()
    sr=open('SunriseTable.txt','r') # Open and read the data file.
    sunrise = sr.readlines()
       
    for g in curr_folders:
        curr_month = curr_year + '\\' + g
        os.chdir(curr_month)
        print('ACE-MAESTRO',years[i],g)

        acemaestro_uv_curr, acemaestro_vis_curr = ACEMAESTROPlotter(sunset, sunrise)
      
        v = v + acemaestro_vis_curr
        u = u + acemaestro_uv_curr

        acemaestro_vis_byyear = acemaestro_vis_byyear + [acemaestro_vis_curr]  
        acemaestro_uv_byyear = acemaestro_uv_byyear + [acemaestro_uv_curr] 

    # Now save the measurements to a dictionary in a file.
    # ACE-MAESTRO-UV
    # Go through each year. 
    a = instrument()
    a.measurements_by_year = acemaestro_uv_byyear
    b = {'ACE-MAESTRO-UV': a }
    name = parent_directory+"\\acemaestro_uv_"+str(year)+".pickle"
    pickle_out = open(name,"wb")
    pickle.dump(b, pickle_out) # Save instrument object to a pickle.
    pickle_out.close()

    # ACE-MAESTRO-VIS
    a = instrument()
    a.measurements_by_year = acemaestro_vis_byyear
    b = {'ACE-MAESTRO-VIS': a }
    name = parent_directory+"\\acemaestro_vis_"+str(year)+".pickle"
    pickle_out = open(name,"wb")
    pickle.dump(b, pickle_out) # Save instrument object to a pickle.
    pickle_out.close()

    # ACE-MAESTRO UV/VIS PAIR
    acemaestro_uvvis = pair()
    acemaestro_uvvis.instrument_1 = acemaestro_uv_byyear
    acemaestro_uvvis.instrument_2 = acemaestro_vis_byyear

os.chdir(parent_directory)

parent_directory = os.getcwd() # Find current working directory. We will look at folders inside the CWD.
# Now we will find CoincidentPairs and find the measurement pairs for
# each setting and save the pickle files with the coincident pair 'pair' objects in their respective folders.
for i in range(0,len(acemaestro_vis_byyear),1): # For each month
    print('year ',year,' + ',i)
    pairs = CoincidentPairs(acemaestro_uv_byyear[i],acemaestro_vis_byyear[i]) # Augment list of coincident pairs for each year
    acemaestro_uvvis.coincident_pairs = acemaestro_uvvis.coincident_pairs + pairs

b = {'pair': acemaestro_uvvis }
name = "acemaestro_uvvis_"+str(year)+".pickle"
pickle_out = open(name,"wb")
pickle.dump(b, pickle_out) # Save pair object to a pickle.
pickle_out.close()

AltitudeModeller(u,year,'uv')
AltitudeModeller(v,year,'vis')


 
  