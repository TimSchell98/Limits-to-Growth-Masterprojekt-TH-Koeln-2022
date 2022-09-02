import numpy as np
import pandas as pd
import analysis_parallel_settings as s
def calculate_d_value(model_data, empirical_data):
    '''Function for the formula for delta value
    Originally from Herrington 2020 - Update to limits to growth
    \n inputs are two arrays with data
    Output is the calculated value different for the last timestep as specified in the paper
    '''
    d_value = (np.array(model_data)[-1]-np.array(empirical_data)[-1])/np.array(empirical_data)[-1]
    return d_value

def calculate_roc(model_data, empirical_data, timestep:float, calculation_interval = 5):
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
    roc = ((model_data[-1]-model_data[-stepwidth])-(empirical_data[-1]-empirical_data[-stepwidth]))/(empirical_data[-1]-empirical_data[-stepwidth])
    return roc

def calculate_nrmsd(model_data, empirical_data, timestep:float , calculation_interval=5, calculation_period=50):
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
        nominator_single_values[-i-1]=np.square(model_data[-i*stepwidth-1]-empirical_data[-i*stepwidth-1])
        denominator_single_values[-i-1] = empirical_data[-i*stepwidth-1]

    nrmsd = (np.sqrt(nominator_single_values.sum()/6)) / (denominator_single_values.sum()/6)
    return nrmsd

def calculate_metrics(model_data, empirical_data, row_name='default', calculation_period = 50):
    results = pd.DataFrame(index=[row_name])
    results['delta_value[%]'] = calculate_d_value(model_data,empirical_data)
    results['roc[%]'] = calculate_roc(model_data, empirical_data, timestep=s.sim_time_step, calculation_interval=s.calculation_interval)
    results['NRMSD[%]'] = calculate_nrmsd(model_data, empirical_data, timestep=s.sim_time_step, calculation_interval=s.calculation_interval, calculation_period=calculation_period)
    return results

def initialize_empirical_data():
    "Data - measured"
    measured_data = pd.read_csv('emperical_data.csv', names= ['data'])
    measured_data = measured_data['data'].str.split(";", expand=True)
    measured_data = measured_data.iloc[:,0:4]
    measured_data.columns=['Year', 'Population', 'Arable_Land', 'GFCF']
    empirical_data = measured_data.replace(0, np.nan)

    return empirical_data

def prepare_data_for_metric_calc(model_data:pd.DataFrame, empirical_data:pd.DataFrame, variable):

    start_row = s.empirical_settings.loc[variable, 'year_min']*s.sim_time_step-1900
    stop_row = s.empirical_settings.loc[variable, 'year_max']*s.sim_time_step-1900
    result_model = model_data[start_row:stop_row]
    result_empirical = empirical_data[variable][start_row:stop_row]
    return result_model, result_empirical


if __name__=='__main__':
    #testing roc and d_value caclulation
    a = np.arange(10)
    b = np.arange(0, 20, 2)
    print(a,b)
    print(calculate_d_value(b, a))
    print(calculate_roc(b, a, 1, 5))

    # testing nrmsd
    a = np.arange(100)
    b = np.arange(0, 200, 2)
    print(calculate_nrmsd(b+100,b,1,5,50))

    empirical = initialize_empirical_data()
    model_sliced, empirical_sliced = prepare_data_for_metric_calc(empirical, empirical, s.pop_name)

    print(model_sliced, empirical_sliced)