import numpy as np
import pandas as pd
import analysis_parallel_settings as s
from scipy.signal import savgol_filter
from scipy import signal
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from PyWorld3_Update.pyworld3 import World3


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
    parameter_list = pd.read_excel('Parameters_to_be_analysed.xlsx')
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

    parameter_list_steps = pd.DataFrame(index = np.arange(s.grid_resolution))
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
    
def improved_limits(metrics, parameter_list, parameter_list_full):
    #Find NRMSD index of line which has the minimal NRMSD.
    NRMSD_index = int(metrics[s.variable_to_improve].idxmin())-1 #-1, because metrics dataframe starts at index 1, parameter_list_starts at 0

    #Temporary version of parameter_history
    parameter_history_temp = pd.DataFrame(columns = ["changed parameter", "previous value", "next value", "NRMSD_min", "location", "relative change"], index = [0])
    
    #save min NRMSD in dataframe
    parameter_history_temp["NRMSD_min"] = round(metrics[s.variable_to_improve].min(),10)
            
    #calculate index of parameter which is to be improved       
    parameter_index = int(NRMSD_index/s.grid_resolution)
    #save improved parameter name, new and old value
    parameter_history_temp.iloc[0,0] = parameter_list.iloc[parameter_index,0]
    parameter_history_temp.iloc[0,1] = parameter_list.iloc[parameter_index,2]
    parameter_history_temp.iloc[0,2] = parameter_list_full.iloc[NRMSD_index,parameter_index]
    #save improved value in parameter_list
    parameter_list.iloc[parameter_index,2] = parameter_list_full.iloc[NRMSD_index,parameter_index]
    
    #check if optimal value is last of first value
    if NRMSD_index < s.grid_resolution*parameter_list.shape[0]-1 and NRMSD_index > 0:
        #if best parameter value is not an edge value, use previous value and next value as new start and end values
        if parameter_list_full.iloc[NRMSD_index-1,parameter_index] < parameter_list_full.iloc[NRMSD_index, parameter_index] and parameter_list_full.iloc[NRMSD_index+1,parameter_index] > parameter_list_full.iloc[NRMSD_index,parameter_index]:
            #print("Was mid value")
            parameter_history_temp.iloc[0,4] = "mid-value"
            parameter_list.iloc[parameter_index,4] = parameter_list_full.iloc[NRMSD_index-1,parameter_index]
            parameter_list.iloc[parameter_index,5] = parameter_list_full.iloc[NRMSD_index+1,parameter_index]
        #check if best parameter value is edge value, if yes then move start or end value by given amount
        #check if best parameter is first value
        if parameter_list_full.iloc[NRMSD_index-1,parameter_index] > parameter_list_full.iloc[NRMSD_index,parameter_index] or NRMSD_index <= 0:
            #print("Was start value")
            parameter_history_temp.iloc[0,4] = "start-value"
            parameter_list.iloc[parameter_index,4] = round(parameter_list.iloc[parameter_index,4]*(1-s.parameter_move_start_end_value),6) 
            parameter_list.iloc[parameter_index,5] = parameter_list_full.iloc[NRMSD_index+1,parameter_index]
        #check if best parameter is last value
        if parameter_list_full.iloc[NRMSD_index+1,parameter_index] < parameter_list_full.iloc[NRMSD_index,parameter_index] or NRMSD_index >= s.grid_resolution*parameter_list.shape[0]-1:
            #print("Was end value")
            parameter_history_temp.iloc[0,4] = "end-value"
            parameter_list.iloc[parameter_index,4] = parameter_list_full.iloc[NRMSD_index-1,parameter_index]
            parameter_list.iloc[parameter_index,5] = round(parameter_list.iloc[parameter_index,4]*(1+s.parameter_move_start_end_value),6) 
    
    return parameter_list, parameter_history_temp

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

    nrmsd = (np.sqrt(nominator_single_values.sum() / calculation_interval+1)) / (denominator_single_values.sum() / calculation_interval+1)
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
                                              calculation_interval=s.calculation_interval, calculation_period=s.empirical_settings['period'].iloc[i])

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


def calculate_metrics(model_data, empirical_data, index=0, parameter_name='none', parameter_value=np.nan,
                      calculation_period=50):
    results = pd.DataFrame(index=[index])
    if not parameter_name == 'none':
        results['{}'.format(parameter_name)] = parameter_value
    results['NRMSD[%]'] = calculate_nrmsd(model_data, empirical_data, timestep=s.sim_time_step, calculation_interval=s.calculation_interval, calculation_period=calculation_period)
    return results


def initialize_empirical_data():
    "Data - measured"
    measured_data = pd.read_csv('empirical_data.csv', sep=',')
    # measured_data = measured_data['data'].str.split(";", expand=True)
    measured_data = measured_data.iloc[:,0:22]
    # measured_data.columns=['Year', 'Population', 'Arable_Land', 'GFCF']
    empirical_data = measured_data.replace(0, np.nan)
    empirical_data.iloc[66,9] = 0
    # filter settings 

    for attribute_name in s.empirical_settings.index:
        if s.empirical_settings.loc[attribute_name,'smooth'] == False:
            empirical_data[attribute_name] = empirical_data[attribute_name]
        else:
            empirical_data.iloc[s.empirical_settings.loc[attribute_name,'year_min']-1900:s.empirical_settings.loc[attribute_name,'year_max']-1900,empirical_data.columns.get_loc(attribute_name)]  = smooth(empirical_data.iloc[s.empirical_settings.loc[attribute_name,'year_min']-1900:s.empirical_settings.loc[attribute_name,'year_max']-1900,empirical_data.columns.get_loc(attribute_name)], s.empirical_settings.loc[attribute_name,'smooth'])
    
    return empirical_data

def smooth(empirical_data, critical_freq):
    b, a = signal.ellip(6, 0.01, 120, critical_freq)  # Filter to be applied
    #good: 6, 0.1, 12, 0.3
        # (order, rp (min allowed ripple(dB), rp (max allowed ripple(dB)), critical frequency))
    empirical_data = signal.filtfilt(b, a, empirical_data, method="gust")

    
    return empirical_data


if __name__ == '__main__':


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

