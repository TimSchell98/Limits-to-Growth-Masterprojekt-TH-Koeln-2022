# - - - - Imports - - - - - -
import multiprocessing as mp
import numpy as np
import pandas as pd
import analysis_functions as af
import analysis_parallel_settings as s
import matplotlib.pyplot as plt
import time
startTime = time.time()
# - - -  World 3 import and Version Switching
use_update = False
if use_update:
    from PyWorld3_Update.pyworld3 import World3
else:
    from pyworld3 import World3

# - - - - - - Function definitions - -

def run_simulation(i, parameter_var_list):
    print('Starting Simulation {}'.format(i))
    #run simulation
    world3 = World3(dt=s.sim_time_step, year_max=s.year_max)
    world3.init_world3_constants(dcfsn = parameter_var_list.iloc[i-s.grid_resolution*int(i/s.grid_resolution),0],
                                 frpm = parameter_var_list.iloc[int((i-s.grid_resolution**2*int(i/s.grid_resolution**2))/s.grid_resolution),1],
                                 pl = parameter_var_list.iloc[int(i/s.grid_resolution**2),2])
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)
    
    #gather simulation data
    simulation_data = pd.DataFrame()
    simulation_data['POP_{}'.format(i)] = world3.pop
    simulation_data['AL_{}'.format(i)] = world3.al
    simulation_data['CDR_{}'.format(i)] = world3.cdr
    simulation_data['CBR_{}'.format(i)] = world3.cbr
    simulation_data['IO_{}'.format(i)] = world3.io
    simulation_data['FPC_{}'.format(i)] = world3.fpc
    simulation_data['POLC_{}'.format(i)] = world3.ppol
    #simulation_data['Ecologial-Footprint_{}'.format(i)] = world3.ef
    #simulation_data['Human-Welfare-Index_{}'.format(i)] = world3.hwi
    print('Ending Simulation {}'.format(i))
    return simulation_data

if __name__ == '__main__':
    startTime = time.time()
    pool = mp.Pool(mp.cpu_count())
    run_parallel = True
    mp.freeze_support()

    #create parameter_var_list for this script
    parameter_var_list = s.parameter_init()

    print("Starting limits:")
    print(parameter_var_list)
    print("Parameter1 = " + s.parameter1_name)
    print("Parameter2 = " + s.parameter2_name)
    print("Parameter3 = " + s.parameter3_name)
    
    #create list for plotting
    population_list = []
    for i in range(0,s.grid_resolution**3):
        population_list.append("POP_" + str(i))
        
    # - - - Run Simulation - - -
    for j in range(0, s.grid_zoom+1):
        print('Number of simulations left = ' + str(s.grid_resolution**3+(s.grid_zoom-j)*s.grid_resolution**3))

        if not run_parallel:
            print('Estimated time left = ' + str(round(s.grid_resolution**3*1.24+(s.grid_zoom-j)*s.grid_resolution**3*1.24,2)) + ' seconds')
            print('Running in not-parallel mode')
            
            results = pd.DataFrame()
            df_results = pd.DataFrame()
            for i in range(0, s.grid_resolution**3):
                results = run_simulation(i, parameter_var_list)
                df_results = pd.concat([df_results, results], axis=1)
            
        else:
            print('Estimated time left = ' + str(round(s.grid_resolution**3*0.71+(s.grid_zoom-j)*s.grid_resolution**3*0.45, 2)) + ' seconds')
            print('Running in parallel mode')
            
            #run simulations and safe results
            df_results = pd.DataFrame()
            #results = pool.map(run_simulation, [i for i in range(0, s.grid_resolution**3)])
            results = [pool.apply_async(run_simulation, args=(i, parameter_var_list)) for i in range(0, s.grid_resolution**3)]
            for i in results:
                i.wait()

            for i in range(0, s.grid_resolution**3):
                df_results = pd.concat([df_results, results[i].get()], axis=1)
        
        print("df_results:")
        print(df_results)        
    
        # - - - Metric calculation - -
        empirical_data = af.initialize_empirical_data()
        metrics = pd.DataFrame() 
        model_data, empirical_data_slice = af.prepare_data_for_metric_calc(df_results, empirical_data, s.pop_name) # for single attribute 

        for i in range(s.grid_resolution**3):
            metric_result = af.calculate_metrics_multiple_attributes(df_results, empirical_data, str(i+1), 
                                                 'parameter1',parameter_var_list.iloc[i-s.grid_resolution*int(i/s.grid_resolution),0],
                                                 'parameter2',parameter_var_list.iloc[int((i-s.grid_resolution**2*int(i/s.grid_resolution**2))/s.grid_resolution),1],
                                                 'parameter3',parameter_var_list.iloc[int(i/s.grid_resolution**2),2],i)
            metrics = pd.concat([metrics, metric_result])

        #Improved limits
        print("Metrics:")
        print(metrics)
        print("Parameter1 = " + s.parameter1_name)
        print("Parameter2 = " + s.parameter2_name)
        print("Parameter3 = " + s.parameter3_name)
        print("Old limits:")
        print(parameter_var_list)
        parameter_var_list=af.improved_limits(metrics,parameter_var_list)
        print("Improved limits:")
        print(parameter_var_list)
        
        #plot resolution
        #df_results.plot(legend=0)
        df_results[population_list].plot(legend=0, color = ["b"], linewidth = 0.5)
        empirical_data["Population"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.ylim([1e9,10e9])
        plt.show()

    #results = pool.map(af.calculate_metrics_single_attribute(model_data['AL_{}'.format(i)]))
   
    pool.close()
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(round(executionTime,2)))