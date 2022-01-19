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
from averageVMRComparePlotter_interp import *
from vmrPlotter import *
from VMRanalysis_v313 import *
from averageVMRHeatMap_monthly import * 
from ButterflyMap import *
import numpy 
import matplotlib.pyplot as plt
from delta_abs_rel import *
from pair import pair
from measurement import *
from instrument import instrument
import os
import pickle
from vmrPlotter_sections import *
from analyze_divisions import *
from diffPlotter_sections import *
from diffPlotter_profile_sections import *

# folder = "Figures" # Choose which folders the figures being made should be saved in. 
# year = 2011

# pickle_in = open("acemaestro_visvis_"+str(year)+"_3.13_vmranalyzed_div.pickle","rb")
# open_meas = pickle.load(pickle_in) #Open the pickle file
# acemaestro_uvvis = open_meas['pair']
# pickle_in.close()

# acemaestro_uvvis, acemaestro_uvvis_all = [],[[],[],[]]
# for i in range(0,8,1):
#     year = 2004+i
#     pickle_in = open("acemaestro_uvvis_"+str(year)+"_3.13_vmranalyzed_div.pickle","rb")
#     open_meas = pickle.load(pickle_in) #Open the pickle file
#     acemaestro_uvvis = acemaestro_uvvis + [ open_meas['pair'] ]
#     pickle_in.close()

for i in range(0,8,1):
    year = 2004+i
    print(i)
    pickle_in = open("acemaestro_uvvis_"+str(year)+"_3.13_vmranalyzed_div.pickle","rb")
    open_meas = pickle.load(pickle_in) #Open the pickle file
    acemaestro_uvvis_all[0] = acemaestro_uvvis_all[0] + [ open_meas['pair'] ]
    pickle_in.close()
    pickle_in = open("acemaestro_visvis_"+str(year)+"_3.13_vmranalyzed_div.pickle","rb")
    open_meas = pickle.load(pickle_in) #Open the pickle file
    acemaestro_uvvis_all[1] = acemaestro_uvvis_all[1] + [ open_meas['pair'] ]
    pickle_in.close()
    pickle_in = open("acemaestro_uvvis_"+str(year)+"_vmranalyzed_div.pickle","rb")
    open_meas = pickle.load(pickle_in) #Open the pickle file
    acemaestro_uvvis_all[2] = acemaestro_uvvis_all[2] + [ open_meas['pair'] ]
    pickle_in.close()    

# diffPlotter_all(acemaestro_uvvis,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-UV (1.2) O3 VMR ',['ACE-MAESTRO-VIS (3.13) (ppv)','ACE-MAESTRO-UV (1.2) (ppv)'])

# diffPlotter_sections(acemaestro_uvvis,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-UV (1.2) O3 VMR ',['ACE-MAESTRO-VIS (3.13) (ppv)','ACE-MAESTRO-UV (1.2) (ppv)'])
# vmrPlotter_sections(acemaestro_uvvis[0],acemaestro_uvvis[0].coincident_pairs,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-UV (1.2) O3 VMR ',['ACE-MAESTRO-VIS (3.13) (ppv)','ACE-MAESTRO-UV (1.2) (ppv)'],year)

# vmrPlotter_sections_ALL(acemaestro_uvvis,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-UV (1.2) O3 VMR ',['ACE-MAESTRO-VIS (3.13) (ppv)','ACE-MAESTRO-UV (1.2) (ppv)'])

# diffPlotter_profile_sections(acemaestro_uvvis,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-UV (1.2) O3 VMR Comparisons',['2004','2005','2006','2007','2008','2009','2010','2011'])

# diffPlotter_profile_sections(acemaestro_uvvis_all,'ACE-MAESTRO-VIS (3.13 and 1.2), ACE-MAESTRO-UV (1.2) O3 VMR Comparisons',['2004','2005','2006','2007','2008','2009','2010','2011'])

# acemaestro_uvvis = []
# for i in range(0,8,1):
#     year = 2004+i
#     pickle_in = open("acemaestro_visvis_"+str(year)+"_3.13_vmranalyzed_div.pickle","rb")
#     open_meas = pickle.load(pickle_in) #Open the pickle file
#     acemaestro_uvvis = acemaestro_uvvis + [ open_meas['pair'] ]
#     pickle_in.close()

# diffPlotter_all(acemaestro_uvvis,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-VIS (1.2) O3 VMR ',['ACE-MAESTRO-VIS (3.13) (ppv)','ACE-MAESTRO-VIS (1.2) (ppv)'])
# diffPlotter_sections(acemaestro_uvvis,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-VIS (1.2) O3 VMR ',['ACE-MAESTRO-VIS (3.13) (ppv)','ACE-MAESTRO-VIS (1.2) (ppv)'])
# vmrPlotter_sections(acemaestro_uvvis[0],acemaestro_uvvis[0].coincident_pairs,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-VIS (1.2) O3 VMR ',['ACE-MAESTRO-VIS (3.13) (ppv)','ACE-MAESTRO-VIS (1.2) (ppv)'],year)
# vmrPlotter_sections_ALL(acemaestro_uvvis,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-VIS (1.2) O3 VMR ',['ACE-MAESTRO-VIS (3.13) (ppv)','ACE-MAESTRO-VIS (1.2) (ppv)'])

