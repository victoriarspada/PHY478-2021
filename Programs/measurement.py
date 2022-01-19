# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 10:04:42 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: August 14 2020.
"""
# This file defines a 'measurement' class with data as properties. 
# Generally, each trace gas measurement has its own data file (ie, type .asc, .csv, .dat, etc)
# This object can contain/collect all the information stored in a data file, such as:
# date
# time
# longitude/latitude
# pressure/temperature/volume mixing ratios/number density/ air density as functions of altitude
# measured partial/total columns

# Some attributes are instrument specific, such as:
# UVVIS: This quanitity specifies, for ACE-MAESTRO measurements, whether the spectral analysis was done in 
# the UV or VISIBLE range, but remains blank for other instrument measurements. 
# occultation_ID: Since each measurement made by ACE-FTS & ACE-MAESTRO is assigned an occultation ID, this name
# is stored to easily identify the coincidences between ACE-FTS & ACE-MAESTRO, while this 'ID' value is left blank
# for all other instruments.

# O3 number densities and O3 VMR for an interpolated grid (the grid that ACE-FTS & ACE-MAESTRO measurements lie on) are also 
# and attribute for this class. 

import numpy

class measurement:
   
    def __init__(self):
        
        self.filename = '' # Char array (ie, 'EU200101.CSV')     
        self.occultation_ID = '' # String, for ACE-MAESTRO, ACE-FTS.
        self.uvvis = numpy.NaN # Int for ACE-MAESTRO spectrum specification ( 0 - UV, 1 - VIS, -1 - INFRARED)

        self.DOY = numpy.NaN # Day of the year of measurement.
        self.date = '' # String, (ie, '2020-01-01')
        self.time = '' # String, (ie, '12:30:04')
        self.year = '' # String, (ie, '2020')
        
        self.datetime = numpy.NaN # datetime class, used for determining time differences.
        self.YMDHMIS = [0,0,0,0,0,0] # Year, Month, Day, Hour, Minute, Second.
        
        self.elevation = numpy.NaN # Float [km]
        self.longitude = numpy.NaN # Floats [degrees]
        self.latitude = numpy.NaN # Floats [degrees]
        self.beta_angle = numpy.NaN # Floats [degrees]
        
        self.temperature = numpy.NaN # Float Array, [Degrees Celsius]
        self.temperature_error = numpy.NaN # Float array, [Degrees Celsius]
        
        self.pressure = numpy.NaN # Float Array, [mPa]
        self.o3_partial_pressure = numpy.NaN # Float Array, [mPa]
        
        self.altitude = numpy.NaN # Float array, [km]

        # Values read off of DMPs (Derived Meteorological Products)        
        self.sPV = numpy.NaN #  Scaled Potential Vorticity Float Array, Altitude [km] Float Array [[10^-4 s^-1], [km]].
        self.sPV_layers = numpy.NaN # [[],[],[]] # [ [sPV], [0:Outside, 1:Inside, numpy.NaN:Grey areas], [altitude] ]
    
        # Numbers interpolated onto a common grid.
        # Altitude grid is set to match the grid of ACE-FTS & ACE-MAESTRO measurements: [0.5, 1.5, 2.5, 3.5, ...]
        self.is_retrieved = numpy.NaN 
        self.common_altitude = numpy.NaN  # Float array, [km]
        self.common_o3_vmr = numpy.NaN # Float array [ppv]
        self.common_o3_vmr_error = numpy.NaN # Float array, [ppv]
        self.common_o3_number_density = numpy.NaN # Float array, [molec cm^-3]
        self.common_o3_number_density_error = numpy.NaN # Float array, [molec cm^-3]
        self.common_sPV = numpy.NaN # Float array, [10^4  s^-1]
        self.common_sPV_altitude = numpy.NaN       

        # OZONE related attributes.
        self.o3_number_density = numpy.NaN # Float array, [molecules/cm^3]
        self.o3_number_density_error = numpy.NaN # Float Array, [molecules/cm^3]
        self.air_density = numpy.NaN # Float array, [molecules/cm^3]       
        self.o3_vmr = numpy.NaN # Float array, [ppv]
        self.o3_vmr_error = numpy.NaN # Float array, [ppv]

        self.o3_total_column = numpy.NaN # Float, [DU]
        self.o3_total_column_error = numpy.NaN # Used for PEARL/UT-GBS, as well as ACE-FTS and ACE-MAESTRO (using a-priori numbers to fill in missing spots)

        self.o3_partial_column = numpy.NaN # Float, [DU]
        self.o3_partial_column_error = numpy.NaN  # Float, [DU]

        self.o3_partial_column_1452 = numpy.NaN # Float, [DU], for comparison with other instrument
        self.o3_partial_column_1452_error = numpy.NaN # Float, [DU], for comparison with other instrument

        self.o3_partial_column_1030 = numpy.NaN # Float, [DU], for comparison with other instrument
        self.o3_partial_column_1030_error = numpy.NaN # Float, [DU], for comparison with other instrument

        self.o3_partial_column_range = [numpy.NaN, numpy.NaN] # 1X2 Double, Floats, for comparison with other instrument

        self.o3_column_plus_coin_sonde = numpy.NaN # For ACE-MAESTRO & ACE-FTS measurements, so the COINCIDENT ozonesnde fills in the lower altitudes where there is no retrieval
        self.o3_column_plus_coin_sonde_error = numpy.NaN # Float, [DU]
        
        self.o3_column_plus_sonde = numpy.NaN # For ACE-MAESTRO & ACE-FTS measurements, so the CLOSEST ozonesnde fills in the lower altitudes where there is no retrieval
        self.o3_column_plus_sonde_error = numpy.NaN # Float, [DU]



