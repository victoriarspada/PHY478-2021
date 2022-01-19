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
from ButterflyMap import *
import numpy 
import matplotlib.pyplot as plt
from delta_abs_rel import *
from pair import pair
from instrument import instrument
import os
import pickle
from pair_update import *
from analyze_divisions import *
from vmrPlotter_sections import * 
from diffPlotter_sections import *

folder = "Figures" # Choose which folders the figures being made should be saved in. 

acemaestro_uvvis = []
for i in range(0,8,1):
    year = 2004+i
    pickle_in = open("acemaestro_uvvis_"+str(year)+"_vmranalyzed_div.pickle","rb")
    open_meas = pickle.load(pickle_in) #Open the pickle file
    acemaestro_uvvis = acemaestro_uvvis + [ open_meas['pair'] ]
    pickle_in.close()
    
# pickle_in = open("acemaestro_uvvis_"+str(year)+"_vis_info_arrays.pickle","rb")
# open_meas = pickle.load(pickle_in) #Open the pickle file
# o3_vmr_vis = open_meas['o3_vmr']
# o3_vmr_error_vis = open_meas['o3_vmr_error']
# retrievals_vis = open_meas['retrievals']
# dates_vis = open_meas['dates']
# longitudes_vis = open_meas['longitudes']
# latitudes_vis = open_meas['latitudes']
# pickle_in.close()

# pickle_in = open("acemaestro_uvvis_"+str(year)+"_uv_info_arrays.pickle","rb")
# open_meas = pickle.load(pickle_in) #Open the pickle file
# o3_vmr_uv = open_meas['o3_vmr']
# o3_vmr_error_uv= open_meas['o3_vmr_error']
# retrievals_uv = open_meas['retrievals']
# dates_uv = open_meas['dates']
# longitudes_uv = open_meas['longitudes']
# latitudes_uv = open_meas['latitudes']
# pickle_in.close()

# print('ACE-MAESTRO-UV & VIS')
# # acemaestro_uvvis = vmrAnalysis(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs)
# acemaestro_uvvis = analyze_divisions(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs)
# print('Done VMR Analysis')

# a = {'pair' : acemaestro_uvvis}
# pickle_out = open("acemaestro_uvvis_"+str(year)+"_vmranalyzed_div.pickle","wb")
# pickle.dump(a, pickle_out)
# pickle_out.close()

diffPlotter_all(acemaestro_uvvis,'ACE-MAESTRO-UV vs. ACE-MAESTRO-VIS O3 VMR ',['ACE-MAESTRO-UV (ppv)','ACE-MAESTRO-VIS (ppv)'])

# diffPlotter_sections(acemaestro_uvvis,'ACE-MAESTRO-UV vs. ACE-MAESTRO-VIS O3 VMR ',['ACE-MAESTRO-UV (ppv)','ACE-MAESTRO-VIS (ppv)'])
# vmrPlotter_sections(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs,'ACE-MAESTRO-UV vs. ACE-MAESTRO-VIS O3 VMR ','ACE-MAESTRO-UV vs. ACE-MAESTRO-VIS O3 VMR Absolute Differences',['ACE-MAESTRO-UV (ppv)','ACE-MAESTRO-VIS (ppv)'],year)
# vmrPlotter(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs,'ACE-MAESTRO-UV vs. ACE-MAESTRO-VIS O3 VMR ','ACE-MAESTRO-UV vs. ACE-MAESTRO-VIS O3 VMR Absolute Differences',['ACE-MAESTRO-UV (ppv)','ACE-MAESTRO-VIS (ppv)'],year)
# vmrColorbar(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs,'ACE-MAESTRO-UV vs. ACE-MAESTRO-VIS O3 VMR',['ACE-MAESTRO-UV [ppv]','ACE-MAESTRO-VIS [ppv]'],folder,year)
# diff, diff_err, rel_diff, rel_diff_err = averageVMRComparePlotter(acemaestro_uvvis,['ACE-MAESTRO-UV','ACE-MAESTRO-VIS'],folder,year)  

# acemaestro_uvvis.o3_vmr_mean_absolute_diff_arr = diff
# acemaestro_uvvis.o3_vmr_mean_absolutee_diff_err_arr = diff_err
# acemaestro_uvvis.o3_vmr_mean_relative_diff_arr = rel_diff
# acemaestro_uvvis.o3_vmr_mean_relative_diff_err_arr = rel_diff_err

# a = {'pair' : acemaestro_uvvis}
# pickle_out = open("acemaestro_uvvis_2011_vmranalyzed.pickle","wb")
# pickle.dump(a, pickle_out)
# pickle_out.close()

# O3VMRHeatMap(o3_vmr_vis,dates_vis,retrievals_vis,latitudes_vis,longitudes_vis,year,'vis')
# O3VMRHeatMap(o3_vmr_uv,dates_uv,retrievals_uv,latitudes_uv,longitudes_uv,year,'uv')
# WorldMap(o3_vmr_vis,dates_vis,latitudes_vis,longitudes_vis,year,'vis')
# WorldMap(o3_vmr_uv,dates_uv,latitudes_uv,longitudes_uv,year,'uv')
# ButterflyMap(o3_vmr_uv,dates_uv,latitudes_uv,year,'uv')
# ButterflyMap(o3_vmr_vis,dates_vis,latitudes_vis,year,'vis')
#DifferencesHeatMap([acemaestro_uvvis])

# csvfilename = 'acemaestro_uvvis_numbers.txt'
# csvWrite(csvfilename,0,[acemaestro_uvvis])
