#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 14:47:08 2022

@author: rubenwillamowski, 
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyworld3 import World3
from pyworld3.utils import plot_world_variables

# Needed Vars
d_value_list = []                                       
d_roc_list   = []
nrmsd_list   = []  


"Functions"

def compare(pyworld_data, real_data, sensivity_variable):
    """calculate Rate of Change, NRMSD (Branderhorst 2020)
    """
    
    n = len(pyworld_data)
    
    for year_n in np.arange(0,n,5): 
       #d_value
        d_value      = (pyworld_data[year_n-1]-real_data[year_n-1])/real_data[year_n-1]
        d_value_list.append(d_value)
        d_value_sum = sum(d_value_list)
        
        #roc
        d_roc   = (((pyworld_data[year_n-1]-pyworld_data[year_n-6])-(real_data[year_n-1]-real_data[year_n-6]))
               /(real_data[year_n-1]-real_data[year_n-6]))
        d_roc_list.append(d_roc)
        d_roc_sum = sum(d_roc_list)
        
        #nrmsd
        nrmsd   = (((((pyworld_data[year_n-1]-real_data[year_n-1])**2)/6))**(1/2))/(real_data[year_n-1]/6)    
        nrmsd_list.append(nrmsd)
        nrmsd_sum = sum(nrmsd_list)
                 
    results_dvalue = pd.DataFrame(data = d_value_sum, index = [sensivity_variable], 
                     columns = ['d value'])
    results_droc   = pd.DataFrame(data = d_roc_sum, index = [sensivity_variable], 
                     columns = ['d ROC'])
    results_nrmsd  = pd.DataFrame(data = nrmsd_sum, index = [sensivity_variable], 
                     columns = ['NRMSD'])
    
    results = pd.concat([results_dvalue, results_droc, results_nrmsd], 
                        axis = 1)
    
    return results


"Run Py-World"

params = {'lines.linewidth': '3'}
plt.rcParams.update(params)

world3 = World3(dt = 1)                 # set time step = 1 [year] 
world3.init_world3_constants()
world3.init_world3_variables()
world3.set_world3_table_functions()
world3.set_world3_delay_functions()
world3.run_world3(fast=False)

plot_world_variables(world3.time,
                     [world3.nrfr, world3.iopc, world3.fpc, world3.pop,
                      world3.ppolx],
                     ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                     [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                     figsize=(7, 5),
                     title="World3 standard run")


"Data decleration"

## Define Pyworld Data 
#population
pop_py= world3.pop[75:122]                          # Data from 1970 - 2021

## Import Observed Data
# Population
pop_data_big = pd.read_csv('Data_population.csv')
pop_data = pop_data_big.iloc[0:1, 19:]              # Data from 1970 - 2021
pop_data = np.transpose(pop_data.values.tolist())

# Food per capita


"Evaluation"
#compare(pyworld_data, real_data, sensivity_variable):
res_comparison = compare(pop_py, pop_data, "population")


"Print Results and plot Data"
print (res_comparison)

plot_world_variables(world3.time[75:122],
                     [pop_py, pop_data],
                     ["pop_py", "pop_data"],
                     [[0, 16e9], [0, 16e9]],
                     figsize=(7, 5),
                     title="World3 standard run compare pop")



"TODO"
#functions
    #pyworld data time 
    #import observed data
    #print standard + compare
    ## function+loop set parameter, run, compare (all vars)
#for-loop function compare














