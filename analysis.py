# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import multiprocessing as mp
import analysis_parallel_settings_working as s
import analysis_functions_working as af
from analysis_plotting import plot_data
import matplotlib.pyplot as plt
import time
from datetime import datetime
from PyWorld3_Update.pyworld3 import World3
startTime = time.time()


def parameter_to_simulation(i, parameter_list_full, year_max):
    parameter_dict = {}
    #parameter_list_full.columns[column_index][0]
    for column_index, column_name in enumerate(parameter_list_full.columns):
        parameter_dict[column_name[0]] = parameter_list_full[column_name[0]].iloc[i].item()
        #print(parameter_dict[column_name[0]])
    return af.run_simulation_kwargs(year_max, i, **parameter_dict)

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    mp.freeze_support()

    #   -   -   - create dataframe of all variables with steps, empirical data and parameter history -   -   -
    #create base list of parameter to be analysed
    parameter_list=af.init_parameter_list()
    #create list of every combination of parameters
    parameter_list_full = af.parameter_list_full(parameter_list)
    #initialize empirical data
    empirical_data = af.initialize_empirical_data()
    #DataFrame in which in every step the change is being saved
    parameter_history = pd.DataFrame(columns = ["changed parameter", "previous value", "next value", "NRMSD_min", "location", "relative change"])

    #   -   -   - run analysis -   -   -
    no_of_simulations = len(parameter_list_full)
    analysis_number = 0
    stop_condition = True
    #delta_NRMSD will be calculated in the third run, so it has to be predefined
    delta_nrmsd = 1
    
    print('Number of simulations in one zoom = ' + str(len(parameter_list_full)))
    print('Estimated time for one zoom = ' + str(round(len(parameter_list_full)*0.51)) + ' seconds')
    print('Estimated time till end conditions are met = ' + str(round(len(parameter_list_full)*0.51 * s.analysis_number_end_condition)) + ' seconds')

    #start of analysis loop, stops of stop conditions are reached
    while stop_condition == True:
        analysis_number = analysis_number + 1
    
        print('\nNumber of zooms completed = ' + str(analysis_number-1))
        print('Number of simulations completed = ' + str(len(parameter_list_full) * (analysis_number-1)))
        
        #run simulation
        df_results = pd.DataFrame()
        #results = [pool.apply_async(af.run_simulation_combinations, args=(i, parameter_list_full)) for i in range(0, parameter_list_full.shape[0])]
        results = [pool.apply_async(parameter_to_simulation, args=(i, parameter_list_full, s.year_max)) for i in range(0, no_of_simulations)]
        
        for i in results:
            i.wait()
        
        for i in range(0, no_of_simulations):
            df_results = pd.concat([df_results, results[i].get()], axis=1) #hier entsteht ein error wenn eine bestimmte anzahl an zu analysierenden parameten überschritten wird.
        print(df_results)
        
        #   -   -   - Metrics calculation -   -   -

        metrics = pd.DataFrame()

        for i in range(0, no_of_simulations):
            metric_result = af.calculate_metrics_multiple_attributes(df_results, empirical_data, str(i+1))
            metrics = pd.concat([metrics, metric_result])
            
        #   -   -   - Plot data -   -   -
        if s.plot_results == True:        
            plot_data(df_results, empirical_data, parameter_list_full)
    
        #   -   -   - Calculate next parameter_list_full and save values in list -   -   -
        print(str(s.variable_to_improve) + " min = " + str(round(metrics[s.variable_to_improve].min(),8)))
        
        #ToDo: in ne funktion packen
        # bis parameter history temp
        
        #parameter_list, parameter_history = improved_limits(metrics, parameter_list, parameter_list_full, parameter_history)
  
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
        
        #ToDO: Conditions zusammennfassen
        
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
            if parameter_list_full.iloc[NRMSD_index-1,parameter_index] > parameter_list_full.iloc[NRMSD_index,parameter_index]:
                #print("Was start value")
                parameter_history_temp.iloc[0,4] = "start-value"
                parameter_list.iloc[parameter_index,4] = round(parameter_list.iloc[parameter_index,4]*(1-s.parameter_move_start_end_value),6) 
                parameter_list.iloc[parameter_index,5] = parameter_list_full.iloc[NRMSD_index+1,parameter_index]
            #check if best parameter is last value
            if parameter_list_full.iloc[NRMSD_index+1,parameter_index] < parameter_list_full.iloc[NRMSD_index,parameter_index]:
                #print("Was end value")
                parameter_history_temp.iloc[0,4] = "end-value"
                parameter_list.iloc[parameter_index,4] = parameter_list_full.iloc[NRMSD_index-1,parameter_index]
                parameter_list.iloc[parameter_index,5] = round(parameter_list.iloc[parameter_index,4]*(1+s.parameter_move_start_end_value),6) 
        
        #check if optimal value is last value
        if NRMSD_index >= s.grid_resolution*parameter_list.shape[0]-1:
            #print("Was end value")
            parameter_history_temp.iloc[0,4] = "end-value"
            parameter_list.iloc[parameter_index,4] = parameter_list_full.iloc[NRMSD_index-1,parameter_index]
            parameter_list.iloc[parameter_index,5] = round(parameter_list.iloc[parameter_index,4]*(1+s.parameter_move_start_end_value),6) 
        
        #check if optimal value is first value
        if NRMSD_index <= 0:
            #print("Was start value")
            parameter_history_temp.iloc[0,4] = "start-value"
            parameter_list.iloc[parameter_index,4] = round(parameter_list.iloc[parameter_index,4]*(1-s.parameter_move_start_end_value),6) 
            parameter_list.iloc[parameter_index,5] = parameter_list_full.iloc[NRMSD_index+1,parameter_index]
            
        
        #append parameter_history_temp to parameter_history
        parameter_history = pd.concat([parameter_history, parameter_history_temp], ignore_index = True)
        
    
        print("Improved parameter = " + parameter_history.iloc[analysis_number-1,0])
        print("From value: " + str(parameter_history.iloc[analysis_number-1,1]) + " to value: " + str(parameter_history.iloc[analysis_number-1,2]))

        #create new parameter_list_full with the new default values in parameter_list
        parameter_list_full = af.parameter_list_full(parameter_list)
        
        #calculate relative change of imporoved parameter
        change = round(abs(parameter_history.iloc[analysis_number-1,1]-parameter_history.iloc[analysis_number-1,2])/parameter_history.iloc[analysis_number-1,1],6)
        print("Relative change: "+ str(change))
        parameter_history.iloc[analysis_number-1,5] = change
        
        #calculate delta between nrmsd of current simulations and nrmsd of previous simulation
        if analysis_number > 1:
            delta_nrmsd = abs(parameter_history.iloc[analysis_number-1,3]-parameter_history.iloc[analysis_number-2,3])
            #print("Delta NRMSD = " + str(round(delta_nrmsd,8)))

        #if end condition are met set boolian "stop_condition"
        if (delta_nrmsd < s.nrmsd_delta_end_condition and parameter_history.iloc[analysis_number-1,3] < s.desired_nrmsd) or analysis_number >= s.analysis_number_end_condition:
            stop_condition = False
        
        #print runtime    
        executionTime = (time.time() - startTime)
        print('Elapsed time in seconds: ' + str(round(executionTime,2)))
    
    print("\n")
    
    #Count how many times the optimal value was start, middle or end value
    no_mid_value = 0
    no_start_value = 0
    no_end_value = 0
    for i in np.arange(len(parameter_history)):  
        if parameter_history.iloc[i,4] == "mid-value":
            no_mid_value = no_mid_value+1
        if parameter_history.iloc[i,4] == "start-value":
            no_start_value = no_start_value+1
        if parameter_history.iloc[i,4] == "end-value":
            no_end_value = no_end_value+1
    print("Number of mid values: " + str(no_mid_value))
    print("Number of edge values: " + str(no_start_value + no_end_value))
    
    #print minimal nrmsd
    print("NRMSD min: " + str(parameter_history.iloc[len(parameter_history)-1,3]))
    
    #plot NRMDS history
    parameter_history["NRMSD_min"].plot(title = "NRMSD min")
    
    # Getting the current date and time and use it as a timestamp
    date_time = datetime.now().strftime("%y_%m_%d_%H_%M") 
    #save parameter_list results in excel list with timestamp
    parameter_improved_value_list = parameter_list[["name", "default"]]
    parameter_improved_value_list.to_excel("Analyse Ergebnisse/Analysis parameter_list_{}.xlsx".format(date_time))
    #save parameter_history results in excel list
    parameter_history.to_excel("Analyse Ergebnisse/Analysis parameter_history_{}.xlsx".format(date_time))

    #simulate with improved parameters
    results = parameter_to_simulation(NRMSD_index, parameter_list_full,2100)

    #simulate with default parameters
    world3 = World3(dt=s.sim_time_step)
    world3.init_world3_constants()
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3()   
    pop_pyworld = pd.DataFrame(data = world3.pop)
    
    #save results in one dataframe
    population_results = results["pop_" + str(NRMSD_index)]
    pd.concat([population_results, empirical_data["Population"]], axis = 1)
    pd.concat([population_results, pop_pyworld], axis = 1)
    #plot results
    #population_results.plot(title="Population comparison", legend = True)

    #print final computing time
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(round(executionTime,2)))