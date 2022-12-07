# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:56:16 2022

@author: Tim Schell
"""

import pandas as pd
import analysis_functions_working as af
from pyworld3 import World3



empirical_data = af.initialize_empirical_data()


world3 = World3(dt = 1, pyear = 4000, year_max = 2022)
world3.init_world3_constants(dcfsn=3.8,len=28.0,mtfn=13.47273,lfpf=0.63907,icor1=3.0,scor1=1.025139,faipm = 0.000836,fioac1=0.43,lfh=0.7,palt=3200000000.0,pl=0.1,sd=0.052059,alln=1000.0,sfpc=230.0,frpm=0.006587,nri=1636363636363.6362)
#dynamisch alle variablen aus der erstellten "Analysis parameter_list_{}.xlsx" einfügen
world3.init_world3_variables() #faipm=0.000836
world3.set_world3_table_functions()
world3.set_world3_delay_functions()
world3.run_world3(fast=False)

world3_data = pd.DataFrame(data = world3.pop)

world3_data.plot()
empirical_data["Population"].plot()
