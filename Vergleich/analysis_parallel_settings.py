import pandas as pd
import numpy as np

# - - - - - Global  Settings
use_update = False #should updated World3 be used in the analysis
run_parallel = True #should analysis run parallel
single_parameter_zoom = 0 #how often should the parameter with the highest influence be improved alone
grid_resolution = 3 #number of simulations per zoom
zoom_limit = False #If true, analysis runs till NRMSD is equal or lower than "result_accuracy". If false, analysis runs till it reaches the grid zoom
grid_zoom = 0 #number of zooms, gerade nicht benutzt
result_accuracy = 0 #accuracy, when zoom should stop
delta_end = 0.0001 #at witch delta the simulation should stopp
sim_time_step = 1 #pro Jahr in Simulation
year_max = 2022
year_max1 = year_max +1
year_min = 1900
period  = year_max1 - year_min # wird es noch benötigt?




#temporäre variablen, ich muss mir noch was besseres einfallen lassen
x = 1
parameter_hi = 0

#how much should the start/end limits be from the default. 0.5 = 50%, 1 = 100%, 2 = 200%
parameter_divergence = 0.25

# - Analysis Settings
calculation_interval = 5 # step size [years] for calculation
calculation_period = 30  # period [years ]for calculation

# - - - - - Parameter Settings 
#1) desired complete family size normal - default = 4
parameter1_default = 4
parameter1_name = "dcfsn"

#parameter modifier for improved limits function
parameter1_modifier = parameter1_default/(grid_resolution*2)

#2) fraction res pers mtl - default = 0.02
parameter2_default = 0.02
parameter2_name = "frpm"

#parameter modifier for improved limits function
parameter2_modifier = parameter2_default/(grid_resolution*2)

#3) processing loss  - default = 0.1
parameter3_default = 0.1
parameter3_name = "pl"

#parameter modifier for improved limits function
parameter3_modifier = parameter3_default/(grid_resolution*2)

def parameter_init():
    #parameter1 start+end value
    if parameter1_default-parameter1_default*parameter_divergence < 0:
        parameter1_start_val = 0
    else:
        parameter1_start_val = parameter1_default-parameter1_default*parameter_divergence
    parameter1_end_val = parameter1_default+parameter1_default*parameter_divergence
    
    #parameter2 start+end value 
    if parameter2_default-parameter2_default*parameter_divergence < 0:
        parameter2_start_val = 0
    else:
        parameter2_start_val = parameter2_default-parameter2_default*parameter_divergence
    parameter2_end_val = parameter2_default+parameter2_default*parameter_divergence
    
    #parameter3 start+end value
    if parameter3_default-parameter3_default*parameter_divergence < 0:
        parameter3_start_val = 0
    else:
        parameter3_start_val = parameter3_default-parameter3_default*parameter_divergence
    parameter3_end_val = parameter3_default+parameter3_default*parameter_divergence
    
    # - - Dataframe Settings
    setting_values = {'start_value':[parameter1_start_val, parameter2_start_val, parameter3_start_val],
                      'end_value':[parameter1_end_val, parameter2_end_val, parameter3_end_val] }
    setting_values = pd.DataFrame( data = setting_values, index = ['parameter1', 'parameter2', 'parameter3'])
    setting_values['delta'] = (setting_values['end_value'] - setting_values['start_value'])/(grid_resolution-1)
    
    #print(setting_values)
    
    # - - Dataframe Parameter list
    parameter_var_list_sorted = {'parameter1': np.arange(setting_values.iloc[0,0], setting_values.iloc[0,1]+0.00001, setting_values.iloc[0,2]),
                          'parameter2': np.arange(setting_values.iloc[1,0], setting_values.iloc[1,1]+0.00001, setting_values.iloc[1,2]),
                          'parameter3': np.arange(setting_values.iloc[2,0], setting_values.iloc[2,1]+0.00001, setting_values.iloc[2,2])}
    
    parameter_var_list_sorted = pd.DataFrame(data=parameter_var_list_sorted)
    
    
    #parameter_var_list_full is a list of every combination of the parameters
    parameter_var_list_full = pd.DataFrame()
    i1 = 0
    i2 = 0
    i3 = 0
    j = 0
    x = 0
    for i in range (0,grid_resolution**3):
        #fill parameter_var_list_full with parameter 1
        i1 = i1+1
        parameter_var_list_full.loc[i,0] = parameter_var_list_sorted.iloc[i1-1,0]
        if i1 == grid_resolution:
            i1 = 0
            
        #fill parameter_var_list_full with parameter 2
        j = j+1
        
        parameter_var_list_full.loc[i,1] = parameter_var_list_sorted.iloc[i2,1]
        if j == grid_resolution:
            
            j = 0
            i2 = i2+1
        if i2 == grid_resolution:
            i2 = 0

        
        #fill parameter_var_list_full with parameter 3
        x = x+1
        parameter_var_list_full.loc[i,2] = parameter_var_list_sorted.iloc[i3,2]
        if x == grid_resolution**2:
            x = 0
            i3 = i3+1
        if i3 == grid_resolution:
            i3 = 0
        
    print("Starting limits:")
    print(parameter_var_list_sorted)
    print("Parameter1 = " + parameter1_name)
    print("Parameter2 = " + parameter2_name)
    print("Parameter3 = " + parameter3_name)
    
    return parameter_var_list_full, parameter_var_list_sorted





