import pandas as pd
import numpy as np

# - - - - - Global  Settings
grid_resolution = 3 #number of simulation
grid_zoom = 0 #number of zooms
sim_time_step = 1 #pro Jahr in Simulation
year_max = 2021
year_max1 = year_max +1
year_min = 1900
period  = year_max1 - year_min # wird es noch benötigt?

# - Analysis Settings
calculation_interval = 5

# - - - - - Parameter Settings 
#1) desired complete family size normal - default = 4
parameter1_name = "dcfsn"
parameter1_start_val = 3.0
parameter1_end_val = 5.0

#2) fraction res pers mtl - default = 0.02
parameter2_name = "frpm"
parameter2_start_val = 0.01
parameter2_end_val = 0.03

#3) processing loss  - default = 0.1
parameter3_name = "pl"
parameter3_start_val = 0.01
parameter3_end_val = 0.3

def parameter_init():
    # - - Dataframe Settings
    setting_values = {'start_value':[parameter1_start_val, parameter2_start_val, parameter3_start_val],
                      'end_value':[parameter1_end_val, parameter2_end_val, parameter3_end_val] }
    setting_values = pd.DataFrame( data = setting_values, index = ['parameter1', 'parameter2', 'parameter3'])
    setting_values['delta'] = (setting_values['end_value'] - setting_values['start_value'])/(grid_resolution-1)
    
    # - - Dataframe Parameter list #TODO als Function und verbessern
    parameter_var_list = {'parameter1': np.arange(setting_values.iloc[0,0], setting_values.iloc[0,1]+0.001, setting_values.iloc[0,2]),
                          'parameter2': np.arange(setting_values.iloc[1,0], setting_values.iloc[1,1]+0.001, setting_values.iloc[1,2]),
                          'parameter3': np.arange(setting_values.iloc[2,0], setting_values.iloc[2,1]+0.001, setting_values.iloc[2,2])}
    parameter_var_list = pd.DataFrame(data=parameter_var_list)
    
    return parameter_var_list


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
crd_name = 'Death_rate'
crd_year_min = 1970
crd_year_max = 2020

# Crude Birth Rate
brd_name = 'Birth_rate'
brd_year_min = 1970
brd_year_max = 2020

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
polco2_year_min = 1960
polco2_year_max = 2021

# - Settings to Dataframe
empirical_settings = pd.DataFrame(index=[pop_name, al_name, crd_name, brd_name, gfcf_name, fpc_name, polco2_name], columns=['name' ,'year_min','year_max'])
empirical_settings['name'] = (pop_name, al_name, crd_name, brd_name, gfcf_name, fpc_name, polco2_name)
empirical_settings['year_min'] = (pop_y_min, al_year_min, crd_year_min, brd_year_min, gfcf_year_min, fpc_year_min, polco2_year_min)
empirical_settings['year_max'] = (pop_y_max, al_year_max, crd_year_max, brd_year_max, gfcf_year_max, fpc_year_max, polco2_year_max)



if __name__ == '__main__':
    print(empirical_settings)
    #print(empirical_settings[empirical_settings['name'] == 'Population']['year_min'])
    #print(empirical_settings.loc[pop_name, 'year_min'])
    #print(parameter_var_list)