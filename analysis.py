# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import analysis_parallel_settings_working as s
import analysis_functions_working as af

"""
todo:
1. dataframe erstellen die alle variablen und die werte dieser beinhaltet. check
2. run_simulation für jeden inhalt dieses dataframes
3. variable raussuchen bei der die differenz zu den empirical data am geringsten ist
4. den wert dieser variable speichern und den alten wert mit diesen überschreiben
5. weiter bei schritt 2 aber mit neuem wert der variable  

"""

# kann in eine initierungs function
#   -   -   - create dataframe of all variables with steps -   -   -
#read excel with to be analysed parameters
parameter = pd.read_excel('Parameter Liste.xls')
#create base form of parameter list  
parameter_list = pd.DataFrame(columns = [parameter.var_name], index = np.arange(s.grid_resolution))
#fill parameter list with steps
for i in range (0,parameter.shape[0]):
    start_val = round(parameter.iloc[i,2]-parameter.iloc[i,2]*s.parameter_divergence,4)
    end_val = round(parameter.iloc[i,2]+parameter.iloc[i,2]*s.parameter_divergence,4)
    delta = (end_val-start_val)/s.grid_resolution
    values = np.arange(start_val, end_val+0.00001, delta)
    for j in range (0,s.grid_resolution):
        parameter_list.iloc[j,i] = values[j]

#   -   -   - run_simulation for every entry of parameter_list -   -   -
a = 0
for i in range(0,parameter_list.shape[1]):
    for j in range(0,s.grid_resolution):
        #so kann jeder eintrag der parameter_list durchgegangen werden


"""
var_name ="dcfsn"
var_value = 5
results = af.run_simulation(parameter_list.size, var_name = var_value) #wie würde das funktionieren
"""