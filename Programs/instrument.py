# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 13:30:06 2020

@author: Victoria Spada
Contact: victoria.spada@mail.utoronto.ca
Last edited: August 14 2020.
"""
# This file contains the definition of a class: 'instrument'.
# This object encapsulates information for a particular instrument (ie, ACE-FTS)
# and includes properties for all measurements, the years included, and average values.

# There are no inputs required to create the instrument object.

class instrument():
    # Instrument object with data as properties  
    def __init__(self):
        self.name =  '' # String  indicating the name of the instrument.
        self.years = [] # A list of integers. Each element is a year for which measurements were taken.
        self.measurements = [] # A list of 'measurement' class objects, each corresponsing to a measurement made by the instrument.
        self.measurements_by_year = [] 
        self.measurements_by_year_and_month = []
        
        self.average_o3_number_density_by_year = [] # List of lists. Each list is an array describing the average o3 number density recorded that year.
        self.average_o3_number_density_error_by_year = [] # List of lists. Each list is an array describing the average o3 number density recorded that year.
        
    def dispYears(self):  # Display years included in the object.
        print('Years Included: ',self.years,'\n')
        return
    def dispInstrumentName(self):  # Print the name of the instrument.
        print('Intrument: ',self.name,'\n')
        return