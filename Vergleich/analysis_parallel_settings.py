import pandas as pd
import numpy as np

# - - - - - Global  Settings

grid_resolution = 5 #number of simulation
grid_zoom = 2 #number of zooms
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

# - - - - - empirical data settings
# population 
pop_name = 'Population'
pop_y_min = 1970
pop_y_max = 2018
#index_pop_last = measured_data['population'].index.get_loc(measured_data['population'].last_valid_index())

# Arable Land
al_name = 'Arable_Land'
al_year_min = 1970
al_year_max = 2018

# - Settings to Dataframe
empirical_settings = pd.DataFrame(index=[pop_name, al_name], columns=['name' ,'year_min','year_max'])
#empirical_settings['name'] = (pop_name, al_name)
empirical_settings['year_min'] = (pop_y_min, al_year_min)
empirical_settings['year_max'] = (pop_y_max, al_year_max)


if __name__ == '__main__':
    print(empirical_settings)
    print(empirical_settings[empirical_settings['name'] == 'Population']['year_min'])
    print(empirical_settings.loc[pop_name, 'year_min'])
    print(setting_values)
    print(parameter_var_list)