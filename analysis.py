# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import multiprocessing as mp
import analysis_parallel_settings_working as s
import analysis_functions_working as af

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    mp.freeze_support()
    
    
    """
    todo:
    1. dataframe erstellen die alle variablen und die werte dieser beinhaltet. check
    2. run_simulation für jeden inhalt dieses dataframes
    3. variable raussuchen bei der die differenz zu den empirical data am geringsten ist
    4. den wert dieser variable speichern und den alten wert mit diesen überschreiben
    5. weiter bei schritt 2 aber mit neuem wert der variable  
    
    """
    
    
    #   -   -   - create dataframe of all variables with steps -   -   -
    # kann in eine initierungs funktion
    #read excel with to be analysed parameters
    parameter = pd.read_excel('Parameter Liste.xls')
    #create base of parameter list  
    parameter_list = pd.DataFrame(columns = [parameter.var_name], index = np.arange(s.grid_resolution))
    #fill parameter list with steps
    for i in range (0,parameter.shape[0]):
        start_val = round(parameter.iloc[i,2]-parameter.iloc[i,2]*s.parameter_divergence,4)
        end_val = round(parameter.iloc[i,2]+parameter.iloc[i,2]*s.parameter_divergence,4)
        delta = round((end_val-start_val)/(s.grid_resolution-1),6)
        values = np.arange(start_val, end_val+0.001, delta) #probleme bei end_value +0.001 -> da der NRI so hoch ist, darf nicht +0.00001 gerechnet werden. 0.001 ist aber zu groß -> der kleinste standart wert ist 0.001
        #lösung: einfache for schleife
        for x in range(0,s.grid_resolution):
            values[x] = start_val+delta*x
        #write steps into parameter_list
        for j in range (0,s.grid_resolution):
            parameter_list.iloc[j,i] = values[j]
    
    
    
    
    #create dataframe with every possible combination
    #create base
    parameter_list_full = pd.DataFrame(columns = [parameter.var_name],index = np.arange(s.grid_resolution*parameter.shape[0]))
    #fill parameter_list_full with standard values
    for i in range(0,parameter.shape[0]*s.grid_resolution):
        for j in range(0,parameter.shape[0]):
            parameter_list_full.iloc[i,j] = parameter.iloc[j,2]
    #fill parameter_list_full with steps     
    for i in range(0,parameter.shape[0]):
        for j in range(0,s.grid_resolution):
            parameter_list_full.iloc[j+i*5,i] = parameter_list.iloc[j,i]
    
    
    
    
    
    
    #run_simultion in einen loop packen, der so lange geht, bis der delta zwischen dem NRMSD zwischen zwei analysen kleiner 0.0001 ist, oder die zoom stufe bei 25 angelangt ist.
    
    #zoom_amount = 0
    #while delta_nrmsd > 0.0001 and zoom_amount < 25:
        #zoom_amount = zoom_amount +1
    
    #   -   -   - run_simulation for every entry of parameter_list -   -   -
    df_results = pd.DataFrame()
    a = 0
    for i in range(0,parameter_list.shape[1]):
        for j in range(0,s.grid_resolution):
            #so kann jeder eintrag der parameter_list durchgegangen werden
            a = a+1
            #print(a)
            #results = af.run_simulation(parameter_list.size, parameter_list.iloc[0,j] = parameter_list.iloc[i,j]) #wie geht das? Könnte gelöst werden, indem ich einen dataframe erzeuge mit allen "komnbinationen" die ich dann jeweils den parametern zuordne, aber es muss eigenlich auch schöner gehen.
            #pd.concat(df_results, results)
    
    print(type(parameter_list.columns[0]))
    print(type(''.join(map(str, parameter_list.columns[0]))))
    
    """
    var_name ="dcfsn"
    var_value = 5
    results = af.run_simulation(parameter_list.size, var_name = var_value)
    #wie würde das funktionieren?
    """
    
    """
    df_results = pd.DataFrame()
    results = [pool.apply_async(af.run_simulation_test, args=(i, parameter_list_full)) for i in range(0, parameter.shape[0]*s.grid_resolution)]
    for i in results:
        i.wait()
    
    for i in range(0, parameter.shape[0]*s.grid_resolution):
        df_results = pd.concat([df_results, results[i].get()], axis=1)
    print(df_results)
    """
    
    
    #   -   -   - Matrics calculation -   -   -
    
    empirical_data = af.initialize_empirical_data()
    #sollte nicht anders sein als im ersten hauptscript
    
    #min_nrmsd = round(metrics["NRMSD_Population"].min(),4)
    #delta_nrmsd = min_nrmsd_prior - min_nrmsd
    #min_nrmsd_prior = min_nrmsd
    
    
    
    
    
    #   -   -   - Calculate smallest diviation and safe parameter value for the next simulation -   -   -
    
    #wert bei dem die abweichung von den empirical data am geringsten ist, kann in den dataframe "parameter_list" eingefügt werden. Damit kann dann der nächste durchlauf gestartet werden.
    
