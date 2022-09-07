# - - - - Imports - - - - - -
import multiprocessing as mp
import numpy as np
import pandas as pd
import analysis_functions as af
import analysis_parallel_settings as s
import time

# - - -  World 3 import and Version Switching
use_update = False
if use_update:
    from PyWorld3_Update.pyworld3 import World3
else:
    from pyworld3 import World3

# - - - - - - Function definitions - -

def run_simulation(i):
    # simulation durchführen
    world3 = World3(dt=s.sim_time_step)
    world3.init_world3_constants(dcfsn=s.dcfsn_start_val+i*s.dcfsn_delta)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)

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

    # - - - Run Simulation - - -
    if not run_parallel:
        for i in range(0, s.sim_anzahl):
            print("\nSimulation", end=": ")
            print(i + 1)
            print("ETA", end=": ")
            print(round((s.sim_anzahl - i) * 2.8, 2), end="")
            print("s")
            # pool.map(run_simulation)
            # pool.close()
            run_simulation(i)
    else:
        print('Running in parallel mode')
        df_results = pd.DataFrame()
        results = pool.map(run_simulation, [i for i in range(0, s.sim_anzahl)])
        for i in range(0, s.sim_anzahl):
            df_results = pd.concat([df_results, results[i]], axis=1)
    print(df_results)

    # - - - Metric calculation - -
    empirical_data = af.initialize_empirical_data()
    model_data, empirical_data_slice = af.prepare_data_for_metric_calc(df_results, empirical_data, s.pop_name)
    metrics = pd.DataFrame()
    for i in range(s.sim_anzahl):
        metric_result = af.calculate_metrics(model_data['POP_{}'.format(i)], empirical_data_slice, str(i+1), 'dcfsn',
                                             s.parameter_var_list.iloc[i,0])
        metrics = pd.concat([metrics, metric_result])

    print(metrics)
    #results = pool.map(af.calculate_metrics(model_data['AL_{}'.format(i)]))
