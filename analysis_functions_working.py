import numpy as np
import pandas as pd
import analysis_parallel_settings_working as s
import analysis as p
from scipy.signal import savgol_filter
from scipy import signal
from scipy.signal import butter, lfilter, freqz


import matplotlib.pyplot as plt
from PyWorld3_Update.pyworld3 import World3
#from PyWorld3_Old.pyworld3 import World3

def run_simulation(i=0, **kwargs):
    """
    Functions for running the World3 Model with variable set of parameters.
    Return Value is a pandas Dataframe with certain selected Model Variables.

        Parameters:
                i = Number of simulation when used in a multi-run skript, for naming the output Dataframe
                **kwargs = world3 variables that are initialized at the start of world3.
                            The arguments are passed directly to the initialization

        Returns:
                Pandas Dataframe that contains certain parameters of the simulation

    """

    # run simulation
    world3 = World3(dt=s.sim_time_step, year_max=s.year_max)
    world3.init_world3_constants(**kwargs)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)

    # gather simulation data
    simulation_data = pd.DataFrame()
    for attribute_name in s.empirical_settings.index:
        if  s.empirical_settings.loc[attribute_name,'type']=='pyworld':
            simulation_data['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] = getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name'])
        elif s.empirical_settings.loc[attribute_name,'type']=='derivation':    
            simulation_data['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] = np.append((np.diff(getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']))/s.sim_time_step),np.nan) 
        elif s.empirical_settings.loc[attribute_name,'type']=='proportion':
            proportion_help1 = np.append(getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']),np.NaN)
            proportion_help2 = np.append(np.NaN,getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']))
            simulation_data['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] =  ((proportion_help1-proportion_help2)/proportion_help1)[:-1]

    # print('Ending Simulation {}'.format(i))

    return simulation_data


def run_simulation_combinations(i, parameter_list_full):
    """
    Functions for running the World3 Model with variable set of parameters.
    Return Value is a pandas Dataframe with certain selected Model Variables.

        Parameters:
                i = Number of simulation when used in a multi-run skript, for naming the output Dataframe
                parameter_list_full = dataframe which contains every combination of parameter value steps

        Returns:
                Pandas Dataframe that contains certain parameters of the simulation

    """

    # run simulation
    world3 = World3(dt=s.sim_time_step, year_max=s.year_max)
    world3.init_world3_constants(dcfsn = parameter_list_full.iloc[i,0], mtfn = parameter_list_full.iloc[i,1]) #usw.....keine ahnung wie das dynamisch gehen soll
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)

    # gather simulation data
    simulation_data = pd.DataFrame()
    for attribute_name in s.empirical_settings.index:
        if  s.empirical_settings.loc[attribute_name,'type']=='pyworld':
            simulation_data['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] = getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name'])
        elif s.empirical_settings.loc[attribute_name,'type']=='derivation':    
            simulation_data['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] = np.append((np.diff(getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']))/s.sim_time_step),np.nan) 
        elif s.empirical_settings.loc[attribute_name,'type']=='proportion':
            proportion_help1 = np.append(getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']),np.NaN)
            proportion_help2 = np.append(np.NaN,getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']))
            simulation_data['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] =  ((proportion_help1-proportion_help2)/proportion_help1)[:-1]

    # print('Ending Simulation {}'.format(i))

    return simulation_data

def run_simulation_kwargs(year_max, i=0, **kwargs):
    """
    Functions for running the World3 Model with variable set of parameters.
    Return Value is a pandas Dataframe with certain selected Model Variables.

        Parameters:
                i = Number of simulation when used in a multi-run skript, for naming the output Dataframe
                **kwargs = world3 variables that are initialized at the start of world3.
                            The arguments are passed directly to the initialization

        Returns:
                Pandas Dataframe that contains certain parameters of the simulation

    """

    # run simulation
    world3 = World3(dt=s.sim_time_step, year_max=year_max)
    world3.init_world3_constants(**kwargs)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)

    # gather simulation data
    simulation_data = pd.DataFrame()
    for attribute_name in s.empirical_settings.index:
        if  s.empirical_settings.loc[attribute_name,'type']=='pyworld':
            simulation_data['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] = getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name'])
        elif s.empirical_settings.loc[attribute_name,'type']=='derivation':    
            simulation_data['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] = np.append((np.diff(getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']))/s.sim_time_step),np.nan) 
        elif s.empirical_settings.loc[attribute_name,'type']=='proportion':
            proportion_help1 = np.append(getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']),np.NaN)
            proportion_help2 = np.append(np.NaN,getattr(world3,s.empirical_settings.loc[attribute_name,'pyworld_name']))
            simulation_data['{0}_{1}'.format(s.empirical_settings.loc[attribute_name,'pyworld_name_complete'], i)] =  ((proportion_help1-proportion_help2)/proportion_help1)[:-1]


    #simulation_data['Ecological-Footprint_{}'.format(i)] = world3.ef
    #simulation_data['Human-Welfare-Index_{}'.format(i)] = world3.hwi
    # print('Ending Simulation {}'.format(i))

    return simulation_data


def init_parameter_list():
    """
    
    Returns
    -------
    parameter_list_shortened : TYPE Pandas DataFrame
        Returns DataFrame of all parameters which will be analysed. Set in excel "Parameter"

    """
    #read excel with to be analysed parameters
    parameter_list = pd.read_excel('Parameter.xlsx')
    #shortened = parameter list if collumn "use_in_analysis" == True
    parameter_list_shortened = parameter_list
    parameter_list_shortened = parameter_list[parameter_list.use_in_analysis == True]
    #rename index 
    parameter_list_shortened.set_index([np.arange(parameter_list_shortened.shape[0])], inplace = True)
    
    #if use standard == true, use parameter_divergence to calculate start and end value and write it into parameter list, to be used in parameter_list_full function
    for i in range (0,parameter_list_shortened.shape[0]):
        if parameter_list_shortened.iloc[i,3] == True:
            parameter_list_shortened.iloc[i,4] = round(parameter_list_shortened.iloc[i,2]-parameter_list_shortened.iloc[i,2]*s.parameter_divergence,4)
            parameter_list_shortened.iloc[i,5] = round(parameter_list_shortened.iloc[i,2]+parameter_list_shortened.iloc[i,2]*s.parameter_divergence,4)

    return parameter_list_shortened

def parameter_list_full(parameter_list):
    """
    
    Parameters
    ----------
    parameter_list : TYPE Pandas DataFrame
        DataFrame which contains parameter names and values

    Returns
    -------
    parameter_list_full : TYPE Pandas DataFrame
        DataFrame which contains all the combinations of every parameter.

    """

    parameter_list_steps= pd.DataFrame(index = np.arange(s.grid_resolution))
    #loop for filling parameter_list_full
    for i in range (0,parameter_list.shape[0]):
        
        #pull start and end value out of parameter_list
        start_val = parameter_list.iloc[i,4]
        end_val = parameter_list.iloc[i,5]
        
        #calculate delta from start and end value
        delta = round((end_val-start_val)/(s.grid_resolution-1),6)
        #create and write steps into parameter_list_steps
        for j in range (0,s.grid_resolution):
            parameter_list_steps.loc[j,i] = round(start_val+delta*j,6)
    parameter_list_steps.rename(columns = parameter_list.name, inplace = True)
    
    #create dataframe with every possible combination
    #create base
    parameter_list_full = pd.DataFrame(columns = [parameter_list.name],index = np.arange(s.grid_resolution*parameter_list.shape[0]))
    #fill parameter_list_full with standard values
    for i in range(0,parameter_list.shape[0]*s.grid_resolution):
        for j in range(0,parameter_list.shape[0]):
            parameter_list_full.iloc[i,j] = parameter_list.iloc[j,2]
    #fill parameter_list_full with steps     
    for i in range(0,parameter_list.shape[0]):
        for j in range(0,s.grid_resolution):
            parameter_list_full.iloc[j+i*s.grid_resolution,i] = parameter_list_steps.iloc[j,i]

    return parameter_list_full
    

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

    nrmsd = (np.sqrt(nominator_single_values.sum() / 6)) / (denominator_single_values.sum() / 6)
    return nrmsd

def calculate_metrics_multiple_attributes(model_data, empirical_data, index=0, calculation_period=50, sim_number=0):
    """ Calculate NRSMD for selected attributes 
    - using function "prepare_data_for_metric_calc_multiple_attributes" to cut data
    - NRMSD total for weighting attributes"""
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
                                              calculation_interval=s.calculation_interval, calculation_period=s.calculation_period)

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
    start_row = s.empirical_settings.loc[variable_empirical, 'year_min'] * s.sim_time_step - 1900
    stop_row = s.empirical_settings.loc[variable_empirical, 'year_max'] * s.sim_time_step - 1900
    result_model = model_data[variable_model][start_row:stop_row]
    result_empirical = empirical_data[variable_empirical][start_row:stop_row]
    
    return result_model, result_empirical


