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

    #print(parameter_list_full)
    no_of_parameters = len(parameter_list_full.columns)
   
    parameter_dict = {}
    #parameter_list_full.columns[column_index][0]
    for column_index, column_name in enumerate(parameter_list_full.columns):
        parameter_dict[column_name[0]] = parameter_list_full[column_name[0]].iloc[i].item()
        #print(parameter_dict[column_name[0]])
    return af.run_simulation_kwargs(i, **parameter_dict)

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    mp.freeze_support()

    
    #   -   -   - create dataframe of all variables with steps, empirical data and parameter hhistory -   -   -
    #create base list of parameter to be analysed
    parameter_list=af.init_parameter_list()
    #create list of every combination of parameters
    parameter_list_full = af.parameter_list_full(parameter_list)
    #initialize empirical data
    empirical_data = af.initialize_empirical_data()
    #DataFrame in which in every step the change is being saved, nrmsd_min könnte hier auch noch hinzugefügt werden usw.
    parameter_history = pd.DataFrame(columns = ["changed parameter", "previous value", "next value", "NRMSD_min"])
    #Temporary version of parameter_history
    parameter_history_temp = pd.DataFrame(columns = ["changed parameter", "previous value", "next value", "NRMSD_min"], index = [0])

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
        
        #nrmsd in liste speichern
        parameter_history_temp["NRMSD_min"] = round(metrics[s.variable_to_improve].min(),6)

    
    #   -   -   - Plot data -   -   -
        #plot population
        population_list = []
        for i in range(0,parameter_list_full.shape[0]):
            population_list.append("POP_" + str(i))
            
        df_results[population_list].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Population"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Population')
        plt.ylim([1e9,10e9])
        plt.xlim([0,122])
        plt.show()  
        
        """
        #plot ecological footprint
        #ef ist gar nicht in nrmsd total drin
        ef_list = []
        for i in range(0,parameter_list_full.shape[0]):
            ef_list.append("Ecological-Footprint_" + str(i))
            
        df_results[ef_list].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Ecological_Footprint"].plot(legend=0, color = ["r"], linewidth = 1.5)
        plt.title('Ecological Footprint') 
        plt.ylim([0,5])
        plt.xlim([0,122])
        plt.show()
        """
        
        
        #todo:
        #andere vegleichsvariablen ploten
        
    
    
    
        #   -   -   - Calculate next parameter_list_full -   -   -
        print(str(s.variable_to_improve) + " min = " + str(round(metrics[s.variable_to_improve].min(),6)))
        
        
        """
        #Zoom methode 1: parameter_divergence wird vekleinert für jede verbesserung eines parameters. FEHLER: Die grid_resolution macht keinen unterschied!
        #in ne funktion packen!
        NRMSD_index = int(metrics["NRMSD_total"].idxmin())-1 #-1 weil metrics bei 1 beginnt und parameter_list_full bei 0
        new_parameter_values=parameter_list_full.iloc[[NRMSD_index]].transpose()
        new_parameter_values.set_index([np.arange(parameter_list.shape[0])], inplace = True)
        #check if new value is equal to standard value, if no, set new default value
        for i in range (0,parameter_list.shape[0]):
            if parameter_list.iloc[i,2] != new_parameter_values.iloc[i,0]:
                #save new parameter in dataframe
                parameter_history_temp.iloc[0,0] = parameter_list.iloc[i,0]
                parameter_history_temp.iloc[0,1] = parameter_list.iloc[i,2]
                parameter_history_temp.iloc[0,2] =  new_parameter_values.iloc[i,0]
    
        parameter_history = pd.concat([parameter_history, parameter_history_temp], ignore_index = True)

        #count how many times the parameter of the current time step has been improved
        parameter_counter = 0
        for i in range(0,parameter_history.shape[0]-1):
            if parameter_history.iloc[i,0] == parameter_history.iloc[parameter_history.shape[0]-1,0]:
                parameter_counter = parameter_counter+1
        
        #shrink parameter_divergence the number of times which the parameter has been improved
        for i in range (0,parameter_list.shape[0]):
            if parameter_list.iloc[i,2] != new_parameter_values.iloc[i,0]:
                #calculate new parameter values
                parameter_list.iloc[i,2] = new_parameter_values.iloc[i,0]
                parameter_list.iloc[i,4] = round(new_parameter_values.iloc[i,0]-new_parameter_values.iloc[i,0]*(s.parameter_divergence*(1-s.parameter_divergence_shrinkage)**parameter_counter),4)
                parameter_list.iloc[i,5] = round(new_parameter_values.iloc[i,0]+new_parameter_values.iloc[i,0]*(s.parameter_divergence*(1-s.parameter_divergence_shrinkage)**parameter_counter),4)
        #create new parameter_list_full with the new default values in parameter_list
        parameter_list_full = af.parameter_list_full(parameter_list)
        """
        
        
        
        
        #zoom methode 2: Für den Parameter der verbessert werden soll, wird der vorherige und der nächste wert als neuer start und end wert genommenn.
        #Falls der beste wert ein rand wert sein sollte, wird die grenze um 20% verschoben todo: 20% zu einer veränderbaren variable ändern
        #in ne funktion packen
        
        #Find NRMSD index of line which has the minimal NRMSD.
        NRMSD_index = int(metrics[s.variable_to_improve].idxmin())-1 #-1, becouse metrics dataframe starts at index 1, parameter_list_starts at 0
        #save parameter values of line "NRMSD_index" as new defaults
        new_parameter_values=parameter_list_full.iloc[[NRMSD_index]].transpose()
        new_parameter_values.set_index([np.arange(parameter_list.shape[0])], inplace = True)
        #check if new value is equal to standard value, if no, set new default value and save improved parameter
        for i in range (0,parameter_list.shape[0]):
            if parameter_list.iloc[i,2] != new_parameter_values.iloc[i,0]:
                #save improved parameter name and new+old value in parameter_list
                parameter_history_temp.iloc[0,0] = parameter_list.iloc[i,0]
                parameter_history_temp.iloc[0,1] = parameter_list.iloc[i,2]
                parameter_history_temp.iloc[0,2] = new_parameter_values.iloc[i,0]
                #save improved value in parameter_list
                parameter_list.iloc[i,2] = new_parameter_values.iloc[i,0]
                #save index of to-be-improved parameter in parameter_list_full    
                parameter_index = i
        
        #append parameter_history_temp to parameter_history
        parameter_history = pd.concat([parameter_history, parameter_history_temp], ignore_index = True)
        
        
        print("Improved parameter = " + parameter_history.iloc[analysis_number-1,0])
        print("From value: " + str(parameter_history.iloc[analysis_number-1,1]) + " to value: " + str(parameter_history.iloc[analysis_number-1,2]))
        
        #if best parameter value is not an edge value, use previous value and next value as new start and end values
        if parameter_list_full.iloc[NRMSD_index-1,parameter_index] < parameter_list_full.iloc[NRMSD_index, parameter_index] and parameter_list_full.iloc[NRMSD_index+1,parameter_index] > parameter_list_full.iloc[NRMSD_index,parameter_index]:
            parameter_list.iloc[parameter_index,4] = parameter_list_full.iloc[NRMSD_index-1,parameter_index]
            parameter_list.iloc[parameter_index,5] = parameter_list_full.iloc[NRMSD_index+1,parameter_index]
        #check if best parameter value is edge value, if yes then calculate next value
        #check if best parameter is first value
        #move start value by 20%
        if parameter_list_full.iloc[NRMSD_index-1,parameter_index] > parameter_list_full.iloc[NRMSD_index,parameter_index]:
            print("Was edge value")
            parameter_list.iloc[parameter_index,4] = round(parameter_list.iloc[parameter_index,4]*(1-s.parameter_move_start_end_value),6) 
            parameter_list.iloc[parameter_index,5] = parameter_list_full.iloc[NRMSD_index+1,parameter_index]
        #check if best parameter is last value
        #move last value by 20%
        if parameter_list_full.iloc[NRMSD_index+1,parameter_index] < parameter_list_full.iloc[NRMSD_index,parameter_index]:
            print("Was edge value")
            parameter_list.iloc[parameter_index,4] = parameter_list_full.iloc[NRMSD_index-1,parameter_index]
            parameter_list.iloc[parameter_index,5] = round(parameter_list.iloc[parameter_index,4]*(1+s.parameter_move_start_end_value),6) 
        
        #create new parameter_list_full with the new default values in parameter_list
        parameter_list_full = af.parameter_list_full(parameter_list)
        
        
        #calculate delta between nrmsd of current simulations and nrmsd of previous simulation
        if analysis_number > 1:
            delta_nrmsd = abs(round(parameter_history.iloc[analysis_number-1,3]-parameter_history.iloc[analysis_number-2,3],6))
            print("Delta NRMSD = " + str(delta_nrmsd))
        
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
    parameter_improved_value_list.to_excel("Analysis parameter_list_{}.xlsx".format(date_time))
    
    #save parameter_history results in excel list
    parameter_history.to_excel("Analysis parameter_history_{}.xlsx".format(date_time))
    
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(round(executionTime,2)))
    #   -   -   - Calculate smallest diviation and safe parameter value for the next simulation -   -   -
    
    #wert bei dem die abweichung von den empirical data am geringsten ist, kann in den dataframe "parameter_list" eingefügt werden. Damit kann dann der nächste durchlauf gestartet werden.
    
