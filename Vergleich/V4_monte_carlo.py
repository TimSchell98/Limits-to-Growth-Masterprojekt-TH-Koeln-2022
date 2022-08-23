#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:53:23 2022

@author: rubenwillamowski
"""

## Import packages
import matplotlib.pyplot as plt
import numpy as np 
import random
import pandas as pd


## creating functions

def rolling_dice():
    diece_1 = random.randint(1, 6)
    diece_2 = random.randint(1, 6)
    dice_12 = diece_1 + diece_2
    return dice_12

def count_dice (pips_number):
    res_table = pips.count(pips_number)
    return res_table


## Simulation
#Inputs
n = 100000             # number of rolls  
pips = []           # list for dice results
number_pips = []    # amount of pips diced 
dice_combinations = np.arange(2,13)

# loop 
for i in range(n):
    pips.append(rolling_dice())
   
# count results
for possible_pips in dice_combinations:
    number_pips.append(count_dice(possible_pips))

#make dataframe wioth results
results = {"possible pips": dice_combinations, "number": number_pips}   
df_res  = pd.DataFrame(data = results)


## plot
df_res.plot.bar(x = "possible pips", y = "number", rot = 70, title = 'montecarlo')
plt.show(block=True);

#print avarage
avarage = (dice_combinations * number_pips).sum()/n
print ('The avarage with', n, 'runs is:', avarage)
print (df_res)