def prepare_data_for_metric_calc(model_data:pd.DataFrame, empirical_data:pd.DataFrame, variable):
    start_row = s.empirical_settings.loc[variable, 'year_min']*s.sim_time_step-1900
    stop_row = s.empirical_settings.loc[variable, 'year_max']*s.sim_time_step-1900
    result_model = model_data[start_row:stop_row]
    result_empirical = empirical_data[variable][start_row:stop_row]
    return result_model, result_empirical

def calculate_metrics(model_data, empirical_data, index=0, parameter_name='none', parameter_value=np.nan,
                      calculation_period=50):
    results = pd.DataFrame(index=[index])
    if not parameter_name == 'none':
        results['{}'.format(parameter_name)] = parameter_value
    results['NRMSD[%]'] = calculate_nrmsd(model_data, empirical_data, timestep=s.sim_time_step, calculation_interval=s.calculation_interval, calculation_period=calculation_period)
    return results


def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def initialize_empirical_data():
    "Data - measured"
    measured_data = pd.read_csv('empirical_data.csv', sep=',')
    # measured_data = measured_data['data'].str.split(";", expand=True)
    measured_data = measured_data.iloc[:,0:22]
    # measured_data.columns=['Year', 'Population', 'Arable_Land', 'GFCF']
    empirical_data = measured_data.replace(0, np.nan)
    empirical_data.iloc[66,9] = 0
    # filter settings 
    fs= 11
    order = 6
    
    for attribute_name in s.empirical_settings.index:
        if s.empirical_settings.loc[attribute_name,'smooth'] == False:
            empirical_data[attribute_name] = empirical_data[attribute_name]
        else:
            empirical_data.iloc[s.empirical_settings.loc[attribute_name,'year_min']-1900:s.empirical_settings.loc[attribute_name,'year_max']-1900,empirical_data.columns.get_loc(attribute_name)]  = butter_lowpass_filter(empirical_data.iloc[s.empirical_settings.loc[attribute_name,'year_min']-1900:s.empirical_settings.loc[attribute_name,'year_max']-1900,empirical_data.columns.get_loc(attribute_name)], s.empirical_settings.loc[attribute_name,'smooth'], fs, order)
    
    return empirical_data

