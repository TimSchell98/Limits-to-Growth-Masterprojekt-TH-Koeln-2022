# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:56:16 2022

@author: Tim Schell
"""

from PyWorld3_Update.pyworld3 import World3
from pyworld3.utils import plot_world_variables
import matplotlib.pyplot as plt
import analysis_functions as af
import pandas as pd

params = {'lines.linewidth': '3','axes.labelsize' : '12', 'xtick.labelsize' : '10', 'ytick.labelsize' : '10', 'figure.autolayout' : 'True'}
plt.rcParams.update(params)

new_parameter_list = pd.read_excel('Analysis parameter_list_23_02_24_11_54.xlsx', index_col=0)  
old_parameter_list = pd.read_excel('Parameters_to_be_analysed.xlsx', index_col=0)
print(new_parameter_list)




world3 = World3(dt = 1, pyear = 4000, year_max = 2100)
world3.init_world3_constants(
    
ali =	910434007.1,
alln=	1087.098689,
amti=	2.074183,
faipm=	0.001775,
frpm=	0.021555,
fspd=	3.027545,
hsid=	25.606112,
imef=	0.000012,
imti=	9.568968,
lferti=	750.000012,
lpd=	15.556328,
lufdt=	1.80842,
mtfn=	11.482764,
nri=	9.44862E+11,
nruf1=	1.102015,
pali=	2438793103,
pp19=	145463968.1,
ppgf1=	1.657834,
pptd=	62.666523,
rlt=	29.224133,
sad=	19.649231,
sd=	0.025952,
uildt=	0.655913,
uili=	7139508.077

    
    )

#dynamisch alle variablen aus der erstellten "Analysis parameter_list_{}.xlsx" einfügen
world3.init_world3_variables()
world3.set_world3_table_functions()
world3.set_world3_delay_functions()
world3.run_world3(fast=False)

plot_world_variables(world3.time,
                 [world3.nrfr, world3.io, world3.f, world3.pop,
                  world3.ppolx],
                 ["NRFR", "IO", "F", "POP", "PPOLX"],
                 [[0, 1.975], [0, 4e12], [0, 5.8e12], [0, 12e9], [0, 40]],
                 img_background="./img/fig 4-1-1.png",
                 figsize=(7, 5),
                 title="World3 Referenze Run, 2004 Szenario 1")

plot_world_variables(world3.time,
                 [world3.le, world3.fpc, world3.sopc, world3.ciopc],
                 ["LE", "FPC", "SOPC", "CIOPC"],
                 [[0, 90], [0,1000],[0,970], [0, 250]],
                 img_background="./img/fig 4-1-2.png",
                 figsize=(7, 5),
                 title="World3 Referenze Run - Material standard of living, 2004 Szenario 1")

plot_world_variables(world3.time,
                 [world3.ef, world3.hwi],
                 ["EF", "HWI"],
                 [[0, 4], [0,1]],
                 img_background="./img/fig 4-1-3.png",
                 figsize=(7, 5), title="World3 Referenze Run - Human Wellfare and Footprint, 2004 Szenario 1")



empirical_data=af.initialize_empirical_data()
#empirical_data["Population"]
