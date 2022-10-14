# - - - - Imports - - - - - -
import multiprocessing as mp
import numpy as np
from numpy import diff
import pandas as pd
import analysis_functions as af
import analysis_parallel_settings as s
import matplotlib.pyplot as plt
import time
import sys
startTime = time.time()
# - - -  World 3 import and Version Switching

if s.use_update == True:
    sys.path.append('..')
    from PyWorld3_Update.pyworld3 import World3
if s.use_update == False:
    sys.path.append('..')
    from PyWorld3_Old.pyworld3 import World3

# - - - - - - Function definitions - -

def run_simulation(i, parameter_var_list_full):

    #run simulation
    world3 = World3(dt=s.sim_time_step, year_max=s.year_max)
    world3.init_world3_constants(dcfsn = parameter_var_list_full.iloc[i,0],
                                 frpm = parameter_var_list_full.iloc[i,1],
                                 pl = parameter_var_list_full.iloc[i,2])
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
    #simulation_data['POLC_GR_{}'.format(i)] = np.append((diff(world3.ppol)/s.sim_time_step),np.nan) #Pollution groth rate / derivation 
    #simulation_data['Ecologial-Footprint_{}'.format(i)] = world3.ef
    #simulation_data['Human-Welfare-Index_{}'.format(i)] = world3.hwi
    #print('Ending Simulation {}'.format(i))

    return simulation_data