def improved_limits_all_parameter(metrics, parameter_var_list, parameter_var_list_sorted):
    """
    Find the combination at which the NRMSD is minimal.
    Cecks if parameter is boundary value, if yes calculate next value as new limit.
    Calculate new limits.
    """
    #print old limits
    print("Parameter1 = " + s.parameter1_name)
    print("Parameter2 = " + s.parameter2_name)
    print("Parameter3 = " + s.parameter3_name)
    
    #das könnte man eigentlich allgemein halten und dann 3 mal ausführen
    
    
    #set initial limits
    parameter1_start_val_old = round(parameter_var_list_sorted.iloc[0,0],6)
    parameter1_end_val_old = round(parameter_var_list_sorted.iloc[s.grid_resolution-1,0],6)
    parameter2_start_val_old = round(parameter_var_list_sorted.iloc[0,1],6)
    parameter2_end_val_old = round(parameter_var_list_sorted.iloc[s.grid_resolution-1,1],6)
    parameter3_start_val_old = round(parameter_var_list_sorted.iloc[0,2],6)
    parameter3_end_val_old = round(parameter_var_list_sorted.iloc[s.grid_resolution-1,2],6)
    
    #find index of optimal combination
    NRMSD_index= int(metrics["NRMSD_Population"].idxmin())
    
    #find optimal combination parameter values
    parameter1_val = round(metrics.iloc[NRMSD_index-1,0],6)
    parameter2_val = round(metrics.iloc[NRMSD_index-1,1],6)
    parameter3_val = round(metrics.iloc[NRMSD_index-1,2],6)

    #find index of parameters, probably a better solution but not found
    for i in range (0,s.grid_resolution):
        if round(parameter_var_list_sorted.iloc[i,0],6) == round(parameter1_val,6):
            index_parameter1 = i

    for i in range (0,s.grid_resolution):
        if round(parameter_var_list_sorted.iloc[i,1],6) == round(parameter2_val,6):
            index_parameter2 = i

    for i in range (0,s.grid_resolution):
        if round(parameter_var_list_sorted.iloc[i,2],6) == round(parameter3_val,6):
            index_parameter3 = i
            
    #check if parameter values are boundry values and set new limits
    if parameter1_val == parameter1_start_val_old and parameter1_val != parameter1_end_val_old:
        parameter1_start_val = round(parameter1_val-(((parameter1_end_val_old-parameter1_start_val_old)/(s.grid_resolution-1))*2),5)
        if parameter1_start_val < 0:
            parameter1_start_val = 0
        parameter1_end_val = round(parameter_var_list_sorted.iloc[index_parameter1+2,0],6)
        
    if parameter1_val == parameter1_end_val_old and parameter1_val != parameter1_start_val_old:
        parameter1_end_val = round(parameter1_val+(((parameter1_end_val_old-parameter1_start_val_old)/(s.grid_resolution-1))*2),5)
        parameter1_start_val = round(parameter_var_list_sorted.iloc[index_parameter1-2,0],6)
        
    if parameter1_val != parameter1_start_val_old and parameter1_val != parameter1_end_val_old:
        parameter1_start_val = round(parameter_var_list_sorted.iloc[index_parameter1-1,0],6)
        parameter1_end_val = round(parameter_var_list_sorted.iloc[index_parameter1+1,0],6)
    
    if parameter2_val == parameter2_start_val_old and parameter2_val != parameter2_end_val_old:
        parameter2_start_val = round(parameter2_val-(((parameter2_end_val_old-parameter2_start_val_old)/(s.grid_resolution-1))*2),4)
        if parameter2_start_val < 0:
            parameter2_start_val = 0
        parameter2_end_val = round(parameter_var_list_sorted.iloc[index_parameter2+2,1],6)
        
    if parameter2_val == parameter2_end_val_old and parameter2_val != parameter2_start_val_old:
        parameter2_end_val = round(parameter2_val+(((parameter2_end_val_old-parameter2_start_val_old)/(s.grid_resolution-1))*2),4)
        parameter2_start_val = round(parameter_var_list_sorted.iloc[index_parameter2-2,1],6)
        
    if parameter2_val != parameter2_start_val_old and parameter2_val != parameter2_end_val_old:
        parameter2_start_val = round(parameter_var_list_sorted.iloc[index_parameter2-1,1],6)
        parameter2_end_val = round(parameter_var_list_sorted.iloc[index_parameter2+1,1],6)
    
    if parameter3_val == parameter3_start_val_old and parameter3_val != parameter3_end_val_old:
        parameter3_start_val = round(parameter3_val-(((parameter3_end_val_old-parameter3_start_val_old)/(s.grid_resolution-1))*2),4)
        if parameter3_start_val < 0:
            parameter3_start_val = 0
        parameter3_end_val = round(parameter_var_list_sorted.iloc[index_parameter3+2,2],6)
        
    if parameter3_val == parameter3_end_val_old and parameter3_val != parameter3_start_val_old:
        parameter3_end_val = round(parameter3_val+(((parameter3_end_val_old-parameter3_start_val_old)/(s.grid_resolution-1))*2),4)
        parameter3_start_val = round(parameter_var_list_sorted.iloc[index_parameter3-2,2],6)
        
    if parameter3_val != parameter3_start_val_old and parameter3_val != parameter3_end_val_old:
        parameter3_start_val = round(parameter_var_list_sorted.iloc[index_parameter3-1,2],6)
        parameter3_end_val = round(parameter_var_list_sorted.iloc[index_parameter3+1,2],6)
    
    #calculate new parameter dataframe with steps
    setting_values = {'start_value':[parameter1_start_val, parameter2_start_val, parameter3_start_val],
                      'end_value':[parameter1_end_val, parameter2_end_val, parameter3_end_val] }
    setting_values = pd.DataFrame( data = setting_values, index = ['parameter1', 'parameter2', 'parameter3'])
    setting_values['delta'] = (setting_values['end_value'] - setting_values['start_value'])/(s.grid_resolution-1)

    #print(setting_values)
    
    parameter_var_list_improved_val = {'parameter1': np.arange(setting_values.iloc[0,0], setting_values.iloc[0,1]+0.00000001, setting_values.iloc[0,2]),
                                       'parameter2': np.arange(setting_values.iloc[1,0], setting_values.iloc[1,1]+0.00000001, setting_values.iloc[1,2]),
                                       'parameter3': np.arange(setting_values.iloc[2,0], setting_values.iloc[2,1]+0.00000001, setting_values.iloc[2,2])}

    parameter_var_list_improved = pd.DataFrame()
    parameter_var_list_improved = pd.DataFrame(data=parameter_var_list_improved_val)

    #parameter_var_list_full is a list of every combination of the parameters
    parameter_var_list_full = pd.DataFrame()
    i1 = 0
    i2 = 0
    i3 = 0
    j = 0
    x = 0
    
    #fill parameter_var_list_full with parameters 1-3
    for i in range (0,s.grid_resolution**3):
        
        i1 = i1+1
        parameter_var_list_full.loc[i,0] = parameter_var_list_improved.iloc[i1-1,0]
        if i1 == s.grid_resolution:
            i1 = 0
            
        j = j+1
        parameter_var_list_full.loc[i,1] = parameter_var_list_improved.iloc[i2,1]
        if j == s.grid_resolution:
            j = 0
            i2 = i2+1
        if i2 == s.grid_resolution:
            i2 = 0
        
        x = x+1
        parameter_var_list_full.loc[i,2] = parameter_var_list_improved.iloc[i3,2]
        if x == s.grid_resolution**2:
            x = 0
            i3 = i3+1
        if i3 == s.grid_resolution:
            i3 = 0

    return parameter_var_list_full, parameter_var_list_improved


