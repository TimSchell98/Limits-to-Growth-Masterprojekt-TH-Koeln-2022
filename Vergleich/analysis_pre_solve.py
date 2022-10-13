'''
Contains a function that can be called to pre-solve 1 parameter with 1 empirical dataset.
It specifies the number of runs the model should take.
'''

# - - - - -  Imports  - - - - -
from analysis_parallel import run_simulation
import multiprocessing as mp
import analysis_parallel_settings as s
import analysis_pre_solve_settings as ps
import analysis_functions as af
import pandas as pd
import numpy as np

def create_variation(default_value):
    start = default_value * (1-ps.search_range_from_default)
    stop = default_value * (1+ps.search_range_from_default)
    step = (stop-start) / ps.grid_resolution
    return np.linspace(start, stop, ps.grid_resolution)

def create_single_value_array(value):
    return np.full(ps.grid_resolution,value)

#def calculate_nrmsd(model_results, empirical_data):



def pre_solver(parameter_name, empirical_data_name):
    #parameter initialisation
    parameter_var_list = pd.DataFrame(columns=[s.parameter1_name, s.parameter2_name, s.parameter3_name])
    if parameter_name == s.parameter1_name:
        default_value = s.parameter1_default
        parameter_var_list[s.parameter1_name] = create_variation(default_value)
        parameter_var_list[s.parameter2_name] = create_single_value_array(s.parameter2_default)
        parameter_var_list[s.parameter3_name] = create_single_value_array(s.parameter3_default)
    elif parameter_name == s.parameter2_name:
        default_value = s.parameter2_default
        parameter_var_list[s.parameter1_name] = create_single_value_array(s.parameter1_default)
        parameter_var_list[s.parameter2_name] = create_variation(s.parameter2_default)
        parameter_var_list[s.parameter3_name] = create_single_value_array(s.parameter3_default)
    elif parameter_name == s.parameter3_name:
        default_value = s.parameter3_default
        parameter_var_list[s.parameter1_name] = create_single_value_array(s.parameter1_default)
        parameter_var_list[s.parameter2_name] = create_single_value_array(s.parameter2_default)
        parameter_var_list[s.parameter3_name] = create_variation(s.parameter3_default)
    else:
        print('No Settings found for Parameter: {}'.format(parameter_name))

    if ps.print_debug_messages:
        print('Parameter Variation List:\n', parameter_var_list)

    pool = mp.Pool(mp.cpu_count())
    mp.freeze_support()
    df_results = pd.DataFrame()
    results = [pool.apply_async(run_simulation, args=(i, parameter_var_list)) for i in range(0, ps.grid_resolution)]
    for i in results:
        i.wait()

    for i in range(0, ps.grid_resolution):
        df_results = pd.concat([df_results, results[i].get()], axis=1)

    if ps.print_debug_messages:
        print('Simulation results:\n', df_results)

    # - - - Metric calculation - - -
    empirical_data = af.initialize_empirical_data()  # CSV Data to Dataframe
    metrics = pd.DataFrame()                         # Dataframe for results - metrics

    model_data, empirical_data_slice = af.prepare_data_for_metric_calc(df_results, empirical_data, empirical_data_name)
    print(empirical_data_slice)

    for i in range(ps.grid_resolution):
        metric_result = af.calculate_metrics(model_data['{}_{}'.format(ps.name_dict_empirical_model[empirical_data_name], i)], empirical_data_slice, str(i+1), parameter_name,
                                             parameter_var_list[parameter_name][i])
        metrics = pd.concat([metrics, metric_result])

    if ps.print_debug_messages:
        print('NRMSD results: \n', metrics)

    index_of_minimum_nrmsd = metrics['NRMSD[%]'].idxmin()

    print('Minimum NRMSD for {}={} with the {} empirical data\nDefault value for {} is {}'.format(parameter_name, round(metrics[parameter_name][index_of_minimum_nrmsd], 5), empirical_data_name, parameter_name, default_value))

    return metrics[parameter_name][index_of_minimum_nrmsd]



'''Code for Script Testing'''
if __name__ == '__main__':
    test_parameter_name = 'dcfsn'
    test_empirical_data_name = 'Arable_land'
    pre_solver(test_parameter_name, test_empirical_data_name)
    #   print(create_variation(3))
    #   print()

