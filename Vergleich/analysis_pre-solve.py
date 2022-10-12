'''
Contains a function that can be called to pre-solve 1 parameter with 1 empirical dataset.
It specifies the number of runs the model should take.
'''

# - - - - -  Imports  - - - - -
from analysis_parallel import run_simulation
import multiprocessing as mp
import analysis_parallel_settings as s
import pandas as pd


def pre_solver(parameter_name, empirical_data_name):
    #parameter initialisation
    parameter_var_list = pd.DataFrame()
    if parameter_name



'''Code for Script Testing'''
if __name__ == '__main__':
    print('Collapsing in:\n......3\n....2\n....2')
    test_parameter_name = 'dcfsn'
    test_empirical_data_name = 'Population'
    pre_solver(test_parameter_name,test_empirical_data_name,depth)
