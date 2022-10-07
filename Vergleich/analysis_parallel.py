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

if s.use_update == True:
    from PyWorld3_Update.pyworld3 import World3
if s.use_update == False:
    from pyworld3 import World3

# - - - - - - Function definitions - -

def run_simulation(i, parameter_var_list):

    #run simulation
    world3 = World3(dt=s.sim_time_step, year_max=s.year_max)
    world3.init_world3_constants(dcfsn = parameter_var_list.iloc[i,0],
                                 frpm = parameter_var_list.iloc[i,1],
                                 pl = parameter_var_list.iloc[i,2])
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
    #print('Ending Simulation {}'.format(i))
    
    return simulation_data

    return simulation_data

if __name__ == '__main__':
    startTime = time.time()
    pool = mp.Pool(mp.cpu_count())
    mp.freeze_support()
    end_simulation = False
     
    #should analysis stopp at grid resolution or NRMSD accuracy
    if s.zoom_limit == True:
        j = 100 #if NRMSD accuracy isnt reached in 100 zooms, analysis will end
    if s.zoom_limit == False:
        j = s.grid_zoom
    
    #create parameter_var_list for this script
    parameter_var_list, parameter_var_list_sorted = s.parameter_init()
        
    
    # - - - Run Simulation - - -
    
    while end_simulation == False:
        j=j-1
        if s.zoom_limit == False:
            print('Number of simulations left = ' + str((j+2)*(s.grid_resolution**3)))
            
            if s.run_parallel == True:
                print('Estimated time left = ' + str(round((j+2) * s.grid_resolution**3 * 0.35, 2)) + ' seconds')
            if s.run_parallel == False:
                print('Estimated time left = ' + str(round((j+2) * s.grid_resolution**3 * 1.21, 2)) + ' seconds')
            
        if s.zoom_limit == True:
            print('Number of simulations completed = ' + str((100-j+1)*s.grid_resolution**3))
        
        if s.run_parallel == False:
            print('Running in not-parallel mode')
            
            #run simulations and safe results
            results = pd.DataFrame()
            df_results = pd.DataFrame()
            for i in range(0, s.grid_resolution**3):
                results = run_simulation(i, parameter_var_list)
                df_results = pd.concat([df_results, results], axis=1)
            
        if s.run_parallel == True:
            print('Running in parallel mode')
            
            #run simulations and safe results
            df_results = pd.DataFrame()
            results = [pool.apply_async(run_simulation, args=(i, parameter_var_list)) for i in range(0, s.grid_resolution**3)]
            for i in results:
                i.wait()

            for i in range(0, s.grid_resolution**3):
                df_results = pd.concat([df_results, results[i].get()], axis=1)
    
    
        # - - - Metric calculation - -
        empirical_data = af.initialize_empirical_data()  # CSV Data to Dataframe 
        metrics = pd.DataFrame()                         # Dataframe for results - metrics

        for i in range(s.grid_resolution**3):            # calculate NRMSD for all parameter possibilities and attributes
            metric_result = af.calculate_metrics_multiple_attributes(df_results, empirical_data, str(i+1), 
                                                 'parameter1',parameter_var_list.iloc[i-s.grid_resolution*int(i/s.grid_resolution),0],
                                                 'parameter2',parameter_var_list.iloc[int((i-s.grid_resolution**2*int(i/s.grid_resolution**2))/s.grid_resolution),1],
                                                 'parameter3',parameter_var_list.iloc[int(i/s.grid_resolution**2),2],i)
            metrics = pd.concat([metrics, metric_result])

        #print resolutions
        print("df_results:")
        print(df_results) 

        print("Metrics:")
        print(metrics)
        
        #end simulation when nrmsd reaches defined accuracy, or if grid_zoom reaches limits
        if s.zoom_limit == True:
            if round(metrics.iloc[(int(metrics["NRMSD_total"].idxmin()))-1,5],4) <= s.result_accuracy or j < 0:
                end_simulation = True

        if s.zoom_limit == False and j < 0:
            end_simulation = True
        
        #Improved limits
        #todo: funktion einfügen die zuerst den parameter mit dem höchsten einfluss analysiert und verbessert, bevor die anderen parameter hinzugefügt werden
        parameter_var_list, parameter_var_list_sorted=af.improved_limits(metrics,parameter_var_list, parameter_var_list_sorted)
        af.new_limits(metrics,parameter_var_list)
        
        #plot resolution
        af.plot_results(df_results,empirical_data, metrics)
   
    #end simulation and print final results 
    pool.close()
    print("Final Results:")
    print("Parameter 1: ", end="")
    print(round(parameter_var_list.iloc[int(s.grid_resolution/2),0],4))
    print("Parameter 2: ", end= "")
    print(round(parameter_var_list.iloc[int(s.grid_resolution/2),1],4))
    print("Parameter 3: ", end= "")
    print(round(parameter_var_list.iloc[int(s.grid_resolution/2),2],4))
    
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(round(executionTime,2)))