def improved_limits_single_parameter(metrics,parameter_var_list_full_old,parameter_var_list_sorted_old):
    """
    Function that calculates which parameter has the biggest influence on the results and calculates the improved limits only for this parameter.
    """
    
    parameter_var_list_full = pd.DataFrame()
    parameter_var_list_sorted = pd.DataFrame() 
    
    #find parameter with the highest influence only in the first usage of this function
    if s.x == 1: #verändern
        s.x = 0
        #find biggest deviation in NRMSD
        max_nrmsd=metrics["NRMSD_Population"].nlargest(s.grid_resolution**2)

        #find fitting parameter values to the biggest NRMSDs. With average, find parameter which has the biggest influence.
        parameter1 = 0
        parameter2 = 0
        parameter3 = 0
        
        for i in range (0,s.grid_resolution**2):
            
            parameter1 = parameter1 + parameter_var_list_full_old.iloc[int(max_nrmsd.index[i]),0]
            parameter2 = parameter2 + parameter_var_list_full_old.iloc[int(max_nrmsd.index[i]),1]
            parameter3 = parameter3 + parameter_var_list_full_old.iloc[int(max_nrmsd.index[i]),2]
        
        parameter1 = parameter1/(s.grid_resolution**2)
        parameter2 = parameter2/(s.grid_resolution**2)
        parameter3 = parameter3/(s.grid_resolution**2)
    
    
        if round(parameter1,6) == round(parameter_var_list_full_old.iloc[int(max_nrmsd.index[0]),0],6):
            s.parameter_hi = 0
            print("Parameter 1 has the highest influence")
        if round(parameter2,6) == round(parameter_var_list_full_old.iloc[int(max_nrmsd.index[0]),1],6):
            s.parameter_hi = 1
            print("Parameter 2 has the highest influence")
        if round(parameter3,6) == round(parameter_var_list_full_old.iloc[int(max_nrmsd.index[0]),2],6):
            s.parameter_hi = 2
            print("Parameter 3 has the highest influence")
        
    #find index of optimal combination
    NRMSD_index= int(metrics["NRMSD_Population"].idxmin())
    
    #define old
    parameter_start_val_old = round(parameter_var_list_sorted_old.iloc[0,s.parameter_hi],6)
    parameter_end_val_old = round(parameter_var_list_sorted_old.iloc[s.grid_resolution-1,s.parameter_hi],6)
    parameter_val = round(metrics.iloc[NRMSD_index-1,s.parameter_hi],6)
    
    for x in range (0,s.grid_resolution):
        if round(parameter_var_list_sorted_old.iloc[x,s.parameter_hi],6) == round(parameter_val,6):
            index_parameter = x
    
    if parameter_val == parameter_start_val_old and parameter_val != parameter_end_val_old:
        parameter_start_val = round(parameter_val-(((parameter_end_val_old-parameter_start_val_old)/(s.grid_resolution-1))*2),5)
        if parameter_start_val < 0:
            parameter_start_val = 0
        parameter_end_val = round(parameter_var_list_sorted_old.iloc[index_parameter+2,s.parameter_hi],6)
        
    if parameter_val == parameter_end_val_old and parameter_val != parameter_start_val_old:
        parameter_end_val = round(parameter_val+(((parameter_end_val_old-parameter_start_val_old)/(s.grid_resolution-1))*2),5)
        parameter_start_val = round(parameter_var_list_sorted_old.iloc[index_parameter-2,s.parameter_hi],6)
        
    if parameter_val != parameter_start_val_old and parameter_val != parameter_end_val_old:
        parameter_start_val = round(parameter_var_list_sorted_old.iloc[index_parameter-1,s.parameter_hi],6)
        parameter_end_val = round(parameter_var_list_sorted_old.iloc[index_parameter+1,s.parameter_hi],6)

    parameter_hi_var_list_improved_val = {'parameter': np.arange(parameter_start_val, parameter_end_val+0.00000001, (parameter_end_val - parameter_start_val)/(s.grid_resolution-1))}
    parameter_hi_var_list_improved = pd.DataFrame()
    parameter_hi_var_list_improved = pd.DataFrame(data=parameter_hi_var_list_improved_val)
    
    for x in range (0,s.grid_resolution):
        parameter_var_list_sorted_old.iloc[x,s.parameter_hi] = parameter_hi_var_list_improved.iloc[x,0]
    
    for x in range (0,s.grid_resolution):
        parameter_var_list_full.loc[x,0] = parameter_var_list_sorted_old.iloc[x,0]
        parameter_var_list_full.loc[x,1] = parameter_var_list_sorted_old.iloc[x,1]
        parameter_var_list_full.loc[x,2] = parameter_var_list_sorted_old.iloc[x,2]

        parameter_var_list_sorted.loc[x,0] = parameter_var_list_sorted_old.iloc[x,0]
        parameter_var_list_sorted.loc[x,1] = parameter_var_list_sorted_old.iloc[x,1]
        parameter_var_list_sorted.loc[x,2] = parameter_var_list_sorted_old.iloc[x,2]

    return parameter_var_list_full, parameter_var_list_sorted

