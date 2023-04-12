#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:26:37 2023

@author: rubenwillamowski
"""

import numpy as np
import pandas as pd
import analysis_parallel_settings as s
from scipy.signal import savgol_filter
from scipy import signal
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from PyWorld3_Update.pyworld3 import World3
from datetime import datetime

empirical_settings = pd.read_excel('empirical_settings_BAU2.xlsx', index_col='index', sheet_name='settings')
calculation_period_BAU2 = 5


def smooth(empirical_data, critical_freq):
    b, a = signal.ellip(4, 0.01, 100, critical_freq)  # Filter to be applied
    #good: 6, 0.1, 12, 0.3
        # (order, rp (min allowed ripple(dB), rp (max allowed ripple(dB)), critical frequency))
    empirical_data = signal.filtfilt(b, a, empirical_data, method = 'gust')


def initialize_empirical_data(zeros_2100 = False):
    "Data - measured"
    if not zeros_2100:
        measured_data = pd.read_csv('empirical_data.csv', sep=',')
    else:
        measured_data = pd.read_csv('empirical_data_filled_until2100.csv', sep=';', decimal=',')
    # measured_data = measured_data['data'].str.split(";", expand=True)
    measured_data = measured_data.iloc[:,0:22]
    # measured_data.columns=['Year', 'Population', 'Arable_Land', 'GFCF']
    empirical_data = measured_data#.replace(0, np.nan)
    empirical_data.iloc[66,9] = 0
    # filter settings 

    proportions = ['Food_per_capita_ve','Pollution_CO2_dt','Expected_years_of_schooling','IPP','Fossil_fuel_consumption_TWh']

    for attribute_name in s.empirical_settings.index:
        if s.empirical_settings.loc[attribute_name,'smooth'] == False:
            empirical_data[attribute_name] = empirical_data[attribute_name]
        else:
            empirical_data.iloc[s.empirical_settings.loc[attribute_name,'year_min']-1900:s.empirical_settings.loc[attribute_name,'year_max']-1900,empirical_data.columns.get_loc(attribute_name)]  = smooth(empirical_data.iloc[s.empirical_settings.loc[attribute_name,'year_min']-1900:s.empirical_settings.loc[attribute_name,'year_max']-1900,empirical_data.columns.get_loc(attribute_name)], s.empirical_settings.loc[attribute_name,'smooth'])
    
    empirical_data.iloc[121,17] = 0.01     # smoothing one value manually 
    
    #empirical_data = empirical_data.loc[71:120, :]
    pollution_5dt = [sum(empirical_data['Pollution_CO2_dt'][i:i+5]) for i in range(0, len(empirical_data['Pollution_CO2_dt']), 5)]
    resource_5dt = [sum(empirical_data['Fossil_fuel_consumption_TWh'][i:i+5]) for i in range(0, len(empirical_data['Fossil_fuel_consumption_TWh']), 5)]
    empirical_data = empirical_data[0::5]
    empirical_data = empirical_data[['Year','Population','Food_per_capita_ve','Expected_years_of_schooling','IPP','Human_Welfare','Ecological_Footprint']]
    empirical_data['Pollution_CO2_dt'] = pollution_5dt
    empirical_data['Fossil_fuel_consumption_TWh'] = resource_5dt
    empirical_data = empirical_data.replace(0, np.nan)

    
    for attribute_name in proportions:
            proportion_help1 = np.append(empirical_data[attribute_name],np.NaN)
            proportion_help2 = np.append(np.NaN,empirical_data[attribute_name])
            empirical_data['{0}_{1}'.format(attribute_name,'p')] =  ((proportion_help1-proportion_help2)/proportion_help1)[:-1]    
            
    return empirical_data

def load_model_data():
    results = pd.read_csv('DatenBAU2.csv', sep=',')
    results = results.iloc[:,0:9]


    proportions=['FPC','IO','POL','SPC','NR']

    results['POP'] = results['POP']*10**9
    results['NR'] = results['NR']*10**9
    results['NRdt'] = np.append(np.diff(results['NR']/5),np.nan)
    results['IO'] = results['IO']*10**9
    results['POL'] = results['POL']*10**6
    
    for attribute_name in proportions:
            proportion_help1 = np.append(results[attribute_name],np.NaN)
            proportion_help2 = np.append(np.NaN,results[attribute_name])
            results['{0}_{1}'.format(attribute_name,'p')] =  ((proportion_help1-proportion_help2)/proportion_help1)[:-1]

    results_names =  pd.DataFrame()
    results_names['Year'] = results['Year']
    results_names['pop_0'] = results['POP']
    results_names['fpcp_0'] = results['FPC_p']
    results_names['ppdt_p_0'] = results['POL_p']
    results_names['iop_0'] = results['IO_p']
    results_names['spc_0'] = results['SPC_p']
    results_names['nrup_p'] = results['NR_p']
    results_names['hwi_0'] = results['HWI']
    results_names['ef_0'] = results['EF']


    return results_names    


def calculate_nrmsd(model_data, empirical_data, timestep: float, calculation_interval=5, calculation_period=50):
    ''' Function for the formula for normalized root mean squre difference (NRMSD)
    Originally from Herrington 2020 - Update to limits to growth
    \n inputs:
     two arrays with data
     the timestep between the data points in yrs
     calculation interval in yrs
     the period for calculating the nrmsd in yrs
    \n Output is the calculated nrmsd for the last timestep and the year back the inteval rate
    '''
    no_of_calculations = int(calculation_period / calculation_interval)
    stepwidth = calculation_interval * timestep

    model_data = np.array(model_data)
    empirical_data = np.array(empirical_data)
    nominator_single_values = np.zeros(no_of_calculations)
    denominator_single_values = np.zeros(no_of_calculations)

    for i in range(no_of_calculations):
        nominator_single_values[-i - 1] = np.square(model_data[-i * stepwidth - 1] - empirical_data[-i * stepwidth - 1])
        denominator_single_values[-i - 1] = empirical_data[-i * stepwidth - 1]

    nrmsd = (np.sqrt(nominator_single_values.sum() / len(nominator_single_values))) / (denominator_single_values.sum() / len(denominator_single_values))
    return nrmsd

def calculate_metrics_multiple_attributes(model_data, empirical_data, index=0, calculation_period=50, sim_number=0):
    ''' Calculate NRSMD for selected attributes 
    - using function "prepare_data_for_metric_calc_multiple_attributes" to cut data
    - NRMSD total for weighting attributes'''
    results = pd.DataFrame(index=[index])
    results['NRMSD_total']=0
    attribute_list_empirical = s.empirical_settings.index
    attribute_list_model = (s.empirical_settings['pyworld_name_complete']+"_{}")

    no_of_results_in_total = 0

    for i in np.arange(0, len(attribute_list_empirical)):
        #attribute_empirical(i)
        #attributemodel = (i)
            
        model_data_slice, empirical_data_slice = prepare_data_for_metric_calc_multiple_attributes(model_data, empirical_data, attribute_list_empirical[i], attribute_list_model[i].format(int(index)-1))
        
        results['NRMSD_{}'.format(attribute_list_empirical[i])] = calculate_nrmsd(model_data_slice, empirical_data_slice, timestep=s.sim_time_step,
                                              calculation_interval=s.calculation_interval, calculation_period=calculation_period_BAU2)

        if s.empirical_settings['total'].iloc[i] == True:
            
            #print(results['NRMSD_{}'.format(attribute_list_empirical[i])][0]) #ist nan bei den proportions
            
            results['NRMSD_total'] += results['NRMSD_{}'.format(attribute_list_empirical[i])][0] * \
                                      s.empirical_settings['NRMSD_total_weighting'].iloc[i]
            no_of_results_in_total +=1

    results['NRMSD_total'] = results['NRMSD_total']/no_of_results_in_total

    '''results['NRMSD_total'] = ((results['NRMSD_Population']+
                                 1*results['NRMSD_Death_rate']+
                                 1*results['NRMSD_Birth_rate'])+
                                 1*results['NRMSD_Food_per_capita_ve']+
                                 1*results['NRMSD_Pollution_proportion']+
                                 1*results['NRMSD_Expected_years_of_schooling_proportion']+
                                 #1*results['NRMSD_GFCF_proportion']+
                                 1*results['NRMSD_Fossil_fuel_consumption_proportion']+
                                 1*results['NRMSD_IPP_proportion'])/8'''
    
    return results

def prepare_data_for_metric_calc_multiple_attributes(model_data: pd.DataFrame, empirical_data: pd.DataFrame, variable_empirical, variable_model):
    """used in function "calculate_metrics_multiple_attributes" to cut big data for NRMSD calculation with fitting period
    - start and stop years can be selected in settings """
    start_row = int((s.empirical_settings.loc[variable_empirical, 'year_min'] - 1900)/5)
    stop_row = int((s.empirical_settings.loc[variable_empirical, 'year_max']- 1900)/5)
    
    result_model = model_data[variable_model][start_row:stop_row]
    result_empirical = empirical_data[variable_empirical][start_row:stop_row]
    
    print(result_model)
    print(result_empirical)
    
    return result_model, result_empirical



empirical_data=initialize_empirical_data()
results = load_model_data()

metric_result = calculate_metrics_multiple_attributes(results, empirical_data, 1)






