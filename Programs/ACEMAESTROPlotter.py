# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 10:32:42 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: Feb 18 2021
"""
# This program will produce data structures for ACE MAESTRO (in .asc files) and save them in a list.
# This file analyzes data and will do this for every .asc file in the current
# working directory. The functions read off -999 as an error input.

# INPUT: N/A
# OUTPUT: ACEMAESTROPlotter outputs a list of 'measurement' classes. Each measurement class represents one 
# measurement (one data file in the current working directory) and contains all relevant information for that measurement.
# DMPs (Derived Meteorological Products) and location text files are also searched for and opened for each measurement (DMP and location text files must be in current working directory).

import numpy
from numpy import sqrt
from measurement import *
# from DMPreader import *
from scipy import interpolate
from round_oneandhalf import * 
import os
import datetime

def ACEMAESTROPlotter(sunset, sunrise):
   files = [f for f in os.listdir('.') if os.path.isfile(f)] # Create list of all files in current working directory.
   acemaestro_uv, acemaestro_vis = [], []
   for f in files:
      test = f[len(f)-4:len(f)] # Take last four chars to check file extension.
      if ((test==".dat")) and ((f[0:2]=='ss') or (f[0:2]=='sr')):  
      # If the file has a .dat extension and a sunrise or sunset ID: 
         filenamedat = f
         acemaestro = extractinfo_acemaestro(filenamedat,sunset, sunrise) # Function to produce and save an object for each .csv file.
         if type(acemaestro)!=bool:
             if acemaestro.uvvis == 0: # UV measurement
                 acemaestro_uv = acemaestro_uv  + [acemaestro]
             if acemaestro.uvvis == 1: # VIS measurement
                 acemaestro_vis = acemaestro_vis  + [acemaestro]
   return acemaestro_uv, acemaestro_vis

def extractinfo_acemaestro(filenamedat,sunset, sunrise):
    
   f=open(filenamedat,'r') # Open and read the data file.
   _lines = f.readlines()
   print(filenamedat)
   acemaestro = measurement()
   acemaestro.filename = filenamedat
   # Extract occultation ID from file title.
   occ_ID=''
   for i in range(0,len(filenamedat),1):
      if filenamedat[i]!='_':
          occ_ID= occ_ID + filenamedat[i]
      else:
          if filenamedat[i+1]=='u': # Add label for if the measurement is from the UV or visible spectrum by reading filename.
              print('UV')
              acemaestro.uvvis = 0
          if filenamedat[i+1]=='v':
             print('VIS')
             acemaestro.uvvis = 1
          break
   acemaestro.occultation_ID = occ_ID 
   # Set up column variables
   o3_vmr = []
   o3_vmr_error = []
   altitude = []
   altitude_lowres = []
   temperature = []
   pressure = []
   air_density = []
   retrievals = []
   columns = []
   lines=[] # Remove end of line symbol, \n.
   for line in _lines:
        x = line.strip().split(',')
        lines.append(x) # Each element in lines is a row from the csv file. 
        columns = columns + [line.split()]
   # First, extract information from Header Lines.    
        
   scanHeader = True # Scan for start of dataset.
   start=0
   while scanHeader == True:  
       if (columns[start]==['Index', 'Height', 'Ozone', 'Error', 'Retrieved?']):
          scanHeader=False
          start+=2
       else:
           start+=1
     
   # Extract O3_VMR and Altitude data from asc files.
   for i in range(start,len(columns),1): 
      currline = columns[i]
      curraltitude = currline[1]
      curro3vmr = currline[2]
      curro3vmrerror = currline[3]
      retrieved = currline[4] # o: no, 1: yes

      # Now that row is over, add the data points to the arrays.
      if (curraltitude=="") or (curro3vmr=="") or (curro3vmrerror==""):  #There was an error and no altitude/temp/pressure data was collected for this row.
         skip = True # Skip the reading for this row and move on.
      else:      # Received a float for all values
         if ((curraltitude=="-1.#JE+000") or (curro3vmr=="-1.#JE+000") or (curro3vmrerror=="-1.#JE+000")): # Received an error message.
            altitude = [numpy.NaN] + altitude   # Add entry to altitude array.
            o3_vmr = [numpy.NaN] + o3_vmr
            o3_vmr_error = [numpy.NaN] + o3_vmr_error   # Add entry to VMR_ERR array.
            retrievals = [int(retrieved)] + retrievals 
         else:
            curraltitude = float(currline[1])
            curro3vmr = float(currline[2])
            curro3vmrerror = float(currline[3])
            retrieved = int(currline[4]) # o: no, 1: yes
            if curraltitude==-999 or curraltitude==-888: # Check current altitude value.
               altitude = [numpy.NaN] + altitude   # Add entry to altitude array.                
            else:
               altitude = [curraltitude] +altitude   # Add entry to altitude array.
            if curro3vmr==-999 or curro3vmr==-888: # Check current O3 VMR value.
               o3_vmr = [numpy.NaN] + o3_vmr   # Add entry to O3 VMR array.                
            else:
               o3_vmr = [curro3vmr] + o3_vmr   # Add entry to O3 VMR array.
            if curro3vmrerror==-999 or curro3vmrerror==-888: # Check current O3 VMR error value.
               o3_vmr_error = [numpy.NaN] + o3_vmr_error   # Add entry to O3 VMR error array.                
            else:
               o3_vmr_error = [float(curro3vmrerror)*curro3vmr] + o3_vmr_error   # Add entry to O3 VMR error array.
               # Recall that this is the fractional error. 
            retrievals = [int(retrieved)] + retrievals 
      if (columns[i+1]==[]): # Check if we are done cycling through data
         break # Set to being finished
   # Once out of While loop, cycle into next row of file.   
   if (o3_vmr_error!=[]):
      acemaestro.o3_vmr_error = o3_vmr_error
   else:
      acemaestro.o3_vmr_error = numpy.NaN
   if (o3_vmr!=[]):
      acemaestro.o3_vmr = o3_vmr
   else:
      acemaestro.o3_vmr = numpy.NaN
   if (altitude!=[]):
      acemaestro.altitude = altitude
   else:
      acemaestro.altitude = numpy.NaN
   acemaestro.is_retrieved = retrievals
   f.close() # Close the file now that we have all the needed data.
   

    # Interpolate O3 VMR onto a common altitude grid for comparisons with other instruments.
    # Use the interpolation function from scipy
   if (type(acemaestro.altitude)==list) and (max(acemaestro.altitude)>=0.5) and (type(acemaestro.o3_vmr)==list):      
      x = acemaestro.altitude
      max_x = 100.5 # Take the maximum of the altitudes and round it down to nearest number on the ACE grid.
      min_x = 0 # Take the minimum of the altitudes and round it up to nearest number on the ACE grid.
      y = acemaestro.o3_vmr 
      f = interpolate.interp1d(x, y, kind = 'linear') # Interpolate with a linear approximation.
      # X range for the interpolation function (here, altitude).
      x_f = numpy.arange(min_x, max_x, 0.5)
      
      y_f = f(x_f)   # Use interpolation function returned by `interp1d`.
      acemaestro.common_o3_vmr = list( y_f )
      acemaestro.common_altitude = list(x_f)
      # Repeat interpolation for O3 VMR error.
      y = acemaestro.o3_vmr_error
      f = interpolate.interp1d(x, y, kind = 'linear') # Interpolate with a linear approximation.
      # X range for the interpolation function (here, altitude).
      x_f = numpy.arange(min_x, max_x, 0.5)
      y_f = f(x_f)   # Use interpolation function returned by `interp1d`.
      acemaestro.common_o3_vmr_error = list( y_f )  
      # Repeat interpolation for retrievals.
      y = acemaestro.is_retrieved
      print(len(x),len(y))
      f = interpolate.interp1d(x, y, kind = 'linear') # Interpolate with a linear approximation.
      # X range for the interpolation function (here, altitude).
      x_f = numpy.arange(min_x, max_x, 0.5)
      y_f = f(x_f)   # Use interpolation function returned by `interp1d`.
      y_f = list( y_f )
      for i in range(0,len(y_f),1):
          if type(y_f[i])==int or type(y_f[i])==float:
              y_f[i] = int(y_f[i])
          else:
              y_f[i] = 0
      acemaestro.common_is_retrieved = list( y_f )  

   # Read sunset or sunrise table 
   if filenamedat[0:2]=='ss':
       # ss=open('SunsetTable.txt','r') # Open and read the data file.
       # _lines = ss.readlines()
       _lines = sunset
       length = len(occ_ID)
       for i in _lines:
           if i[0:length+1]==occ_ID+" ":
               print(i)
               acemaestro.YMDHMIS = [ int(i[length+1:length+5]), int(i[length+6:length+8]), 
                                     int(i[length+9:length+11]), int(i[length+12:length+14]), 
                                    int(i[length+15:length+17]), int(i[length+18:length+20]) ]
               YMDHMIS = acemaestro.YMDHMIS
               acemaestro.date = str( "%.4d" % acemaestro.YMDHMIS[0])+'-'+str( "%.2d" % acemaestro.YMDHMIS[1])+'-'+str( "%.2d" % acemaestro.YMDHMIS[2])
               acemaestro.datetime = datetime.datetime(YMDHMIS[0], YMDHMIS[1], YMDHMIS[2], YMDHMIS[3], YMDHMIS[4], YMDHMIS[5])
               acemaestro.year = str(YMDHMIS[0])
               acemaestro.time = str( "%.2d" % acemaestro.YMDHMIS[3])+':'+str( "%.2d" % acemaestro.YMDHMIS[4])+':'+str( "%.2d" % acemaestro.YMDHMIS[5])

               k = length+20+4
               word = ''
               while k<len(i):
                   if i[k]==' ':
                       k+=1
                       break
                   else:
                       word = word + i[k]
                       k+=1
               acemaestro.latitude = float(word)
               word = ''
               while k<len(i):
                   if i[k]==' ':
                       k+=1
                       break
                   else:
                       word = word + i[k]
                       k+=1
               acemaestro.longitude = float(word)
               word = ''
               while k<len(i):
                   if i[k]==' ':
                       k+=1
                       break
                   else:
                       word = word + i[k]
                       k+=1
               acemaestro.beta_angle = float(word)
               print(acemaestro.YMDHMIS)
   if filenamedat[0:2]=='sr':
       # sr=open('SunriseTable.txt','r') # Open and read the data file.
       # _lines = sr.readlines()  
       _lines = sunrise         
       length = len(occ_ID)
       for i in _lines:
           if i[0:length+1]==occ_ID+" ":
               print(i)
               acemaestro.YMDHMIS = [ int(i[length+1:length+5]), int(i[length+6:length+8]), 
                                     int(i[length+9:length+11]), int(i[length+12:length+14]), 
                                    int(i[length+15:length+17]), int(i[length+18:length+20]) ]
               YMDHMIS = acemaestro.YMDHMIS
               acemaestro.date = str( "%.4d" % acemaestro.YMDHMIS[0])+'-'+str( "%.2d" % acemaestro.YMDHMIS[1])+'-'+str( "%.2d" % acemaestro.YMDHMIS[2])
               acemaestro.datetime = datetime.datetime(YMDHMIS[0], YMDHMIS[1], YMDHMIS[2], YMDHMIS[3], YMDHMIS[4], YMDHMIS[5])
               acemaestro.year = str(YMDHMIS[0])
               acemaestro.time = str( "%.2d" % acemaestro.YMDHMIS[3])+':'+str( "%.2d" % acemaestro.YMDHMIS[4])+':'+str( "%.2d" % acemaestro.YMDHMIS[5])
               k = length+20+4
               word = ''
               while k<len(i):
                   if i[k]==' ':
                       k+=1
                       break
                   else:
                       word = word + i[k]
                       k+=1
               acemaestro.latitude = float(word)
               word = ''
               while k<len(i):
                   if i[k]==' ':
                       k+=1
                       break
                   else:
                       word = word + i[k]
                       k+=1
               acemaestro.longitude = float(word)
               word = ''
               while k<len(i):
                   if i[k]==' ':
                       k+=1
                       break
                   else:
                       word = word + i[k]
                       k+=1
               acemaestro.beta_angle = float(word)
               print(acemaestro.YMDHMIS)
   n=311
   if type(acemaestro.datetime)!=datetime.datetime or type(acemaestro.common_o3_vmr)!=list or type(acemaestro.common_o3_vmr_error)!=list or len(acemaestro.o3_vmr)!=311 or len(acemaestro.o3_vmr)!=311 or len(acemaestro.is_retrieved)!=311 or type(acemaestro.longitude)!=float or type(acemaestro.latitude)!=float:
       print(acemaestro.occultation_ID)
       return False
   else:
      return acemaestro

