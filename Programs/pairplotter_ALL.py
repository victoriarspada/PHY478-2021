# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 10:16:23 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: February 21 2020.
"""
# This file contains a program for the comparison of measurements from files for various instruments over the years 
# 2004-2020.
# Comparisons are done between the ACE-FTS & ACE-MAESTRO aboard the SCISAT satellite with ACE Campaign ozonesondes,
# DIAL, FTIR, PEARL-GBS, and UT-GBS.
# The  assumes that all of the measurements have been read from the appropariate files (see main.py), and that coincident
# measurements have been found.
# It assumes that the coincident pairs list has been stored into a 'pair' objects for every comparison we want to do. 
# (there should be a .pickle file carrying a 'pair' class object with the full lists of all measurements being used for
# that comparisons)
# The program calls functions to perform linear regression (ordinary least squares and reduced major axis) of
# instrument comparisons for coincident measurements of number densities and partial/total columns for O3.
# For these comparisons, regression plots of number densities and columns, tables documenting key values, plots of
# absolute differences, and figures with regression subplots are created and saved in the folder that is inputted.
# The resulting regression and metrics are stored to the 'pair' object and the pockle file is updated for each instrument pair.
# csvWrite is also called to save the results in a csv file.

from csvWrite import *
from averageVMRComparePlotter import *
from vmrPlotter import *
from VMRanalysis import *
from averageVMRHeatMap_monthly import * 

import numpy 
import matplotlib.pyplot as plt
from delta_abs_rel import *
from pair import pair
from instrument import instrument
import os
import pickle

folder = "Figures" # Choose which folders the figures being made should be saved in. 
year = str(2004-2011)

pickle_in = open("acemaestro_uvvis_2004_vmranalyzed.pickle","rb")
open_meas = pickle.load(pickle_in) #Open the pickle file
acemaestro_uvvis_2004 = open_meas['pair']
pickle_in.close()
pickle_in = open("acemaestro_uvvis_2005_vmranalyzed.pickle","rb")
open_meas = pickle.load(pickle_in) #Open the pickle file
acemaestro_uvvis_2005 = open_meas['pair']
pickle_in.close()
pickle_in = open("acemaestro_uvvis_2006_vmranalyzed.pickle","rb")
open_meas = pickle.load(pickle_in) #Open the pickle file
acemaestro_uvvis_2006 = open_meas['pair']
pickle_in.close()
pickle_in = open("acemaestro_uvvis_2007_vmranalyzed.pickle","rb")
open_meas = pickle.load(pickle_in) #Open the pickle file
acemaestro_uvvis_2007 = open_meas['pair']
pickle_in.close()
pickle_in = open("acemaestro_uvvis_2008_vmranalyzed.pickle","rb")
open_meas = pickle.load(pickle_in) #Open the pickle file
acemaestro_uvvis_2008 = open_meas['pair']
pickle_in.close()
pickle_in = open("acemaestro_uvvis_2009_vmranalyzed.pickle","rb")
open_meas = pickle.load(pickle_in) #Open the pickle file
acemaestro_uvvis_2009 = open_meas['pair']
pickle_in.close()
pickle_in = open("acemaestro_uvvis_2010_vmranalyzed.pickle","rb")
open_meas = pickle.load(pickle_in) #Open the pickle file
acemaestro_uvvis_2010 = open_meas['pair']
pickle_in.close()
pickle_in = open("acemaestro_uvvis_2011_vmranalyzed.pickle","rb")
open_meas = pickle.load(pickle_in) #Open the pickle file
acemaestro_uvvis_2011 = open_meas['pair']
pickle_in.close()

acemaestro_uvvis = pair()
acemaestro_uvvis.coincident_pairs = acemaestro_uvvis_2004 + acemaestro_uvvis_2005 + 
                                acemaestro_uvvis_2006 + acemaestro_uvvis_2007 + 
                                acemaestro_uvvis_2008 + acemaestro_uvvis_2009 + 
                                acemaestro_uvvis_2010 acemaestro_uvvis_2011

print('ACE-MAESTRO-UV & VIS')
acemaestro_uvvis = vmrAnalysis(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs)
print('Done VMR Analysis')

acemaestro_uvvis.coincident_pairs = []
a = {'pair' : acemaestro_uvvis}
pickle_out = open("acemaestro_uvvis_2005_vmranalyzed.pickle","wb")
pickle.dump(a, pickle_out)
pickle_out.close()
acemaestro_uvvis.coincident_pairs = acemaestro_uvvis_2004 + acemaestro_uvvis_2005 + 
                                acemaestro_uvvis_2006 + acemaestro_uvvis_2007 + 
                                acemaestro_uvvis_2008 + acemaestro_uvvis_2009 + 
                                acemaestro_uvvis_2010 acemaestro_uvvis_2011

vmrPlotter(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs,'ACE-MAESTRO-UV vs. ACE-MAESTRO-VIS O3 VMR ','ACE-MAESTRO-UV vs. ACE-MAESTRO-VIS O3 VMR Absolute Differences',['ACE-MAESTRO-UV (ppv)','ACE-MAESTRO-VIS (ppv)'],year)
vmrColorbar(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs,'ACE-MAESTRO-UV vs. ACE-MAESTRO-VIS O3 VMR',['ACE-MAESTRO-UV [ppv]','ACE-MAESTRO-VIS [ppv]'],folder,year)
averageVMRComparePlotter(acemaestro_uvvis,['ACE-MAESTRO-UV','ACE-MAESTRO-VIS'],folder,year)  
DifferencesHeatMap([acemaestro_uvvis_2004, acemaestro_uvvis_2005, ace_maestro_uvvis_2006, ace_maestro_uvvis_2007, ace_maestro_uvvis_2008, ace_maestro_uvvis_2009, ace_maestro_uvvis_2010, ace_maestro_uvvis_2011])

# csvfilename = 'acemaestro_uvvis_numbers.txt'
# csvWrite(csvfilename,0,[acemaestro_uvvis])
