import pandas as pd
import numpy as np

# - - - - - Global  Settings
sim_anzahl = 11
sim_time_step = 1 #pro Jahr in Simulation
year_max = 2021
year_max1 = year_max +1
year_min = 1900
period  = year_max1 - year_min # wird es noch benötigt?

# - Analysis Settings
calculation_interval = 5



# - - - - - Parameter Settings 
#1) desired complete family size normal
dcfsn_start_val = 3.0
dcfsn_end_val = 5.0
dcfsn_delta = (dcfsn_end_val-dcfsn_start_val)/(sim_anzahl-1) 
dcfsn_var = np.arange(dcfsn_start_val, dcfsn_end_val+0.001, dcfsn_delta)

#2) industrial output per capita desired
iopcd_start_val = 300.0
iopcd_end_val = 500.0


#3) processing loss 
pl_start_val = 0.01
pl_end_val = 0.3

# - - Dataframe Settings
setting_values = {'start_value':[dcfsn_start_val, iopcd_start_val, pl_start_val],
                  'end_value':[dcfsn_end_val, iopcd_end_val, pl_end_val] }
setting_values = pd.DataFrame( data = setting_values, index = ['dcfsn', 'iopcd', 'pl'])
setting_values['delta'] = (setting_values['end_value'] - setting_values['start_value'])/(sim_anzahl-1)

# - - Dataframe Parameter list
parameter_var_list = {'dcfsn': np.arange(setting_values.iloc[0,0], setting_values.iloc[0,1]+0.001, setting_values.iloc[0,2]),
                      'iopcd': np.arange(setting_values.iloc[1,0], setting_values.iloc[1,1]+0.001, setting_values.iloc[1,2]),
                      'pl': np.arange(setting_values.iloc[2,0], setting_values.iloc[2,1]+0.001, setting_values.iloc[2,2])}
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