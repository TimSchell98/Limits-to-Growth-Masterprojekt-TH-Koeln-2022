import numpy as np
import pandas as pd
import analysis_parallel_settings as s


def calculate_d_value(model_data, empirical_data):
    '''Function for the formula for delta value
    Originally from Herrington 2020 - Update to limits to growth
    \n inputs are two arrays with data
    Output is the calculated value different for the last timestep as specified in the paper
    '''
    d_value = (np.array(model_data)[-1] - np.array(empirical_data)[-1]) / np.array(empirical_data)[-1]
    return d_value


def calculate_roc(model_data, empirical_data, timestep: float, calculation_interval=5):
    ''' Function for the formula for the rate of change(roc)
    Originally from Herrington 2020 - Update to limits to growth
    \n inputs:
     two arrays with data
     the timestep between the data points in yrs
     calculation interval in yrs
    \n Output is the calculated roc for the last timestep and the year back the inteval rate
    '''
    stepwidth = calculation_interval * timestep
    model_data = np.array(model_data)
    empirical_data = np.array(empirical_data)
    roc = ((model_data[-1] - model_data[-stepwidth]) - (empirical_data[-1] - empirical_data[-stepwidth])) / (
                empirical_data[-1] - empirical_data[-stepwidth])
    return roc


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


def calculate_metrics(model_data, empirical_data, index=0, parameter1_name='none', parameter1_value=np.nan, parameter2_name='none', parameter2_value=np.nan, parameter3_name='none', parameter3_value=np.nan,
                      calculation_period=50):
    results = pd.DataFrame(index=[index])
    if not parameter1_name == 'none' or parameter2_name == 'none' or parameter3_name == 'none':
        results['{}'.format(parameter1_name)] = parameter1_value
        results['{}'.format(parameter2_name)] = parameter2_value
        results['{}'.format(parameter3_name)] = parameter3_value
    results['delta_value[%]'] = calculate_d_value(model_data, empirical_data)
    results['roc[%]'] = calculate_roc(model_data, empirical_data, timestep=s.sim_time_step,
                                      calculation_interval=s.calculation_interval)
    results['NRMSD[%]'] = calculate_nrmsd(model_data, empirical_data, timestep=s.sim_time_step,
                                          calculation_interval=s.calculation_interval,
                                          calculation_period=calculation_period)
    return results


def initialize_empirical_data():
    "Data - measured"
    measured_data = pd.read_csv('empirical_data.csv', sep=',')
    # measured_data = measured_data['data'].str.split(";", expand=True)
    measured_data = measured_data.iloc[:,0:10]
    # measured_data.columns=['Year', 'Population', 'Arable_Land', 'GFCF']
    empirical_data = measured_data.replace(0, np.nan)

    return empirical_data


def prepare_data_for_metric_calc(model_data: pd.DataFrame, empirical_data: pd.DataFrame, variable):
    start_row = s.empirical_settings.loc[variable, 'year_min'] * s.sim_time_step - 1900
    stop_row = s.empirical_settings.loc[variable, 'year_max'] * s.sim_time_step - 1900
    result_model = model_data[start_row:stop_row]
    result_empirical = empirical_data[variable][start_row:stop_row]
    return result_model, result_empirical

