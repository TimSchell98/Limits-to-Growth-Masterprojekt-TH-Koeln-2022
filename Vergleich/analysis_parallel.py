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
    #run simulation
    world3 = World3(dt=s.sim_time_step, year_max=2022)
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
    #simulation_data['Deaths-p-y_{}'.format(i)] = world3.d
    #simulation_data['Births-p-y_{}'.format(i)] = world3.b
    #simulation_data['Food-p-c_{}'.format(i)] = world3.fpc
    #simulation_data['Ecologial-Footprint_{}'.format(i)] = world3.ef
    #simulation_data['Human-Welfare-Index_{}'.format(i)] = world3.hwi

    return simulation_data

if __name__ == '__main__':
    startTime = time.time()
    pool = mp.Pool(mp.cpu_count())
    run_parallel = True
    mp.freeze_support()

    #create parameter_var_list for this script
    parameter_var_list = s.parameter_var_list

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
    for j in range (0, s.grid_zoom+1):
        
        print('Number of simulations left = ' + str(s.grid_resolution**3+(s.grid_zoom-j)*s.grid_resolution**3))
        print('Estimated time left = ' + str(round(s.grid_resolution**3*0.71+(s.grid_zoom-j)*s.grid_resolution**3*0.45,2)) + ' seconds')
        
        if not run_parallel:
            for i in range(0, s.grid_resolution**3):
                # pool.map(run_simulation)
                # pool.close()
                run_simulation(i)
        else:
            print('Running in parallel mode')
            
            #run simulations and safe results
            df_results = pd.DataFrame()
            #results = pool.map(run_simulation, [i for i in range(0, s.grid_resolution**3)])
            results = [pool.apply(run_simulation, args=(i, parameter_var_list)) for i in range(0,s.grid_resolution**3)]
            
            for i in range(0, s.grid_resolution**3):
                df_results = pd.concat([df_results, results[i]], axis=1)
        
        print("df_results:")
        print(df_results)
        
    
        # - - - Metric calculation - -
        empirical_data = af.initialize_empirical_data()
        model_data, empirical_data_slice = af.prepare_data_for_metric_calc(df_results, empirical_data, s.pop_name)
        metrics = pd.DataFrame()

        for i in range(s.grid_resolution**3):
            metric_result = af.calculate_metrics(model_data['POP_{}'.format(i)], empirical_data_slice, str(i+1), 
                                                 'parameter1',parameter_var_list.iloc[i-s.grid_resolution*int(i/s.grid_resolution),0],
                                                 'parameter2',parameter_var_list.iloc[int((i-s.grid_resolution**2*int(i/s.grid_resolution**2))/s.grid_resolution),1],
                                                 'parameter3',parameter_var_list.iloc[int(i/s.grid_resolution**2),2])
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
        plt.show()
    
    #results = pool.map(af.calculate_metrics(model_data['AL_{}'.format(i)]))
   
    pool.close()
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(round(executionTime,2)))