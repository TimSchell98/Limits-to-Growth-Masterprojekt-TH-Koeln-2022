#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 15:22:59 2022

@author: rubenwillamowski
"""
# - - - - Imports - - - - - -
import multiprocessing as mp
import numpy as np
from numpy import diff
import pandas as pd
import analysis_functions as af
import analysis_parallel_settings as s
import matplotlib.pyplot as plt
import time
import sys

startTime = time.time()
# - - -  World 3 import and Version Switching

if s.use_update == True:
    sys.path.append('..')
    from PyWorld3_Update.pyworld3 import World3
if s.use_update == False:
    from pyworld3 import World3
    # Wenn old funktioniert:
    #sys.path.append('..') 
    #from PyWorld3_Old.pyworld3 import World3
    
# - - - - - - Function definitions - -

i=1

#run simulation
world3 = World3(dt=s.sim_time_step, year_max=s.year_max)
world3.init_world3_constants()
world3.init_world3_variables()
world3.set_world3_table_functions()
world3.set_world3_delay_functions()
world3.run_world3(fast=False)



#gather simulation data
simulation_data = pd.DataFrame()
simulation_data['POP_{}'.format(i)] = world3.pop
simulation_data['AL_{}'.format(i)] = world3.al
simulation_data['CDR_{}'.format(i)] = world3.cdr
simulation_data['CBR_{}'.format(i)] = world3.cbr
simulation_data['FPC_{}'.format(i)] = world3.fpc
simulation_data['POLC_{}'.format(i)] = world3.ppol
simulation_data['PPOL_dt_{}'.format(i)] = np.append((diff(world3.ppol)/s.sim_time_step),np.nan) #Pollution groth rate / derivation 
simulation_data['SOPC_dt_{}'.format(i)] = np.append((diff(world3.sopc)/s.sim_time_step),np.nan) #Servvice output pc groth rate / derivation
#simulation_data['IO_{}'.format(i)] = world3.io
simulation_data['IO_dt_{}'.format(i)] = np.append((diff(world3.io)/s.sim_time_step),np.nan) #Industrial Output groth rate / derivation
simulation_data['NRUR_{}'.format(i)] = world3.nrur


simulation_data_help = pd.DataFrame()
for attribute_name in s.empirical_settings.index:
    if  s.empirical_settings.loc[attribute_name,'type']=='pyworld':
        simulation_data_help['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] = getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name'])
    elif s.empirical_settings.loc[attribute_name,'type']=='derivation':    
        simulation_data_help['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] = np.append((diff(getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']))/s.sim_time_step),np.nan) 
    elif s.empirical_settings.loc[attribute_name,'type']=='proportion':
        proportion_help1 = np.append(getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']),np.NaN)
        proportion_help2 = np.append(np.NaN,getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']))
        simulation_data_help['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] =  ((proportion_help1-proportion_help2)/proportion_help1)[:-1]
   


print (s.empirical_settings['pyworld_name_complete']+"_{}")

"""WIEDER LÖSCHEN und als funktion wenn world3.VAR_NAME 
+ ohne hilfsvariable sondern mit sim_data['...', i-1,i] - (so ungefähr) """
df_help1 = pd.DataFrame()
df_help1['NRURP_{}'.format(i)]= np.append(world3.nrur,np.NaN)
df_help1['PPOL_dtP_{}'.format(i)]= np.append(world3.ppol,np.NaN)
df_help1['SOPCP_{}'.format(i)]= np.append(world3.sopc,np.NaN)
df_help1['IOP_{}'.format(i)]= np.append(world3.io,np.NaN)

df_help2= pd.DataFrame()
df_help2['NRURP_{}'.format(i)]= np.append(np.NaN,world3.nrur)
df_help2['PPOL_dtP_{}'.format(i)]= np.append(np.NaN,world3.ppol)
df_help2['SOPCP_{}'.format(i)]= np.append(np.NaN,world3.sopc)
df_help2['IOP_{}'.format(i)]= np.append(np.NaN,world3.io)

df_proportion = pd.DataFrame()
df_proportion['NRURP_{}'.format(i)] = (df_help1['NRURP_{}'.format(i)]-df_help2['NRURP_{}'.format(i)])/df_help1['NRURP_{}'.format(i)]
df_proportion['PPOL_dtP_{}'.format(i)] = (df_help1['PPOL_dtP_{}'.format(i)]-df_help2['PPOL_dtP_{}'.format(i)])/df_help1['PPOL_dtP_{}'.format(i)]
df_proportion['SOPCP_{}'.format(i)] = (df_help1['SOPCP_{}'.format(i)]-df_help2['SOPCP_{}'.format(i)])/df_help1['SOPCP_{}'.format(i)]
df_proportion['IOP_{}'.format(i)] = (df_help1['IOP_{}'.format(i)]-df_help2['IOP_{}'.format(i)])/df_help1['IOP_{}'.format(i)]

simulation_data = pd.concat([simulation_data, df_proportion[:-1]], axis=1)




"""l=empirical_settings.index[empirical_settings['proportion'] == True].tolist()
 
for i in l:
    var_name=empirical_settings.loc[i,'pyworld_name']
    i_help = world3.var_name
    """