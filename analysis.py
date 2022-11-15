# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import multiprocessing as mp
import analysis_parallel_settings_working as s
import analysis_functions_working as af

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    mp.freeze_support()
    
    #   -   -   - create dataframe of all variables with steps -   -   -
    
    #create base list of parameter to be analysed
    parameter_list=af.init_parameter_list()
    
    #create list of every combination of parameters
    parameter_list_full = af.parameter_list_full(parameter_list)
    
    #after first initiation the value at "standard" collumn should be used, so that the new value can be used in next run
    parameter_list["standard"] = True

    #   -   -   - run_simulation for every entry of parameter_list -   -   -
   
    #zoom_amount = 0
    #while delta_nrmsd > 0.0001 and zoom_amount < 25:
        #zoom_amount = zoom_amount +1
    

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
    
    #nrmsd in liste speichern
    #nrmsd_delta = nrmsd[aktueller zeitschritt]-nrmsd[vorhergegenagener zeitschritt]


    #test: neuen parameter wert speichern
    #es wird testweise die erste zeile der parameter_list_full benutzt
    #Im funktionierenden code wird einfach die zeile benutzt bei der der nrmsd am gringsten ist.
    #die spalte "default" des "parameter_liste" DataFrame wird mit der zeile der parameter werten überschrieben.
    #mit der parameter_liste kann jetzt wieder in die parameter_list_full gesteckt werden
    neue_parameter_werte=parameter_list_full.iloc[[0]].transpose()
    neue_parameter_werte.set_index([np.arange(parameter_list.shape[0])], inplace = True)
    parameter_list["default"] = neue_parameter_werte
    parameter_list_full_second_simulation = af.parameter_list_full(parameter_list)
    
    
    
    
    #to do: es wird jetzt noch nicht "gezoomed". Die steps bzw der delta ist immer gleich groß, das muss noch verändert werden
    #wenn wir in einer liste speichern, können wir checken ob ein parameter schoneinmal "verbessert" wurde. Falls dies der Fall ist kann dioser parameter "gezoomed" werden.
    #mann kann auch direkt die zeile vor und nach der zeile mit dem besten NRMSD nehmen (mit safety code) aber dann ist wieder der fehler dass in die falsche richtung gezoomed wird.
    #es kann auch erst nach x durchgängen gezoomt werden, damit alle parameter einmal verbessert wurden aber das ist unsafe

    #   -   -   - Calculate smallest diviation and safe parameter value for the next simulation -   -   -
    
    #wert bei dem die abweichung von den empirical data am geringsten ist, kann in den dataframe "parameter_list" eingefügt werden. Damit kann dann der nächste durchlauf gestartet werden.
    
