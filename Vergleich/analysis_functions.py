import numpy as np

def calculate_d_value(model_data, empirical_data):
    '''Function for the formula for delta value
    Originally from Herrington 2020 - Update to limits to growth
    \n inputs are two arrays with data
    Output is the calculated value different for the last timestep as specified in the paper
    '''
    d_value = (model_data[-1]-empirical_data[-1])/empirical_data[-1]
    return d_value

def calculate_roc(model_data, empirical_data, timestep:float, calculation_interval = 5):
    ''' Function for the formula for the rate of change(roc)
    Originally from Herrington 2020 - Update to limits to growth
    \n inputs:
     two arrays with data
     the timestep between the data points in yrs
     calculation interval in yrs
    \n Output is the calculated roc for the last timestep and the year back the inteval rate
    '''
    stepwidth = calculation_interval * timestep
    roc = ((model_data[-1]-model_data[-stepwidth])-(empirical_data[-1]-empirical_data[-stepwidth]))/(empirical_data[-1]-empirical_data[-stepwidth])
    return roc

def calculate_nrmsd(model_data, empirical_data, timestep:float , calculation_interval=5, calculation_period=50):
    ''' Function for the formula for normalized root mean squre difference (NRMSD)
    Originally from Herrington 2020 - Update to limits to growth
    \n inputs:
     two arrays with data
     the timestep between the data points in yrs
     calculation interval in yrs
     the period for calculating the nrmsd in yrs
    \n Output is the calculated roc for the last timestep and the year back the inteval rate
    '''
    no_of_calculations = int(calculation_period / calculation_interval)
    stepwidth = calculation_interval * timestep

    nominator_single_values = np.zeros(no_of_calculations)
    denominator_single_values = np.zeros(no_of_calculations)

    for i in range(no_of_calculations):
        nominator_single_values[-i-1]=np.square(model_data[-i*stepwidth-1]-empirical_data[-i*stepwidth-1])
        denominator_single_values[-i-1] = empirical_data[-i*stepwidth-1]

    nrmsd = (np.sqrt(nominator_single_values.sum()/6)) / (denominator_single_values.sum()/6)
    return nrmsd

if __name__=='__main__':
    #testing roc and d_value caclulation
    a = np.arange(10)
    b = np.arange(0, 20, 2)
    print(a,b)
    print(calculate_d_value(b, a))
    print(calculate_roc(b, a, 1, 5))

    # testing nrmsd
    a = np.arange(100)
    b = np.arange(0, 200, 2)
    print(calculate_nrmsd(b+100,b,1,5,50))