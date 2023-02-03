import importlib.util

MODULE_PATH = "C:/Users/Tim Schell/Documents/GitHub/pyworld3/pyworld3"
MODULE_NAME = "pyworld3"


#spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
#modulevar = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(modulevar)

import matplotlib.pyplot as plt
import numpy as np
from xlwt import Workbook
from pyworld3 import World3
from pyworld3.utils import plot_world_variables
import pandas as pd
from math import isnan


import time
startTime = time.time()

"Analyse Einstelungen"
#berechnen der eingangsparameter "Spruenge"

#Einteilen des Simulationsrasters
sim_anzahl = 11
start_val = 3
end_val = 5
delta = (end_val-start_val)/(sim_anzahl-1)
#Simulation
sim_time_step = 1 #pro Jahr in Simulation
year_max = 2021    
year_max1 = year_max +1   
year_min = 1900
period  = year_max1 - year_min


"Data - measured"
## Import Observed Data
# Population
pop_data_big = pd.read_csv('Data_population.csv')
pop_data = pop_data_big.iloc[0:1, 4:]              # Data from 1970 - 2021
pop_data = np.transpose(pop_data.values.tolist())
#arable Land
al_data_big = pd.read_csv('Data_arable_land1.csv')
al_data = al_data_big.iloc[270]        # Data from 1961 - 2018
al_data = al_data.str.split(";", expand = True)
al_data = al_data.iloc[0:1,5:63]
al_data = np.transpose(al_data.values.tolist())
#create one DataFrame
year_data = np.arange(year_min,year_max1)
measured_data = np.zeros((period, 3))
measured_data[:,0] = year_data
measured_data[60:122,1:2] = pop_data
measured_data[61:119,2:3] = al_data

measured_data = pd.DataFrame(data = measured_data, columns = ['year', 'population', 'arable_land']).replace(0, np.nan)


"Functions"
def calculate_differences(pyworld_data, real_data, sensivity_variable):
    """calculate Rate of Change, NRMSD (Branderhorst 2020)
    """
    #init variables für compare funktion
    d_value_list = []                                       
    d_roc_list   = []
    nrmsd_list   = [] 
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

def evaluate_results(results_pop, portion_pop, results_al, portion_al):
    results_total = results_pop * portion_pop + results_al * portion_al
    return  results_total
    
def analyse_measured_pyworld_data():
    #Simulation für erste Zeile - Standard
    world3 = World3(dt = sim_time_step, year_max=year_max)
    world3.init_world3_constants()
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)
    
    # Pyworld Data 
    pyworld_data = measured_data*0
    pyworld_data['year'] = year_data
    pyworld_data['population'] = world3.pop
    pyworld_data['arable_land'] = world3.al
    
    # get index
    index_pop_first = measured_data['population'].index.get_loc(measured_data['population'].first_valid_index())
    index_pop_last = measured_data['population'].index.get_loc(measured_data['population'].last_valid_index())
    
    index_al_first = measured_data['arable_land'].index.get_loc(measured_data['arable_land'].first_valid_index())
    index_al_last = measured_data['arable_land'].index.get_loc(measured_data['arable_land'].last_valid_index())
    
    # data type for function calculate differences
    pop_py   = pyworld_data.iloc[index_pop_first:index_pop_last,1:2].to_numpy()
    pop_data = measured_data.iloc[index_pop_first:index_pop_last,1:2].to_numpy()
    
    al_py   = pyworld_data.iloc[index_al_first:index_al_last,2:3].to_numpy()
    al_data = measured_data.iloc[index_al_first:index_al_last,2:3].to_numpy()
    
    
    #results first step
    results_pop = calculate_differences(pop_py, pop_data, "standard")  #erste Zeile stadard 
    results_al = calculate_differences(al_py, al_data, 3)  #erste Zeile stadard 

    results_data = np.zeros((1, 4))
    results_data[0,0] = 4
    results_data[0,1] = results_pop["NRMSD"]
    results_data[0,2] = results_al["NRMSD"]
    #Gewichtung
    results_data[0,3] = evaluate_results(results_data[0,1],1,results_data[0,1],0)
    results_data = pd.DataFrame(data=results_data, columns = ['dcfs', 'population', 'arable_land', 'total'])
    
    #Schleife für verschiedene Inputs
    for i in range(0,sim_anzahl):
        #simulation durchführen 
        world3 = World3(dt = sim_time_step, year_max=year_max)
        world3.init_world3_constants(dcfsn = start_val+i*delta)
        world3.init_world3_variables()
        world3.set_world3_table_functions()
        world3.set_world3_delay_functions()
        world3.run_world3(fast=False)

        pyworld_data['population'] = world3.pop
        pyworld_data['arable_land'] = world3.al
        
        # data type for function calculate differences
        pop_py   = pyworld_data.iloc[index_pop_first:index_pop_last,1:2].to_numpy()
        pop_data = measured_data.iloc[index_pop_first:index_pop_last,1:2].to_numpy()
        results_pop = (calculate_differences(pop_py, pop_data, start_val+i*delta))
        
        al_py   = pyworld_data.iloc[index_al_first:index_al_last,2:3].to_numpy()
        al_data = measured_data.iloc[index_al_first:index_al_last,2:3].to_numpy()
        results_al = (calculate_differences(al_py, al_data, start_val+i*delta))
        
        result_total = evaluate_results(results_pop['NRMSD'],1,results_pop['NRMSD'],0)
        results_add = pd.DataFrame(data = {'dcfs':[start_val+i*delta], 'population': [results_pop["NRMSD"]],
                                           'arable_land':[results_al["NRMSD"]], 'total': result_total}).astype(float)
        #results_data = results_data.append(results_add, ignore_index=True)      #was ist besser?
        results_data = pd.concat([results_data, results_add], ignore_index=True)

    return    results_data
  
def improved_limits():
    
    delta0 = delta
    NRMSD_index= results_pop["NRMSD"].idxmin()
    start_val = NRMSD_index - delta0
    end_val = NRMSD_index + delta
    delta1 = (end_val-start_val)/(sim_anzahl-1)
    
    return start_val, end_val, delta1


"Run and print Results"
#results_pop = one_constant()
#print(results_pop)
res1=analyse_measured_pyworld_data()
#res = improved_limits()
print(res1)







"TODO"
# inputs multiple constants
# arable land correct data (not all countries in sum)
# one csv with measured data 
# Gewichtung Vergleichsparameter Eingabe oben (siehe erster Punkt)
# Gewichtung Jahre (optional)
# Gewichtung Abweichung (optional)
# multiple data automatisieren
    # eigenständige parameter selektierung (was vorhanden) - Zeile: 
    # vergleichsvariablen zusammenfassen - Zeile:
# kommentare anfang checken!

# Clean Code
    # Data sieh oben
    # array / Dataframe anhängen (alles array oder alles !DataFrame!)
    # use one DataFrame in function compare_differendes instead of single arrays 
    # -> call function only once 
    # fist / last index with DataFrame
