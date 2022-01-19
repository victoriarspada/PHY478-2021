# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:39:08 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: August 13 2020.
"""
# distance:
# This function calculates, in kilometres, the distance between two points on a
# spherical surface (Earth), inputted as the latitude and longitude of each point.
# The Haversine function is used as an intermediate function.

# INPUT:
# start: [latitude, longitude] is a float array of the start point.
# end: [latitude, longitude] is a float array of the endpoint.

# OUTPUT:
# d: output distance between the two input points: start_p and end_p.

from numpy import *
 
def distance(start_p,end_p):
   r = 6371 #Radius of the Earth [km].
   # Extract latitude and longitude; convert all to radians.
   lat1 = start_p[0]*pi/180
   long1 = start_p[1]*pi/180
   lat2 = end_p[0]*pi/180
   long2 = end_p[1]*pi/180

   d = 2*r*arcsin( sqrt( haversine(lat2-lat1) + cos(lat1)*cos(lat2)*haversine(long2-long1) ) )
   return d

def haversine(theta):
# This function is the haversine function: hav(theta) = sin^2(theta/2) = (1-cos(theta))/2
# Input: theta, in radians.
   ans = (sin(theta/2))**2
   return ans

print(distance([80,-80],[80,-86.4]))
