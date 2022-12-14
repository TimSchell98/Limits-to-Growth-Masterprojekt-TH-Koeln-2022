# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import multiprocessing as mp
import analysis_parallel_settings_working as s
import analysis_functions_working as af
import matplotlib.pyplot as plt
import time
from datetime import datetime
startTime = time.time()


def parameter_to_simulation(i, parameter_list_full):
    parameter_dict = {}
    #parameter_list_full.columns[column_index][0]
    for column_index, column_name in enumerate(parameter_list_full.columns):
        parameter_dict[column_name[0]] = parameter_list_full[column_name[0]].iloc[i].item()
        #print(parameter_dict[column_name[0]])
    return af.run_simulation_kwargs(i, **parameter_dict)

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
    parameter_history = pd.DataFrame(columns = ["changed parameter", "previous value", "next value", "NRMSD_min"])

    #   -   -   - run analysis -   -   -
    no_of_simulations = len(parameter_list_full)
    analysis_number = 0
    stop_condition = True
    #delta_NRMSD will be calculated in the third run, so it has to be predefined
    delta_nrmsd = 1
    
    print('Number of simulations in one zoom = ' + str(len(parameter_list_full)))
    print('Estimated time for one zoom = ' + str(round(len(parameter_list_full)*0.644)) + ' seconds')

    #start of analysis loop, stops of stop conditions are reached
    while stop_condition == True:
        analysis_number = analysis_number + 1
    
        print('\nNumber of zooms completed = ' + str(analysis_number-1))
        print('Number of simulations completed = ' + str(len(parameter_list_full) * (analysis_number-1)))
        
        df_results = pd.DataFrame()
        #results = [pool.apply_async(af.run_simulation_combinations, args=(i, parameter_list_full)) for i in range(0, parameter_list_full.shape[0])]
        results = [pool.apply_async(parameter_to_simulation, args=(i, parameter_list_full)) for i in
                   range(0, no_of_simulations)]
        
        for i in results:
            i.wait()
        
        for i in range(0, no_of_simulations):
            df_results = pd.concat([df_results, results[i].get()], axis=1)
        #print(df_results)

        #   -   -   - Metrics calculation -   -   -

        metrics = pd.DataFrame()
        
        for i in range(0, no_of_simulations):
            #die ersten drei parameter die analysiert werden werden in den metrics dataframe geschrieben, entweder alle oder keinen.
            metric_result = af.calculate_metrics_multiple_attributes(df_results, empirical_data, str(i+1),
                                                 'parameter1',parameter_list_full.iloc[i,0],
                                                 'parameter2',parameter_list_full.iloc[i,1],
                                                 'parameter3',parameter_list_full.iloc[i,2])
            metrics = pd.concat([metrics, metric_result])
            
    #   -   -   - Plot data -   -   -
        
        #ToDo in eine funktion packen
        #plot population
        for i in range(0,parameter_list_full.shape[0]):
            df_results['pop_{}'.format(i)].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Population"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Population')
        plt.ylim([1e9,10e9])
        plt.xlim([0,122])
        plt.show()
        
        #plot death rate
        for i in range(0,parameter_list_full.shape[0]):
            df_results['cdr_{}'.format(i)].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Death_rate"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Death Rate')
        plt.ylim([5,25])
        plt.xlim([0,122])
        plt.show()  
        
        #plot birth rate
        for i in range(0,parameter_list_full.shape[0]):
            df_results['cbr_{}'.format(i)].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Birth_rate"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Birth Rate')
        plt.ylim([5,55])
        plt.xlim([0,122])
        plt.show() 
        
        #plot food per capita 
        for i in range(0,parameter_list_full.shape[0]):
            df_results['fpc_{}'.format(i)].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Food_per_capita_ve"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Food per Capita')
        plt.ylim([0,1000])
        plt.xlim([0,122])
        plt.show() 
        
        #plot Pollution_proportion
        for i in range(0,parameter_list_full.shape[0]):
            df_results['pp_dtp_{}'.format(i)].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Pollution_proportion"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Pollution')
        plt.ylim([-1,2])
        plt.xlim([0,122])
        plt.show() 
        
        #plot Expected_years_of_schooling_proportion
        for i in range(0,parameter_list_full.shape[0]):
            df_results['sopcp_{}'.format(i)].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Expected_years_of_schooling_proportion"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Expected years of schooling')
        plt.ylim([-0.25,0.25])
        plt.xlim([0,122])
        plt.show() 
        
        #plot Fossil_fuel_consumption_proportion
        for i in range(0,parameter_list_full.shape[0]):
            df_results['nrurp_{}'.format(i)].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Fossil_fuel_consumption_proportion"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Fossil fuel consumption')
        plt.ylim([-0.25,0.25])
        plt.xlim([0,122])
        plt.show() 
        
        #plot IPP
        for i in range(0,parameter_list_full.shape[0]):
            df_results['iop_{}'.format(i)].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["IPP_USA_proportion"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('IPP')
        plt.ylim([-0.40,0.40])
        plt.xlim([0,122])
        plt.show() 
        
        #plot EF
        for i in range(0,parameter_list_full.shape[0]):
            df_results['ef_{}'.format(i)].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Ecological_Footprint"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Ecological Footprint (not in NRMSD total!)')
        plt.ylim([0,5])
        plt.xlim([0,122])
        plt.show()
        
        #plot HWI
        for i in range(0,parameter_list_full.shape[0]):
            df_results['hwi_{}'.format(i)].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Human_Welfare"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Human Welfare Index (not in NRMSD total!)')
        plt.ylim([0,1])
        plt.xlim([0,122])
        plt.show()
    
        #   -   -   - Calculate next parameter_list_full and save values in list -   -   -
        print(str(s.variable_to_improve) + " min = " + str(round(metrics[s.variable_to_improve].min(),8)))
        
        #ToDo: in ne funktion packen
    
        #Find NRMSD index of line which has the minimal NRMSD.
        NRMSD_index = int(metrics[s.variable_to_improve].idxmin())-1 #-1, because metrics dataframe starts at index 1, parameter_list_starts at 0

        #Temporary version of parameter_history
        parameter_history_temp = pd.DataFrame(columns = ["changed parameter", "previous value", "next value", "NRMSD_min"], index = [0])
        
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
    
        #append parameter_history_temp to parameter_history
        parameter_history = pd.concat([parameter_history, parameter_history_temp], ignore_index = True)
        
        print("Improved parameter = " + parameter_history.iloc[analysis_number-1,0])
        print("From value: " + str(parameter_history.iloc[analysis_number-1,1]) + " to value: " + str(parameter_history.iloc[analysis_number-1,2]))
        
        #if best parameter value is not an edge value, use previous value and next value as new start and end values
        if parameter_list_full.iloc[NRMSD_index-1,parameter_index] < parameter_list_full.iloc[NRMSD_index, parameter_index] and parameter_list_full.iloc[NRMSD_index+1,parameter_index] > parameter_list_full.iloc[NRMSD_index,parameter_index]:
            print("Was mid value")
            parameter_list.iloc[parameter_index,4] = parameter_list_full.iloc[NRMSD_index-1,parameter_index]
            parameter_list.iloc[parameter_index,5] = parameter_list_full.iloc[NRMSD_index+1,parameter_index]
        #check if best parameter value is edge value, if yes then move start or end value by given amount
        #check if best parameter is first value
        if parameter_list_full.iloc[NRMSD_index-1,parameter_index] > parameter_list_full.iloc[NRMSD_index,parameter_index]:
            print("Was edge value")
            parameter_list.iloc[parameter_index,4] = round(parameter_list.iloc[parameter_index,4]*(1-s.parameter_move_start_end_value),6) 
            parameter_list.iloc[parameter_index,5] = parameter_list_full.iloc[NRMSD_index+1,parameter_index]
        #check if best parameter is last value
        if parameter_list_full.iloc[NRMSD_index+1,parameter_index] < parameter_list_full.iloc[NRMSD_index,parameter_index]:
            print("Was edge value")
            parameter_list.iloc[parameter_index,4] = parameter_list_full.iloc[NRMSD_index-1,parameter_index]
            parameter_list.iloc[parameter_index,5] = round(parameter_list.iloc[parameter_index,4]*(1+s.parameter_move_start_end_value),6) 
        
        #create new parameter_list_full with the new default values in parameter_list
        parameter_list_full = af.parameter_list_full(parameter_list)
        
        #calculate delta between nrmsd of current simulations and nrmsd of previous simulation
        if analysis_number > 1:
            delta_nrmsd = abs(parameter_history.iloc[analysis_number-1,3]-parameter_history.iloc[analysis_number-2,3])
            print("Delta NRMSD = " + str(round(delta_nrmsd,8)))
        
        #if end condition are met set boolian "stop_condition"
        if (delta_nrmsd < s.nrmsd_delta_end_condition and parameter_history.iloc[analysis_number-1,3] < s.desired_nrmsd) or analysis_number >= s.analysis_number_end_condition:
            stop_condition = False
            
        executionTime = (time.time() - startTime)
        print('Elapsed time in seconds: ' + str(round(executionTime,2)))
     
    #plot NRMDS history
    parameter_history["NRMSD_min"].plot()
    
    # Getting the current date and time and use it as a timestamp
    date_time = datetime.now().strftime("%y_%m_%d_%H_%M")
    
    #save parameter_list results in excel list with timestamp
    parameter_improved_value_list = parameter_list[["name", "default"]]
    parameter_improved_value_list.to_excel("Analyse Ergebnisse/Analysis parameter_list_{}.xlsx".format(date_time))
    
    #save parameter_history results in excel list
    parameter_history.to_excel("Analyse Ergebnisse/Analysis parameter_history_{}.xlsx".format(date_time))
    
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(round(executionTime,2)))