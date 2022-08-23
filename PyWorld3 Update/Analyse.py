import matplotlib.pyplot as plt
import numpy as np
from xlwt import Workbook
from pyworld3 import World3
from pyworld3.utils import plot_world_variables
import pandas as pd

import time
startTime = time.time()

#Excel sheets für jede Variable die verglichen werden sollen
wb = Workbook()
res = wb.add_sheet("Results")
var = wb.add_sheet("Eingangsparameter")
pop = wb.add_sheet("Population")
d = wb.add_sheet("Death per Year")
b = wb.add_sheet("Birth per Year")
fpc = wb.add_sheet("Food per Capita")
ef = wb.add_sheet("Ecological Footprint")
hwi = wb.add_sheet("Human Welfare Index")



"Data decleration"
## Import Observed Data
# Population
pop_data_big = pd.read_csv('Data_population.csv')
pop_data = pop_data_big.iloc[0:1, 19:]              # Data from 1970 - 2021
pop_data = np.transpose(pop_data.values.tolist())

# Food per capita

#berechnen der eingangsparameter "sprünge"
sim_anzahl = 11
start_val = 3
end_val = 4
delta = (end_val-start_val)/(sim_anzahl-1)

#eingangs Variablen die verändert werden sollen
def dcfsn_f(i, sim_anzahl):
    
    #hier können wir eine funktion einfügen die die eingangs parameter berechnen, dieser wird auch in der excel geschrieben
    var.write(i+1, 0, start_val+i*delta)
    return start_val+i*delta

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
    
    results_array = [d_value_sum,d_roc_sum,nrmsd_sum]
    
    return results_array

#ausgelagerte initierung für die verbesserung der Laufzeit
world3 = World3(dt = 1)

for i in range(0,sim_anzahl):
    print("\nSimulation" , end =": ")
    print(i+1)
    print("ETA", end =": ")
    print(round((sim_anzahl-i)*2.8,2), end = "")
    print("s")

    #simulation durchführen
    world3.init_world3_constants(dcfsn = dcfsn_f(i, sim_anzahl))
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)
    
    ## Define Pyworld Data 
    #population
    pop_py= world3.pop[75:122]                          # Data from 1970 - 2021
    
    print("dcfsn", end = ": ")
    print(world3.dcfsn)
    "Evaluation"
    #compare(pyworld_data, real_data, sensivity_variable):
    results_array = compare(pop_py, pop_data, "population")
    print("Results:", end = ": ")
    print(results_array)
    
    #alle Werte der Vergleichsvariablen in Excel schrieben
    for y in range(0,200):
        pop.write(y+1, i+1, world3.pop[y])
        d.write(y+1, i+1, world3.d[y])
        b.write(y+1, i+1, world3.b[y])
        fpc.write(y+1, i+1, world3.fpc[y])
        ef.write(y+1, i+1, world3.ef[y])
        hwi.write(y+1, i+1, world3.hwi[y])
        


#excel speichern
wb.save('sim-values.xls')

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))