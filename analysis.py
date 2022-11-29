# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import multiprocessing as mp
import analysis_parallel_settings_working as s
import analysis_functions_working as af

import matplotlib.pyplot as plt

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
    #DataFrame in which in every step the change is being saved, nrmsd_min könnte hier auch noch hinzugefügt werden usw.
    parameter_history = pd.DataFrame(columns = ["changed parameter", "previous value", "next value", "NRMSD_min"])
    
    #   -   -   - create dataframe of all variables with steps -   -   -
    
    #create base list of parameter to be analysed
    parameter_list=af.init_parameter_list()
    
    #create list of every combination of parameters
    parameter_list_full = af.parameter_list_full(parameter_list)
    
    #after first initiation the value at "standard" collumn should be used, so that the new value can be used in next run
    #parameter_list["standard"] = True

    #   -   -   - run_simulation for every entry of parameter_list -   -   -
    no_of_simulations = len(parameter_list_full)
    analysis_number = 0
    delta_nrmsd = 0.0002
    
    while delta_nrmsd > 0.0001 and analysis_number < 25:
        analysis_number = analysis_number + 1
    

        
        df_results2 = pd.DataFrame()
        #results = [pool.apply_async(af.run_simulation_combinations, args=(i, parameter_list_full)) for i in range(0, parameter_list_full.shape[0])]
        results = [pool.apply_async(parameter_to_simulation, args=(i, parameter_list_full)) for i in
                   range(0, no_of_simulations)]
        
        for i in results:
            i.wait()
        
        for i in range(0, no_of_simulations):
            df_results2 = pd.concat([df_results2, results[i].get()], axis=1)
        #print(df_results)
        
        
     
    
        
        
        
    
        #   -   -   - Metrics calculation -   -   -
        
        empirical_data = af.initialize_empirical_data()
        
        metrics = pd.DataFrame()
        
        for i in range(0, no_of_simulations):
            print(i)
            metric_result = af.calculate_metrics(df_results2, empirical_data,i) #funktioniert noch nicht
            metrics = pd.concat([metrics, metric_result])
        
        #nrmsd in liste speichern
        parameter_history.iloc[i,3]= metrics["NRMSD_total"].min()
        
        #nrmsd delta berechnen
        if i>1:
            nrmsd_delta = parameter_history.iloc[i,3]-parameter_history.iloc[i-1,3]
        
    
    
        
        #test: plot population
        population_list = []
        for i in range(0,parameter_list_full.shape[0]):
            population_list.append("POP_" + str(i))
            
        df_results2[population_list].plot(legend=0, color = ["b"], linewidth = 0.4)
        empirical_data["Population"].plot(legend=0, color = ["r"], linewidth = 1.5)
        
        plt.ylim([1e9,10e9])
        plt.xlim([0,122])
        plt.show()  
        
    
    
    
        #   -   -   - Calculate next parameter_list_full -   -   -
        
        
        
        
        #wenn metrics calculation fertig, das hier alles in eine funktion packen
        parameter_history_temp = pd.DataFrame(columns = ["changed parameter", "previous value", "next value", "NRMSD_min"], index = [0])
        #test: ich tue so als wäre die erste zeile die zeile mit dem niedrigsten NRMSD:
        new_parameter_values=parameter_list_full.iloc[[0]].transpose()
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
        
        #shrink parameter_divegens the number of times which the parameter has been improved
        for i in range (0,parameter_list.shape[0]):
            if parameter_list.iloc[i,2] != new_parameter_values.iloc[i,0]:
                #calculate new parameter values
                parameter_list.iloc[i,2] = new_parameter_values.iloc[i,0]
                parameter_list.iloc[i,4] = round(new_parameter_values.iloc[i,0]-new_parameter_values.iloc[i,0]*(s.parameter_divergence*(1-s.parameter_divergence_shrinkage)**parameter_counter),4)
                parameter_list.iloc[i,5] = round(new_parameter_values.iloc[i,0]+new_parameter_values.iloc[i,0]*(s.parameter_divergence*(1-s.parameter_divergence_shrinkage)**parameter_counter),4)
                
        #wenn analyse fertig:
        #parameter_list_full = af.parameter_list_full(parameter_list)
        #zum testen:
        parameter_list_full_second_simulation = af.parameter_list_full(parameter_list)
        
        
        
        
        
        
        
        
     #zoom test: ich tue wieder so, dass die erste zeile die zeile ist mit dem niedrigsten nrmsd, um zu checken ob richtig gezoomed wird. Der parameter_divergence sollte jetzt nur noch 0.425 sein
        parameter_history_temp = pd.DataFrame(columns = ["changed parameter", "previous value", "next value", "NRMSD_min"], index = [0])
        #test: ich tue so als wäre die erste zeile die zeile mit dem niedrigsten NRMSD:
        new_parameter_values2=parameter_list_full_second_simulation.iloc[[0]].transpose()
        new_parameter_values2.set_index([np.arange(parameter_list.shape[0])], inplace = True)
        #check if new value is equal to standard value, if no, set new default value
        for i in range (0,parameter_list.shape[0]):
            if parameter_list.iloc[i,2] != new_parameter_values2.iloc[i,0]:
                #save new parameter in dataframe
                parameter_history_temp.iloc[0,0] = parameter_list.iloc[i,0]
                parameter_history_temp.iloc[0,1] = parameter_list.iloc[i,2]
                parameter_history_temp.iloc[0,2] =  new_parameter_values2.iloc[i,0]
       
        parameter_history = pd.concat([parameter_history, parameter_history_temp], ignore_index = True)


        #count how many times the parameter of the current time step has been improved
        parameter_counter = 0
        for i in range(0,parameter_history.shape[0]-1):
            if parameter_history.iloc[i,0] == parameter_history.iloc[parameter_history.shape[0]-1,0]:
                parameter_counter = parameter_counter+1
        
        print(s.parameter_divergence*(1-s.parameter_divergence_shrinkage)**parameter_counter)
       
        #end while loop:
        delta_nrmsd = 0.000001
     
    
 
    #   -   -   - Calculate smallest diviation and safe parameter value for the next simulation -   -   -
    
    #wert bei dem die abweichung von den empirical data am geringsten ist, kann in den dataframe "parameter_list" eingefügt werden. Damit kann dann der nächste durchlauf gestartet werden.
    
