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
    
    parameter_list_full = af.init_parameter_list_full()

    
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
    
    #min_nrmsd = round(metrics["NRMSD_Population"].min(),4)
    #delta_nrmsd = min_nrmsd_prior - min_nrmsd
    #min_nrmsd_prior = min_nrmsd



    #   -   -   - Calculate smallest diviation and safe parameter value for the next simulation -   -   -
    
    #wert bei dem die abweichung von den empirical data am geringsten ist, kann in den dataframe "parameter_list" eingefügt werden. Damit kann dann der nächste durchlauf gestartet werden.
    