# diffPlotter_profile_sections(acemaestro_uvvis,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-VIS (1.2) O3 VMR Comparisons',['2004','2005','2006','2007','2008','2009','2010','2011'])

acemaestro_uvvis = []
for i in range(0,8,1):
    year = 2004+i
    print(year)
    pickle_in = open("acemaestro_uvvis_"+str(year)+"_vmranalyzed_div.pickle","rb")
    open_meas = pickle.load(pickle_in) #Open the pickle file
    acemaestro_uvvis = acemaestro_uvvis + [ open_meas['pair'] ]
    pickle_in.close()

# diffPlotter_all(acemaestro_uvvis,'ACE-MAESTRO-UV (1.2) vs. ACE-MAESTRO-VIS (1.2) O3 VMR ',['ACE-MAESTRO-UV (1.2) (ppv)','ACE-MAESTRO-VIS (1.2) (ppv)'])
diffPlotter_sections(acemaestro_uvvis,'ACE-MAESTRO-UV (1.2) vs. ACE-MAESTRO-VIS (1.2) O3 VMR ',['ACE-MAESTRO-UV (1.2) (ppv)','ACE-MAESTRO-VIS (1.2) (ppv)'])
# vmrPlotter_sections(acemaestro_uvvis[0],acemaestro_uvvis[0].coincident_pairs,'ACE-MAESTRO-UV (1.2) vs. ACE-MAESTRO-VIS (1.2) O3 VMR ',['ACE-MAESTRO-UV (1.2) (ppv)','ACE-MAESTRO-VIS (1.2) (ppv)'],year)
# vmrPlotter_sections_ALL(acemaestro_uvvis,'ACE-MAESTRO-UV (1.2) vs. ACE-MAESTRO-VIS (1.2) O3 VMR ',['ACE-MAESTRO-UV (1.2) (ppv)','ACE-MAESTRO-VIS (1.2) (ppv)'])

# diffPlotter_profile_sections(acemaestro_uvvis,'ACE-MAESTRO-UV (1.2) vs. ACE-MAESTRO-VIS (1.2) O3 VMR Comparisons',['2004','2005','2006','2007','2008','2009','2010','2011'])

# pickle_in = open("acemaestro_uvvis_"+str(year)+"_vis_3.13_info_arrays.pickle","rb")
# open_meas = pickle.load(pickle_in) #Open the pickle file
# o3_vmr_vis = open_meas['o3_vmr']
# o3_vmr_error_vis = open_meas['o3_vmr_error']
# retrievals_vis = open_meas['retrievals']
# dates_vis = open_meas['dates']
# longitudes_vis = open_meas['longitudes']
# latitudes_vis = open_meas['latitudes']
# pickle_in.close()

# print('ACE-MAESTRO-UV & VIS')
# acemaestro_uvvis = vmrAnalysis_v313(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs)
# print('Done VMR Analysis')
# a = {'pair' : acemaestro_uvvis}
# pickle_out = open("acemaestro_uvvis_"+str(year)+"_3.13_vmranalyzed.pickle","wb")
# pickle.dump(a, pickle_out)
# pickle_out.close()

# acemaestro_uvvis = analyze_divisions_v313(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs)
# print('Done VMR Analysis')

# a = {'pair' : acemaestro_uvvis}
# pickle_out = open("acemaestro_uvvis_"+str(year)+"_3.13_vmranalyzed_div.pickle","wb")
# pickle.dump(a, pickle_out)
# pickle_out.close()

# vmrPlotter_sections(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-UV (1.2) O3 VMR ','ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-UV (1.2) O3 VMR Absolute Differences',['ACE-MAESTRO-VIS (3.13) (ppv)','ACE-MAESTRO-UV (1.2) (ppv)'],year)
# vmrPlotter(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-UV (1.2) O3 VMR ','ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-UV (1.2) O3 VMR Absolute Differences',['ACE-MAESTRO-VIS (3.13) (ppv)','ACE-MAESTRO-UV (1.2) (ppv)'],year)
# vmrColorbar(acemaestro_uvvis,acemaestro_uvvis.coincident_pairs,'ACE-MAESTRO-VIS (3.13) vs. ACE-MAESTRO-UV (1.2) O3 VMR',['ACE-MAESTRO-VIS (3.13) [ppv]','ACE-MAESTRO-UV (1.2) [ppv]'],folder,year)
# diff, diff_err, rel_diff, rel_diff_err = averageVMRComparePlotter_interp(acemaestro_uvvis,['ACE-MAESTRO-VIS (3.13)','ACE-MAESTRO-VIS (1.2)'],folder,year)  

# acemaestro_uvvis.o3_vmr_mean_absolute_diff_arr = diff
# acemaestro_uvvis.o3_vmr_mean_absolute_diff_err_arr = diff_err
# acemaestro_uvvis.o3_vmr_mean_relative_diff_arr = rel_diff
# acemaestro_uvvis.o3_vmr_mean_relative_diff_err_arr = rel_diff_err

# a = {'pair' : acemaestro_uvvis}
# pickle_out = open("acemaestro_visvis_"+str(year)+"_3.13_vmranalyzed.pickle","wb")
# pickle.dump(a, pickle_out)
# pickle_out.close()

# a = {'pair' : acemaestro_uvvis}
# pickle_out = open("acemaestro_visvis_"+str(year)+"_3.13_vmranalyzed_div.pickle","wb")
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
