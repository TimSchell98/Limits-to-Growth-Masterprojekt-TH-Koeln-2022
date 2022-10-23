import pandas as pd
import numpy as np

import analysis_parallel_settings as s

PRINT_DEBUG_MESSAGES = True


class Parameter:
    """
    Class Parameter for unifying all Parameter relevant Settings in one Datatype.
    """

    def __init__(self, name, default_value, standard_variation=True, start_value=np.NaN, end_value=np.NaN,
                 use_in_analysis=False):
        self.name = name
        self.default_value = default_value
        self.use_standard_variation = standard_variation
        self.start_value = start_value
        self.end_value = end_value
        self.delta = np.NaN
        self.use_in_analysis = use_in_analysis

    def set_start_value(self, start_value):
        self.start_value = start_value

    def set_end_value(self, end_value):
        self.end_value = end_value

    def init_start_end_value(self, divergence):
        if self.default_value - self.default_value * divergence < 0:
            self.set_start_value(0)
        else:
            self.set_start_value(self.default_value - self.default_value * divergence)
        self.set_end_value(self.default_value + self.default_value * divergence)

    def set_delta(self, grid_resolution):
        self.delta = (self.end_value - self.start_value) / (grid_resolution - 1)

def parameter_init(parameter_list_excel_file):
    """
    Diese Function liest die INformationen aus einer Excel Datei ein und gibt eine Liste mit Parameter OObjekten zurück,
    die mit den Informationen aus Excel initialisiert wurden. 

    :param parameter_list_excel_file:
    :return: list_of_parameter_objects
    """
    parameter_list_dataframe = pd.read_excel(parameter_list_excel_file)
    if PRINT_DEBUG_MESSAGES:
        print(parameter_list_dataframe)

    parameter_list = []

    for p in range(len(parameter_list_dataframe)):
        param_obj = Parameter(parameter_list_dataframe['name'].loc[p], parameter_list_dataframe['default'].loc[p],
                              parameter_list_dataframe['standard'].loc[p],
                              use_in_analysis=parameter_list_dataframe['use_in_analysis'].loc[p])
        if param_obj.use_in_analysis:
            obj_name = 'param_{}'.format(param_obj.name)
            vars()[obj_name] = param_obj
            parameter_list.append(vars()[obj_name])
            if vars()[obj_name].use_standard_variation:
                vars()[obj_name].init_start_end_value(s.parameter_divergence)
            vars()[obj_name].set_delta(s.grid_resolution)


    if PRINT_DEBUG_MESSAGES:
        print('Initialized {} Parameters'.format(len(parameter_list)))
    return parameter_list

def parameter_var_list_init(parameter_list):
    '''    setting_values = {'start_value': [],
                      'end_value': []}

    setting_values = pd.DataFrame(data=setting_values, index=['parameter1', 'parameter2', 'parameter3'])
    setting_values['delta'] = (setting_values['end_value'] - setting_values['start_value']) / (grid_resolution - 1)'''
    no_of_parameters = len(parameter_list)
    no_of_combinations = s.grid_resolution ** no_of_parameters
    parameter_var_list_sorted = {}

    for parameter_index in range(no_of_parameters):
        parameter_var_list_sorted[parameter_list[parameter_index].name] = np.arange(
            parameter_list[parameter_index].start_value,
            parameter_list[parameter_index].end_value+0.000001,
            parameter_list[parameter_index].delta)


    '''    # - - Dataframe Parameter list
    parameter_var_list_sorted = {'parameter1': np.arange(setting_values.iloc[0, 0], setting_values.iloc[0, 1] + 0.00001,
                                                         setting_values.iloc[0, 2]),
                                 'parameter2': np.arange(setting_values.iloc[1, 0], setting_values.iloc[1, 1] + 0.00001,
                                                         setting_values.iloc[1, 2]),
                                 'parameter3': np.arange(setting_values.iloc[2, 0], setting_values.iloc[2, 1] + 0.00001,
                                                         setting_values.iloc[2, 2])}
    '''
    parameter_var_list_sorted = pd.DataFrame(data=parameter_var_list_sorted)

    # parameter_var_list_full is a list of every combination of the parameters
    parameter_var_list_full = pd.DataFrame(index=np.arange(no_of_combinations),
                                           data=np.full([no_of_combinations, no_of_parameters], np.NaN))
    first_index = np.zeros(no_of_parameters, dtype=int)
    second_index = np.zeros(no_of_parameters-1, dtype=int)

    #TODO Dieser Algorithmus funktioniert noch nicht richtig und muss noch finalisiert werden
    for grid_iterator in range(no_of_combinations):

        for parameter_iterator in range(no_of_parameters):
            second_index += 1
            if not parameter_iterator == 0:
                if second_index[parameter_iterator-1] == s.grid_resolution:
                    second_index[parameter_iterator-1] = 0
                    first_index[parameter_iterator] += 1

            if first_index[parameter_iterator] == s.grid_resolution:
                first_index[parameter_iterator] = 0

            first_index[parameter_iterator] += 1

            parameter_var_list_full.iloc[grid_iterator, parameter_iterator] = parameter_var_list_sorted.iloc[
                first_index[parameter_iterator-1], parameter_iterator]


    '''
    i1 = 0
    i2 = 0
    i3 = 0
    j = 0
    x = 0
    for i in range(0, grid_resolution ** 3):
        # fill parameter_var_list_full with parameter 1
        i1 = i1 + 1
        parameter_var_list_full.loc[grid_iterator, 0] = parameter_var_list_sorted.iloc[i1 - 1, 0]
        if i1 == grid_resolution:
            i1 = 0

        # fill parameter_var_list_full with parameter 2
        j = j + 1

        parameter_var_list_full.loc[grid_iterator, 1] = parameter_var_list_sorted.iloc[i2, 1]
        if j == grid_resolution:
            j = 0
            i2 = i2 + 1
        if i2 == grid_resolution:
            i2 = 0

        # fill parameter_var_list_full with parameter 3
        x = x + 1
        parameter_var_list_full.loc[grid_iterator, 2] = parameter_var_list_sorted.iloc[i3, 2]
        if x == grid_resolution ** 2:
            x = 0
            i3 = i3 + 1
        if i3 == grid_resolution:
            i3 = 0

    print("Starting limits:")
    print(parameter_var_list_sorted)
    print("Parameter1 = " + parameter1_name)
    print("Parameter2 = " + parameter2_name)
    print("Parameter3 = " + parameter3_name)'''

    return parameter_var_list_full, parameter_var_list_sorted

if __name__ == '__main__':
    parameter_list_excel = 'Parameter.xlsx'
    parameter_list = parameter_init(parameter_list_excel)

    full_list, sorted_list = parameter_var_list_init(parameter_list)

    print('Testing Class Parameter')