def improved_limits(metrics):
    """
    Find the combination at which the NRMSD is minimal.
    Cecks if parameter is boundary value, if yes calculate next value as new limit.
    Calculate new limits.
    """
    #set initial limits
    s.dcfsn_start_val = s.parameter_var_list.iloc[0,0]
    s.dcfsn_end_val = s.parameter_var_list.iloc[s.grid_resolution-1,0]
    s.iopcd_start_val = s.parameter_var_list.iloc[0,1]
    s.iopcd_end_val = s.parameter_var_list.iloc[s.grid_resolution-1,1]
    s.pl_start_val = s.parameter_var_list.iloc[0,2]
    s.pl_end_val = s.parameter_var_list.iloc[s.grid_resolution-1,2]
    
    #find index of optimal combination
    NRMSD_index= int(metrics["NRMSD[%]"].idxmin())
    
    #find optimal combination parameter values
    dcfsn_val = metrics.iloc[NRMSD_index-1,0]
    iopcd_val = metrics.iloc[NRMSD_index-1,1]
    pl_val = metrics.iloc[NRMSD_index-1,2]

    #find index of parameters, probably a better solution but not found
    for i in range (0,s.grid_resolution):
        if s.parameter_var_list.iloc[i,0] == dcfsn_val:
            index_dcfsn = i

    for i in range (0,s.grid_resolution):
        if s.parameter_var_list.iloc[i,1] == iopcd_val:
            index_iopcd = i

    for i in range (0,s.grid_resolution):
        if s.parameter_var_list.iloc[i,2] == pl_val:
            index_pl = i
            
    #check if parameter values are boundry values and set new limits
    if dcfsn_val == s.dcfsn_start_val and dcfsn_val != s.dcfsn_end_val:
        dcfsn_start_val = dcfsn_val-((s.dcfsn_end_val-s.dcfsn_start_val)/(s.grid_resolution-1))
        dcfsn_end_val = s.parameter_var_list.iloc[index_dcfsn+1,0]
        
    if dcfsn_val == s.dcfsn_end_val and dcfsn_val != s.dcfsn_start_val:
        dcfsn_end_val = dcfsn_val+((s.dcfsn_end_val-s.dcfsn_start_val)/(s.grid_resolution-1))
        dcfsn_start_val = s.parameter_var_list.iloc[index_dcfsn-1,0]
        
    if dcfsn_val != s.dcfsn_start_val and dcfsn_val != s.dcfsn_end_val:
        dcfsn_start_val = s.parameter_var_list.iloc[index_dcfsn-1,0]
        dcfsn_end_val = s.parameter_var_list.iloc[index_dcfsn+1,0]
    
    if iopcd_val == s.iopcd_start_val and iopcd_val != s.iopcd_end_val:
        iopcd_start_val = iopcd_val-((s.iopcd_end_val-s.iopcd_start_val)/(s.grid_resolution-1))
        iopcd_end_val = s.parameter_var_list.iloc[index_iopcd+1,1]
        
    if iopcd_val == s.iopcd_end_val and iopcd_val != s.iopcd_start_val:
        iopcd_end_val = iopcd_val+((s.iopcd_end_val-s.iopcd_start_val)/(s.grid_resolution-1))
        iopcd_start_val = s.parameter_var_list.iloc[index_iopcd-1,1]
        
    if iopcd_val != s.iopcd_start_val and iopcd_val != s.iopcd_end_val:
        iopcd_start_val = s.parameter_var_list.iloc[index_iopcd-1,1]
        iopcd_end_val = s.parameter_var_list.iloc[index_iopcd+1,1]
    
    if pl_val == s.pl_start_val and pl_val != s.pl_end_val:
        pl_start_val = pl_val-((s.pl_end_val-s.pl_start_val)/(s.grid_resolution-1))
        pl_end_val = s.parameter_var_list.iloc[index_pl+1,2]
        
    if pl_val == s.pl_end_val and pl_val != s.pl_start_val:
        pl_end_val = pl_val+((s.pl_end_val-s.pl_start_val)/(s.grid_resolution-1))
        pl_start_val = s.parameter_var_list.iloc[index_pl-1,2]
        
    if pl_val != s.pl_start_val and pl_val != s.pl_end_val:
        pl_start_val = s.parameter_var_list.iloc[index_pl-1,2]
        pl_end_val = s.parameter_var_list.iloc[index_pl+1,2]
    
    #calculate new parameter dataframe with steps
    setting_values = {'start_value':[dcfsn_start_val, iopcd_start_val, pl_start_val],
                      'end_value':[dcfsn_end_val, iopcd_end_val, pl_end_val] }
    setting_values = pd.DataFrame( data = setting_values, index = ['dcfsn', 'iopcd', 'pl'])
    setting_values['delta'] = (setting_values['end_value'] - setting_values['start_value'])/(s.grid_resolution-1)

    parameter_var_list_improved_val = {'dcfsn': np.arange(setting_values.iloc[0,0], setting_values.iloc[0,1]+0.000001, setting_values.iloc[0,2]), #wozu sind die +0.0001 nötig?
                          'iopcd': np.arange(setting_values.iloc[1,0], setting_values.iloc[1,1]+0.000001, setting_values.iloc[1,2]),
                          'pl': np.arange(setting_values.iloc[2,0], setting_values.iloc[2,1]+0.000001, setting_values.iloc[2,2])}

    parameter_var_list_improved = pd.DataFrame()
    parameter_var_list_improved = pd.DataFrame(data=parameter_var_list_improved_val)
    
    return parameter_var_list_improved

    
if __name__ == '__main__':
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
    s.grid_resolution = 3

    parameter_var_list_val = {'dcfsn':[3, 4, 5],
                              'iopcd':[30, 40, 50],
                              'pl':[300, 400, 500],}
    
    s.parameter_var_list = pd.DataFrame(data=parameter_var_list_val, index = ['0', '1', '2'])
    print("Parameter_var_list:")
    print(s.parameter_var_list)
    
    metrics_val = {  'dcfsn':[3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, ],
                     'iopcd':[30, 30, 30, 40, 40, 40, 50, 50, 50,30, 30, 30, 40, 40, 40, 50, 50, 50, 30, 30, 30, 40, 40, 40, 50, 50, 50],
                     'pl':[300, 300, 300, 300, 300, 300, 300, 300, 300, 400, 400, 400, 400, 400, 400, 400, 400, 400, 500, 500, 500, 500, 500, 500, 500, 500, 500],
                     'NRMSD[%]':[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]}

    metrics = pd.DataFrame(data=metrics_val, index = ['1', '2', '3', "4", "5", "6", "7", "8", "9", "10","11","12","13","14", "15","16","17", "18","19","20","21","22","23","24","25","26","27"])
    print("Simulation Metrics:")
    print(metrics)
    parameter_var_list_improved = improved_limits(metrics)
    print("New Limits:")
    print(parameter_var_list_improved)
