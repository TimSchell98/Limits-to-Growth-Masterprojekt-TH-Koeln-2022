#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 16:25:56 2022

Master Project 
02_Parameter Camparison
creat function for 
    Rate of Change 
    NRMSD - Root-mean-square davitation (Mittleres Abweichungsquadrat)
see Teams:Parameter_Vergleich_Vorbereitung  

@author: rubenwillamowski
"""

## Data creatiopn - see function at line 45
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt


# Data
n            = 200                                      #time steps
t            = np.arange(n)                             #create time vektor #TODO should be same like py3
y_real_data  = 0.1*t**3+0.2*t**2+t+10                   #real Data like py3
y_same       = y_real_data                              #same Data to compare accuracy 
y_noise      = np.random.normal(y_real_data,50000,n)    #random difference 
y_dif        = y_real_data*1.2                          #20 % difference to real data
d_value_list = []                                       #empty list for later
d_roc_list   = []
nrmsd_list   = []                                       #empty list for later

# Plot
fig, ax = plt.subplots()

ax.plot(t, y_noise, linewidth=2.0)
ax.plot(t, y_real_data, linewidth=2.0)
ax.plot(t, y_dif, linewidth=2.0)

ax.set(xlim=(0, 200), xticks=np.arange(0, 200, 50),
       ylim=(0, 1000000), yticks=np.arange(0, 1000000, 100000))

plt.legend(["y_noise", "y", "y_dif"])
plt.show()


""" Function"""


def compare(pyworld_data, year_n = 0, sensivity_variable = 0, real_data = y_real_data):
    """calculate Rate of Change, NRMSD (Branderhorst 2020)
    y = observed Data
    y_diff = Variable
    year_n = start year
    """
    
    for year_n in np.arange(0,n,5):
        #d_value
        d_value      = (pyworld_data[year_n-1]-real_data[year_n-1])/real_data[year_n-1]
        d_value_list.append(d_value)
        d_value_sum = sum(d_value_list)
        
        #roc
        d_roc   = (((pyworld_data[year_n-1]-pyworld_data[year_n-6])-(real_data[year_n-1]-real_data[year_n-6]))
               /(real_data[year_n-1]-real_data[year_n-6]))
        d_roc_list.append(d_roc)
        d_roc_sum = sum(d_roc_list)
        
        #nrmsd
        nrmsd   = (((((pyworld_data[year_n-1]-real_data[year_n-1])**2)/6))**(1/2))/(real_data[year_n-1]/6)    
        nrmsd_list.append(nrmsd)
        nrmsd_sum = sum(nrmsd_list)
                
    
    results_dvalue = pd.DataFrame(data = d_value_sum, index = [sensivity_variable], 
                     columns = ['d value'])
    results_droc   = pd.DataFrame(data = d_roc_sum, index = [sensivity_variable], 
                     columns = ['d ROC'])
    results_nrmsd  = pd.DataFrame(data = nrmsd_sum, index = [sensivity_variable], 
                     columns = ['NRMSD'])
    
    results = pd.concat([results_dvalue, results_droc, results_nrmsd], 
                        axis = 1)
    
    return results
    

## Call Function + Print Results
res = compare(y_noise)
print (res)

