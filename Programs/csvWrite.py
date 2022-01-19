# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 12:24:24 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: August 19 2020.
"""
# csvWrite
# This function takes a filename, the setting for the instrument comparisons, and a list of the pairs we
# are examining (in a pre-determined order). The comparison analyses for each instrument pair for atmospheric
# columns, number density, and VMR are written into and saved into a .txt file that can be read as a .csv
# (semi-colon delimited). The file is saved as 'filename' and given a header based on the coincidence criteria indicated
# by 'setting'.
# INPUT: 
# filename: str; the desired name of the .txt file.
# setting: int; corresponds to a coincidence criteria setting from CoincidentPairs.py.
#0 : within 12 hr and 500 km
#1 : within 12 hr, 500 km, same spv range ( <1.2 10^-4 s^01 or <1.6 10^-4 s^-1)
#2 : within 12 hr, 500 km, same spv range ( <1.2 10^-4 s^01 or <1.6 10^-4 s^-1), or somewhere in between
#3 : within 12 h4, 500 km, and within a margin (input) of sPV at selected layers.
# pairs: a list of 'pair' instruments, in a predetermined order (see function).
# OUTPUT: N/A.

import os

def csvWrite(filename,setting,pairs): 
   check_path = os.getcwd()  # Check if the File exists
   check_path = check_path + '\\' + filename
   if ((os.path.exists(check_path))==True):
      print('Write to Table.txt')
      f=open(filename,'w') # Open and write to the data file.
      f.write('ACE/OSIRIS Campaign, 2004-2009 \n')
      f.write('Coincidence Criteria: \n')
      if setting==0 or setting==1 or setting==2 or setting==3:
         f.write('Spatial Coincidence: 500 km \n')
         f.write('Temporal Coincidence: 12 h \n')
      if setting==0:
         f.write('Dynamical Criteria: NA')
      if setting==1:
         f.write('Dynamical Criteria: both measurements each <10^4*1.2 s^-1 (outside polar vortex) or >10^4*1.6 s^-1 (inside polar vortex) at select altitudes')
      if setting==2:
         f.write('Dynamical Criteria: both measurements each <10^4*1.2 s^-1 (outside polar vortex), >10^4*1.6 s^-1 (inside polar vortex), or in between at select altitudes')
      if setting==3:
         f.write('Dynamical Criteria: measurements of sPV at select altitudes have an sPV difference < 0.1 * 10^4 s^-1 \n')
    
      f.write('\n')
      f.write(' ; Years; Partial Column Range [km]; Number of Partial Column Coincidences; Partial Column Mean Absolute Error [DU]; Partial Column Mean Relative Error [%]; Partial Column RMSD [DU]; Partial Column R.^2; Number of Number Density Coincidences; Number Density Mean Absolute Error [molec cm.^-3]; Number Density Mean Relative Error [%]; Number Density RMSD [molec cm.^-3]; Number Density R.^2; Number of VMR Coincidences; VMR Mean Absolute Error [ppv]; VMR Mean Relative Error [%]; VMR RMSD [ppv]; VMR R.^2;\n')
      for i in range(0,len(pairs),1): # Cycle through all pairs inputted
         if i==0:
            f.write('ACE-MAESTRO-UV vs ACE-MAESTRO-VIS;')
            
         f.write(pairs[i].years)
         f.write(';')
         f.write(str(pairs[i].pc_range))
         f.write(';')
         f.write(str(pairs[i].N))
         f.write(';')
         f.write(str('%.2f' % pairs[i].mean_absolute_diff))
         f.write(str(' ± '))
         f.write(str('%.2f' % pairs[i].mean_absolute_diff_err))
         f.write(';')
         f.write(str('%.2f' % pairs[i].mean_relative_diff))
         f.write(str(' ± '))
         f.write(str('%.2f' % pairs[i].mean_relative_diff_err))
         f.write(';')
         f.write(str('%.2f' % pairs[i].RMSD))
         f.write(';')
         f.write(str('%.3f' % (pairs[i].R2)))
         f.write(';')
         
         f.write(str(pairs[i].o3_nd_N))
         f.write(';')
         f.write(str("{:.2e}".format(pairs[i].o3_nd_mean_absolute_diff)))
         f.write(str(' ± '))
         f.write(str("{:.2e}".format(pairs[i].o3_nd_mean_absolute_diff_err)))
         f.write(';')
         f.write(str('%.2f' % pairs[i].o3_nd_mean_relative_diff))
         f.write(str(' ± '))
         f.write(str('%.2f' % pairs[i].o3_nd_mean_relative_diff_err))
         f.write(';')
         f.write(str("{:.2e}".format(pairs[i].o3_nd_RMSD)))
         f.write(';')
         f.write(str('%.3f' % (pairs[i].o3_nd_R2)))
         f.write(';')
         
         f.write(str(pairs[i].o3_vmr_N))
         f.write(';')
         f.write(str("{:.2e}".format(pairs[i].o3_vmr_mean_absolute_diff)))
         f.write(str(' ± '))
         f.write(str("{:.2e}".format(pairs[i].o3_vmr_mean_absolute_diff_err)))
         f.write(';')
         f.write(str('%.2f' % pairs[i].o3_vmr_mean_relative_diff))
         f.write(str(' ± '))
         f.write(str('%.2f' % pairs[i].o3_vmr_mean_relative_diff_err))
         f.write(';')
         f.write(str("{:.2e}".format(pairs[i].o3_vmr_RMSD)))
         f.write(';')
         f.write(str('%.3f' % (pairs[i].o3_vmr_R2)))
         
         f.write('; \n')

      f.write('\n')
      f.close()
    
   return
      
      