if __name__ == '__main__':
    startTime = time.time()
    pool = mp.Pool(mp.cpu_count())
    mp.freeze_support()
    end_simulation = False
     
    #should analysis stopp at grid resolution or NRMSD accuracy
    if s.zoom_limit == True:
        j = 25 #if NRMSD accuracy isnt reached in 25 zooms, analysis will end
    if s.zoom_limit == False:
        j = s.grid_zoom + s.single_parameter_zoom
    
    #create parameter_var_list for this script
    parameter_var_list_full, parameter_var_list_sorted = s.parameter_init()

    
    # - - - Run Simulation - - -
    
    while end_simulation == False:
        
        #define sim_number as the lenght of parameter_var_list_full
        sim_number = parameter_var_list_full.shape[0]
        
        
        if s.zoom_limit == False:
            print('Number of simulations left = ' + str((j+2)*(s.grid_resolution**3)))
            
            if s.run_parallel == True:
                print('Estimated time left = ' + str(round((j+2) * s.grid_resolution**3 * 0.35, 2)) + ' seconds')
            if s.run_parallel == False:
                print('Estimated time left = ' + str(round((j+2) * s.grid_resolution**3 * 1.21, 2)) + ' seconds')
            
        if s.zoom_limit == True:
            print('Number of simulations completed = ' + str((25-j)*s.grid_resolution**3))
        
        if s.run_parallel == False:
            print('Running in not-parallel mode')
            
            
            # - - - Run Simulation - - -
            results = pd.DataFrame()
            df_results = pd.DataFrame()
            for i in range(0, sim_number):
                results = run_simulation(i, parameter_var_list_full)
                df_results = pd.concat([df_results, results], axis=1)
            
        if s.run_parallel == True:
            print('Running in parallel mode')
            
            df_results = pd.DataFrame()
            results = [pool.apply_async(run_simulation, args=(i, parameter_var_list_full)) for i in range(0, sim_number)]
            for i in results:
                i.wait()

            for i in range(0, sim_number):
                df_results = pd.concat([df_results, results[i].get()], axis=1)
    
    
        # - - - Metric calculation - - -
        empirical_data = af.initialize_empirical_data()  # CSV Data to Dataframe 
        metrics = pd.DataFrame()                         # Dataframe for results - metrics

        for i in range(0, sim_number):            # calculate NRMSD for all parameter possibilities and attributes
            metric_result = af.calculate_metrics_multiple_attributes(df_results, empirical_data, str(i+1), 
                                                 'parameter1',parameter_var_list_full.iloc[i,0],
                                                 'parameter2',parameter_var_list_full.iloc[i,1],
                                                 'parameter3',parameter_var_list_full.iloc[i,2])
            metrics = pd.concat([metrics, metric_result])
        
        #print resolutions
        print("df_results:")
        print(df_results) 

        print("Metrics:")
        print(metrics)
        
        #print minimal NRMSD
        print("Minimal NRMSD_Population:")
        print(round(metrics["NRMSD_Population"].min(),4))
        
        # - - - Improve limits - - -
        print("Old limits:")
        print(parameter_var_list_sorted)
        #for the first number of simulations (defined by "single_parameter_zoom") only the parameter with the highest influence will be improved
        if s.zoom_limit == True and 25-j < s.single_parameter_zoom:
            #print("Improve only one parameter")
            parameter_var_list_full, parameter_var_list_sorted = af.improved_limits_single_parameter(metrics,parameter_var_list_full, parameter_var_list_sorted)
        if s.zoom_limit == True and 25-j >= s.single_parameter_zoom:
            #print("Improve all parameters")
            parameter_var_list_full, parameter_var_list_sorted = af.improved_limits_all_parameter(metrics,parameter_var_list_full, parameter_var_list_sorted)
        if s.zoom_limit == False and s.grid_zoom+s.single_parameter_zoom-j < s.single_parameter_zoom:
            #print("Improve only one parameter")
            parameter_var_list_full, parameter_var_list_sorted = af.improved_limits_single_parameter(metrics,parameter_var_list_full, parameter_var_list_sorted)          
        if s.zoom_limit == False and s.grid_zoom + s.single_parameter_zoom - j >= s.single_parameter_zoom:
            #print("Improve all parameters")
            parameter_var_list_full, parameter_var_list_sorted = af.improved_limits_all_parameter(metrics,parameter_var_list_full, parameter_var_list_sorted)
        
        print("Improved limits:")
        print(parameter_var_list_sorted)
        
        # - - - plot results - - - 
        af.plot_results(df_results,empirical_data, metrics)
    
        #end simulation when nrmsd reaches defined accuracy, or if grid_zoom reaches limits, or delta is smaller or equal to 0.000001
        if s.zoom_limit == True:
            if round(parameter_var_list_sorted.iloc[1,0]-parameter_var_list_sorted.iloc[0,0],6) <= s.delta_end and round(parameter_var_list_sorted.iloc[1,1]-parameter_var_list_sorted.iloc[0,1],6) <= s.delta_end and round(parameter_var_list_sorted.iloc[1,2]-parameter_var_list_sorted.iloc[0,2],6) <= s.delta_end:
                end_simulation = True
            if round(metrics["NRMSD_Population"].min(),4) <= s.result_accuracy or j < 0:
                end_simulation = True
            
        if s.zoom_limit == False and j <= 0:
            end_simulation = True
        
        j=j-1
        
    #end simulation and print final results 
    pool.close()
    print("Final Results:")
    print("NRMSD min:")
    print(round(metrics["NRMSD_Population"].min(),4))
    print("Parameter 1: ", end="")
    print(round(parameter_var_list_sorted.iloc[int(s.grid_resolution/2),0],4))
    print(round(parameter_var_list_full.iloc[int(metrics["NRMSD_Population"].idxmin()),0],4))
    print("Parameter 2: ", end= "")
    print(round(parameter_var_list_sorted.iloc[int(s.grid_resolution/2),1],4))
    print(round(parameter_var_list_full.iloc[int(metrics["NRMSD_Population"].idxmin()),1],4))
    print("Parameter 3: ", end= "")
    print(round(parameter_var_list_sorted.iloc[int(s.grid_resolution/2),2],4))
    print(round(parameter_var_list_full.iloc[int(metrics["NRMSD_Population"].idxmin()),2],4))
    
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(round(executionTime,2)))