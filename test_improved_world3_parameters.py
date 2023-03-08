# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:56:16 2022

@author: Tim Schell
"""

from PyWorld3_Update.pyworld3 import World3
#from pyworld3.utils import plot_world_variables
import result_plotting as rs
import matplotlib.pyplot as plt
import analysis_functions as af
import pandas as pd

params = {'lines.linewidth': '3','axes.labelsize' : '12', 'xtick.labelsize' : '10', 'ytick.labelsize' : '10', 'figure.autolayout' : 'True'}
plt.rcParams.update(params)

new_parameter_list = pd.read_excel('Neue Parameter Liste/Analysis parameter_list_23_03_04_17_10.xlsx', index_col=0)

old_parameter_list = pd.read_excel('Parameters_to_be_analysed.xlsx', index_col=0)
print(new_parameter_list)
empirical_data=af.initialize_empirical_data(True)

parameter_dict = {}
for index, name in enumerate(new_parameter_list['name']):
    parameter_dict[name] = new_parameter_list['default'].iloc[index].item()

world3 = World3(dt = 1, pyear = 4000, year_max = 2100)
world3.init_world3_constants(**parameter_dict)
#world3.init_world3_constants()
world3.init_world3_variables()
world3.set_world3_table_functions()
world3.set_world3_delay_functions()
world3.run_world3(fast=False)

plt.figure(dpi=300)

"""
plot_world_variables(world3.time,
                 [empirical_data["Population"], world3.io, world3.f, world3.pop,
                  world3.ppolx, world3.nrfr],
                 ["POPEMP", "IO", "F", "POP", "PPOLX", "NRFR"],
                 [[0, 12e9], [0, 4e12], [0, 5.8e12], [0, 12e9], [0, 40], [0, 1.975]],
                 img_background="./img/fig 4-1-1.png",
                 figsize=(7, 5),
                 title="World3 Referenze Run, 2004 Szenario 1")
"""

'''plot_world_variables(world3.time,
                 [world3.io, world3.f, world3.pop,
                  world3.ppolx, world3.nrfr],
                 ["IO", "F", "POP", "PPOLX", "NRFR"],
                 [[0, 4e12], [0, 5.8e12], [0, 12e9], [0, 40], [0, 1.975]],
                 img_background="./img/fig 4-1-1.png",
                 figsize=(7, 5),
                 title="Variation A, PyWorld3-05 run with improved parameters")
plt.savefig("PyWorld3-05 run with improved parameters.pdf")'''


"""
rs.plot_world_variables(world3.time,
                 [empirical_data["Population"], world3.io, world3.f, world3.pop,
                  world3.ppolx, world3.nr],
                 ["POPEMP", "IO", "F", "POP", "PPOLX", "NR"],
                 [[0, 12e9], [0, 4e12], [0, 5.8e12], [0, 12e9], [0, 40], [0, 2e12]],
                 img_background="./img/fig 4-1-1.png",
                 figsize=(7, 5),
                 title="World3 Referenze Run, 2004 Szenario 1", alpha = 1)
"""
'''plot_world_variables(world3.time,
                 [world3.le, world3.fpc, world3.sopc, world3.ciopc],
                 ["LE", "FPC", "SOPC", "CIOPC"],
                 [[0, 89], [0,999],[0,970], [0, 250]],
                 img_background="./img/fig 4-1-2.png",
                 figsize=(7, 5),
                 title="PyWorld3-05 run with improved parameters")'''

rs.plot_world_variables(world3.time,
                 [empirical_data['Ecological_Footprint'], world3.ef, empirical_data['Human_Welfare'], world3.hwi],
                 ["EF empirical", "EF model", "HWI empirical", "HWI model"],
                 [[0, 4], [0, 4], [0, 1], [0, 1]],
                 [1, 0.7, 1, 0.7],
                 img_background="exports/BAU_HWI-EF_Background-Picture.png",
                 figsize=(7, 5), title="Variation A, PyWorld3-03 run with improved parameters")
plt.savefig("exports/PyWorld3-03 run with improved parameters_ef hwi-own background.png")
#plt.show()
'''rs.plot_world_variables_black_linestyle(world3.time,
                                        [world3.io, world3.f, world3.pop,
                                         world3.ppolx, world3.nrfr],
                                        ["IO", "F", "POP", "PPOLX", "NRFR"],
                                        [[0, 4e12], [0, 5.8e12], [0, 12e9], [0, 40], [0, 1.975]],
                        [1,1,1,1],
                        ['solid', 'dotted', 'dashed', 'dashdot'],
                        figsize = (7, 5),
                        title = "PyWorld3-03 BAU - State of the World")
plt.savefig('exports/BAU_State_of_the_world.png')'''

'''rs.plot_world_variables_black_linestyle(world3.time,
                        [world3.le, world3.fpc, world3.sopc, world3.ciopc],
                        ["LE", "FPC", "SOPC", "CIOPC"],
                        [[0, 89], [0, 999], [0, 970], [0, 250]],
                        [1,1,1,1],
                        ['solid', 'dotted', 'dashed', 'dashdot'],
                        figsize = (7, 5),
                        title = "PyWorld3-03 BAU - Material Standard of Living")
plt.savefig('exports/BAU_Material_standard_of_living.png')'''

'''rs.plot_world_variables_black_linestyle(world3.time,
                                        [world3.ef,world3.hwi],
                                        ["EF", "HWI"],
                                        [[0, 4], [0, 1]],
                        [1,1],
                        ['solid', 'dotted'],
                        figsize = (7, 5),
                        title = "PyWorld3-03 BAU - HWI and EF")
plt.savefig('exports/BAU_HWI-EF.png')'''

#plt.show()