def plot_results(df_results,empirical_data,metrics):
    """
    Function for plotting the model results and the empirical data
    """
    #create list for plotting function
    population_list = []
    for i in range(0,metrics.shape[0]):
        population_list.append("pop_" + str(i))
        
    df_results[population_list].plot(legend=0, color = ["b"], linewidth = 0.4)
    empirical_data["Population"].plot(legend=0, color = ["r"], linewidth = 1.5)
    
    plt.ylim([1e9,10e9])
    plt.xlim([0,122])
    plt.show()

def plot_empirical_data_and_pyworld_default(attribute,empirical_settings, empirical_data, df_results, i=0):
    """
    Function for comparing empeerical data to pyworld data with default parameters
    """
    years = np.arange(1900, 2023,1)

    fig, f1 = plt.subplots()
    f1.plot(years, df_results[s.empirical_settings.loc[attribute, 'pyworld_name_complete']+ "_" + str(i)], label=s.empirical_settings.loc[attribute, 'pyworld_name_complete'] + " ["+s.empirical_settings.loc[attribute, 'pyworld_unit'] + "]", color='blue')
    f1.plot(years, empirical_data[attribute], label= attribute + " ["+s.empirical_settings.loc[attribute, 'empirical_unit'] + "]", color='red')
    f1.set_title(s.empirical_settings.loc[attribute, 'title'])
    f1.set_xlabel('time in years')
    f1.legend()
    plt.show()

