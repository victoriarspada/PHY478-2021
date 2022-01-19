# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 10:16:23 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: August 20 2020.
"""
# This file contains a program for the analysis of files for various instruments over the years 2004-2020.
# Comparisons are done between the ACE-FTS & ACE-MAESTRO aboard the SCISAT satellite with ACE Campaign ozonesondes,
# Brewer, DIAL, PEARL-GBS, and UT-GBS.
# The program reads all of the files related to these instruments that exist in subfolders of the current working directory.
# The program looks for subfolders with names of years (ie, '2004', '2005') and looks within these folders for instrument
# files of type .asc, .txt, .csv, and .dat. DMP files are also scanned for, and if they exist, are read for each measurement.
# The measurements are then saved to a .pickle file.
# The measurements are also saved into 'pair' objects into pickle files, and also put into 'instrument' objects and saved into pickle files.

from csvWrite import *
from ACEMAESTROPlotter import * 

import numpy 
from delta_abs_rel import *
from pair import pair
from measurement import measurement
from CoincidentPairs_acemaestroUVVIS import *
from instrument import instrument
import os
import pickle

acefts = []
acemaestro = []
acemaestro_uv = []
acemaestro_vis = [] 

acemaestro_byyear = []
acemaestro_uv_byyear = []
acemaestro_vis_byyear = []

acemaestro_byyear_andmonth = []
acemaestro_uv_byyear_andmonth = []
acemaestro_vis_byyear_andmonth = []

folders = [f for f in os.listdir('.') if os.path.isdir(f)] # Create list of all folders in current working directory.
years = []
parent_directory = os.getcwd() # Find current working directory. We will look at folders inside the CWD.
for f in folders:
    if (f[0:4]=='mae_'):  # If the file has a year title" 
      years = years + [f]
for i in range(0,2,1): # Cycle through all years (2004-2020).
      u, v = [], []
      curr_year = parent_directory + '\\' + years[i]
      os.chdir(curr_year) 
      print('ACE-MAESTRO',years[i])
      curr_folders = [g for g in os.listdir('.') if os.path.isdir(g)] # Create list of all folders in current working directory.
      print(curr_folders)
      for g in curr_folders:
          curr_month = curr_year + '\\' + g
          os.chdir(curr_month)
          print('ACE-MAESTRO',years[i],g)

          acemaestro_uv_curr, acemaestro_vis_curr = ACEMAESTROPlotter()
      
          v = v + [acemaestro_vis_curr]
          u = u + [acemaestro_uv_curr]
          acemaestro_vis = acemaestro_vis + acemaestro_vis_curr
          acemaestro_uv = acemaestro_uv + acemaestro_uv_curr          

      acemaestro_vis_byyear_andmonth = acemaestro_vis_byyear_andmonth + [v]
      acemaestro_uv_byyear_andmonth = acemaestro_uv_byyear_andmonth + [u]
      acemaestro_vis_byyear = acemaestro_vis_byyear + [acemaestro_vis_curr]  
      acemaestro_uv_byyear = acemaestro_uv_byyear + [acemaestro_uv_curr] 
      
os.chdir(parent_directory)

# Now save the measurements to a dictionary in a file.
# ACE-MAESTRO-UV
a = instrument()
a.measurements = acemaestro_uv
a.measurements_by_year = acemaestro_uv_byyear
a.measurements_by_year_and_month = acemaestro_vis_byyear_andmonth
b = {'ACE-MAESTRO-UV': a }
pickle_out = open("acemaestro_uv.pickle","wb")
pickle.dump(b, pickle_out) # Save instrument object to a pickle.
pickle_out.close()

# ACE-MAESTRO-VIS
a = instrument()
a.measurements = acemaestro_vis
a.measurements_by_year = acemaestro_vis_byyear
a.measurements_by_year_and_month = acemaestro_vis_byyear_andmonth
b = {'ACE-MAESTRO-VIS': a }
pickle_out = open("acemaestro_vis.pickle","wb")
pickle.dump(b, pickle_out) # Save instrument object to a pickle.
pickle_out.close()

# ACE-MAESTRO UV/VIS PAIR
acemaestro_uvvis = pair()
acemaestro_uvvis.instrument_1 = acemaestro_uv_byyear
acemaestro_uvvis.instrument_2 = acemaestro_vis_byyear
b = {'ACE-MAESTRO-UVVIS': acemaestro_uvvis }
pickle_out = open("acemaestro_vis.pickle","wb")
pickle.dump(b, pickle_out) # Save pair object to a pickle.
pickle_out.close()

parent_directory = os.getcwd() # Find current working directory. We will look at folders inside the CWD.
# Now we will find CoincidentPairs and find the measurement pairs for
# each setting and save the pickle files with the coincident pair 'pair' objects in their respective folders.
for i in range(0,len(acemaestro_vis_byyear_andmonth),1): # For each year
    print('year 2004 +',i)
    for j in range(0,len(acemaestro_vis_byyear_andmonth[i]),1):
        pairs = CoincidentPairs(acemaestro_vis_byyear_andmonth[i][j],acemaestro_vis_byyear_andmonth[i][j]) # Augment list of coincident pairs for each year
        acemaestro_uvvis.coincident_pairs = acemaestro_uvvis.coincident_pairs + pairs

a = {'pair' : acemaestro_uvvis}
pickle_out = open("acemaestro_uvvis.pickle","wb")
pickle.dump(a, pickle_out)
pickle_out.close()

 
  