# - - - - - empirical data settings
# population 
pop_name = 'Population'
pop_y_min = 1960
pop_y_max = 2021
#index_pop_last = measured_data['population'].index.get_loc(measured_data['population'].last_valid_index())

# Arable Land
al_name = 'Arable_land'
al_year_min = 1961
al_year_max = 2020

# Crude Death Rate
cdr_name = 'Death_rate'
cdr_year_min = 1970
cdr_year_max = 2020

# Crude Birth Rate
cbr_name = 'Birth_rate'
cbr_year_min = 1970
cbr_year_max = 2020

# Gross Fixed Capital Formation
gfcf_name = 'GFCF'
gfcf_year_min = 1970
gfcf_year_max = 2020

# Food per Capita Vegetable Equivalent
fpc_name = 'Food_per_capita_ve'
fpc_year_min = 1961
fpc_year_max = 2019

# Pollution CO2
polco2_name = 'Pollution_CO2'
polco2_year_min = 1979
polco2_year_max = 2021

polco2_dt_name = 'Pollution_CO2_dt'
polco2_dt_year_min = 1959
polco2_dt_year_max = 2021

nrur_name = 'Fossil_fuel_consumption_TWh'
nrur_year_min = 1965
nrur_year_max = 2021

sopc_dt_name = 'Expected_years_of_schooling'
sopc_dt_year_min = 1990
sopc_dt_year_max = 2021

# - Settings to Dataframe
empirical_settings = pd.DataFrame(index=[pop_name, cdr_name, cbr_name, al_name, fpc_name, polco2_dt_name, nrur_name, gfcf_name, sopc_dt_name])
empirical_settings['year_min'] = (pop_y_min, cdr_year_min, cbr_year_min, al_year_min, fpc_year_min, polco2_dt_year_min, nrur_year_min, gfcf_year_min, sopc_dt_year_min)
empirical_settings['year_max'] = (pop_y_max, cdr_year_max, cbr_year_max, al_year_max, fpc_year_max, polco2_dt_year_max, nrur_year_max, gfcf_year_max, sopc_dt_year_max)
empirical_settings['pyworld_name'] = ('POP', 'CRD', 'BRD', 'AL', 'FPC', 'POLC_dt', 'NRUR', 'IO_dt', 'SOPC_dt')
empirical_settings['pyworld_name_add'] = ('POP_{}', 'CBR_{}', 'CDR_{}', 'AL_{}', 'FPC_{}', 'POLC_dt_{}', 'NRUR_{}', 'IO_dt_{}', 'SOPC_dt_{}')


if __name__ == '__main__':
    print(parameter_init())
    #print(empirical_settings)
    #print(empirical_settings[empirical_settings['name'] == 'Population']['year_min'])
    #print(empirical_settings.loc[pop_name, 'year_min'])
    #print(setting_values)
    #print(parameter_var_list)