def plot_empirical_data_and_pyworld_default_multi_y(attribute,empirical_settings, empirical_data, df_results, i=0):
    """
    Function for comparing empeerical data to pyworld data with default parameters
    """
    years = np.arange(1900, 2023,1)

    fig, f1 = plt.subplots()
    f2 = f1.twinx()

    f1.plot(years, df_results[s.empirical_settings.loc[attribute, 'pyworld_name_complete']+ "_" + str(i)], label=s.empirical_settings.loc[attribute, 'pyworld_name_complete'] + " ["+s.empirical_settings.loc[attribute, 'pyworld_unit'] + "]", color='blue')
    f2.plot(years, empirical_data[attribute], label= attribute + " ["+s.empirical_settings.loc[attribute, 'empirical_unit'] + "]", color='red')
    f1.set_title(s.empirical_settings.loc[attribute, 'title'])
    f1.set_xlabel('time in years')
    f1.legend(loc=2);
    f2.legend(loc=6);
    

 
def plot_all_attributes():
    i = 0 #default values
    df_results = run_simulation()
    empirical_data = initialize_empirical_data()  # CSV Data to Dataframe 
    for plot_attribute in s.empirical_settings.index:
        if s.empirical_settings.loc[plot_attribute, '2_y_axis'] == False: 
            plot_empirical_data_and_pyworld_default(plot_attribute, s.empirical_settings, empirical_data, df_results)
        else:
            plot_empirical_data_and_pyworld_default_multi_y(plot_attribute, s.empirical_settings, empirical_data, df_results)
            

