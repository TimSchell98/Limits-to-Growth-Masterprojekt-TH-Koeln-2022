import numpy as np

def calculate_d_value(model_data, empirical_data):
    '''Function for the Formula vor delta value
    Originally from Herrington 2020 - Update to limits to growth
    inputs are two arrays with data
    Output is the calculated value different for the last timestep as specified in the paper
    '''
    d_value = (model_data[-1]-empirical_data[-1])/empirical_data[-1]
    return d_value

def calculate_roc(model_data, empirical_data, timestep, calculation_interval = 5):
    k = calculation_interval * timestep
    roc = ((model_data[-1]-model_data[-k])-(empirical_data[-1]-empirical_data[-k]))/(empirical_data[-1]-empirical_data[-k])
    return roc


if __name__=='__main__':
    #testing roc and d_value caclulation
    a = np.arange(10)
    b = np.arange(0, 20, 2)
    print(a,b)
    print(calculate_d_value(b, a))
    print(calculate_roc(b, a, 1, 5))