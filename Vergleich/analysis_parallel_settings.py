import pandas as pd

#Einteilen des Simulationsrasters
sim_anzahl = 2
dcfsn_start_val = 3
dcfsn_end_val = 5
dcfsn_delta = (dcfsn_end_val-dcfsn_start_val)/(sim_anzahl-1)
#Simulation
sim_time_step = 1 #pro Jahr in Simulation
year_max = 2021
year_max1 = year_max +1
year_min = 1900
period  = year_max1 - year_min


# analysis setting
calculation_interval = 5


# - - - - - empirical data settings
# population - -
pop_name = 'Population'
pop_y_min = 1970
pop_y_max = 2018

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