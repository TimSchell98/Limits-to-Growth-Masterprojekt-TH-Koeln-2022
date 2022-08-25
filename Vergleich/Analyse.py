import importlib.util

MODULE_PATH = "C:/Users/Tim Schell/Documents/GitHub/pyworld3/pyworld3"
MODULE_NAME = "pyworld3"


spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
modulevar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulevar)

import matplotlib.pyplot as plt
import numpy as np
from xlwt import Workbook
from pyworld3 import World3
from pyworld3.utils import plot_world_variables
import pandas as pd

import time
startTime = time.time()

"Data decleration"
## Import Observed Data
# Population
pop_data_big = pd.read_csv('Data_population.csv')
pop_data = pop_data_big.iloc[0:1, 19:]              # Data from 1970 - 2021
pop_data = np.transpose(pop_data.values.tolist())

#Einteilen des Simulationsrasters
sim_anzahl = 11
start_val = 3
end_val = 5
delta = (end_val-start_val)/(sim_anzahl-1)

def compare(pyworld_data, real_data, sensivity_variable):
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

def one_constant():
    #Ergebnis-Matrix in Schleife berechnen
    #erste Zeile
    world3 = World3(dt = 1, year_max = 2023)
    world3.init_world3_constants()
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)
    ## Define Pyworld Data 
    #population
    pop_py= world3.pop[75:122]                          # Data from 1970 - 2021
    results_pop = compare(pop_py, pop_data, "standard")  #erste Zeile stadard
    for i in range(0,sim_anzahl):
        #simulation durchführen 
        world3 = World3(dt = 1)
        world3.init_world3_constants(dcfsn = start_val+i*delta)
        world3.init_world3_variables()
        world3.set_world3_table_functions()
        world3.set_world3_delay_functions()
        world3.run_world3(fast=False)
        ## Define Pyworld Data 
        #population
        pop_py= world3.pop[75:122]                          # Data from 1970 - 2021
        #Evaluation
        #compare(pyworld_data, real_data, sensivity_variable):
        results_pop = results_pop.append(compare(pop_py, pop_data, start_val+i*delta))
    return results_pop   

def multiple_constants():
    "TODO"
    return    
  
def improved_limits():
    
    delta0 = delta
    NRMSD_index= results_pop["NRMSD"].idxmin()
    start_val = NRMSD_index - delta0
    end_val = NRMSD_index + delta0
    delta1 = (end_val-start_val)/(sim_anzahl-1)
    
    return start_val, end_val, delta1

results_pop = one_constant()
print(results_pop)
res = improved_limits()
print(res)






