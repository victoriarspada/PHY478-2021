# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 16:22:07 2020

@author: Victoria Spada
contact: victoria.spada@mail.utoronto.ca
Last edited: August 11 2020.
"""
# round_oneandhalf:
# INPUT: type float.
# OUTPUT: type float.
# Return the value in the following array that is the closest to the input number while being lower than the input:
# [ 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, ...]

# round_down_oneandhalf:
# INPUT: type float.
# OUTPUT: type float.
# Return the value in the following array that is the closest to the input number while being higher than the input:
# [ 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, ...]

import math

def round_oneandhalf(number):
        if number < 0.5:
            return 0.5
        else:
            return ((math.floor((number-0.5)))+0.5)

def round_down_oneandhalf(number):
        return  ((math.ceil((number-0.5)))+0.5)

 