if __name__ == '__main__':
    plot_all_attributes()
    
    
    
    # testing run simulation
    #results = run_simulation(3, nri=3e12,pl=0.4, dcfsn=7)
    #print(results)
    # testing roc and d_value calculation
    """
    a = np.arange(10)
    b = np.arange(0, 20, 2)
    print(a, b)
    print(calculate_d_value(b, a))
    print(calculate_roc(b, a, 1, 5))

    # testing nrmsd
    a = np.arange(100)
    b = np.arange(0, 200, 2)
    print(calculate_nrmsd(b + 100, b, 1, 5, 50))

    empirical = initialize_empirical_data()
    model_sliced, empirical_sliced = prepare_data_for_metric_calc(empirical, empirical, s.pop_name)

    print(model_sliced, empirical_sliced)
    """
    
    #testing improved limits function
    '''s.grid_resolution = 3

    parameter_var_list_val = {'parameter1':[3, 4, 5],
                              'parameter2':[30, 40, 50],
                              'parameter3':[300, 400, 500],}
    
    parameter_var_list = pd.DataFrame(data=parameter_var_list_val, index = ['0', '1', '2'])
    print("Parameter_var_list:")
    print(parameter_var_list)
    '''
    '''
    metrics_val = {  'parameter1':[3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, ],
                     'parameter2':[30, 30, 30, 40, 40, 40, 50, 50, 50,30, 30, 30, 40, 40, 40, 50, 50, 50, 30, 30, 30, 40, 40, 40, 50, 50, 50],
                     'parameter3':[300, 300, 300, 300, 300, 300, 300, 300, 300, 400, 400, 400, 400, 400, 400, 400, 400, 400, 500, 500, 500, 500, 500, 500, 500, 500, 500],
                     'NRMSD[%]':[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]}

    metrics = pd.DataFrame(data=metrics_val, index = ['1', '2', '3', "4", "5", "6", "7", "8", "9", "10","11","12","13","14", "15","16","17", "18","19","20","21","22","23","24","25","26","27"])
    print("Simulation Metrics:")
    print(metrics)
    #parameter_var_list_improved = improved_limits(metrics,parameter_var_list)
    print("New Limits:")
    #print(parameter_var_list_improved)
    '''

