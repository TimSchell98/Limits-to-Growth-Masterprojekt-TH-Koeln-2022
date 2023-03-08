"""
Skript zum Erstellen des Vergleichsplots zwischen 3 Parametrierungen und den empirischen Daten

"""

from PyWorld3_Update.pyworld3 import World3
from pyworld3.utils import plot_world_variables
import result_plotting as rs
import matplotlib.pyplot as plt
import analysis_functions as af
import pandas as pd

params = {'lines.linewidth': '3', 'axes.labelsize': '12', 'xtick.labelsize': '10', 'ytick.labelsize': '10',
          'figure.autolayout': 'True'}
plt.rcParams.update(params)

empirical_data = af.initialize_empirical_data(True)

parameter_set_1 = pd.read_excel('Durchläufe/Größere Grid resolution/60/Analysis parameter_list_23_03_04_17_10.xlsx', index_col=0)
label1 = 'V1_main result'
parameter_set_2 = pd.read_excel('Durchläufe/NRI/Doppelte NRI/Analysis parameter_list_23_03_02_20_24.xlsx', index_col=0)
label2 = 'V2_doubled NRI'
parameter_set_3 = pd.read_excel('Durchläufe/Gewichtung/Alex_Gewichtung/Analysis parameter_list_23_03_03_01_10.xlsx', index_col=0)
label3 = 'V3_inverse weighting '

parameter_dict_1 = {}
for index, name in enumerate(parameter_set_1['name']):
    parameter_dict_1[name] = parameter_set_1['default'].iloc[index].item()

parameter_dict_2 = {}
for index, name in enumerate(parameter_set_2['name']):
    parameter_dict_2[name] = parameter_set_2['default'].iloc[index].item()

parameter_dict_3 = {}
for index, name in enumerate(parameter_set_3['name']):
    parameter_dict_3[name] = parameter_set_3['default'].iloc[index].item()

# standard run

w3_sr = World3(dt=1, pyear=4000, year_max=2100)
w3_sr.init_world3_constants()
w3_sr.init_world3_variables()
w3_sr.set_world3_table_functions()
w3_sr.set_world3_delay_functions()
w3_sr.run_world3(fast=False)

# 3x World 3 mit verschiedenen parametrierungen
w3_1 = World3(dt=1, pyear=4000, year_max=2100)
w3_1.init_world3_constants(**parameter_dict_1)
w3_1.init_world3_variables()
w3_1.set_world3_table_functions()
w3_1.set_world3_delay_functions()
w3_1.run_world3(fast=False)

w3_2 = World3(dt=1, pyear=4000, year_max=2100)
w3_2.init_world3_constants(**parameter_dict_2)
w3_2.init_world3_variables()
w3_2.set_world3_table_functions()
w3_2.set_world3_delay_functions()
w3_2.run_world3(fast=False)

w3_3 = World3(dt=1, pyear=4000, year_max=2100)
w3_3.init_world3_constants(**parameter_dict_3)
w3_3.init_world3_variables()
w3_3.set_world3_table_functions()
w3_3.set_world3_delay_functions()
w3_3.run_world3(fast=False)

rs.plot_world_variables_vc(w3_1.time,
                        [empirical_data["Population"], w3_1.pop, w3_2.pop, w3_3.pop, w3_sr.pop],
                        ["Empirical Data", label1, label2, label3, "2004 standard run"],
                        [[0, 12e9], [0, 12e9], [0, 12e9], [0, 12e9], [0, 12e9]],
                        [1, 0.7, 0.7, 0.7, 0.7],
                        grid=True,
                        figsize=(7, 5),
                        title="Version Comparison Population")
plt.savefig('exports/Variantenvergleich_Population.png')

#plt.show()


'''rs.plot_world_variables_vc(w3_1.time,
                        [empirical_data["Human_Welfare"], w3_1.hwi, w3_2.hwi, w3_3.hwi, w3_sr.hwi],
                        ["EMP", "V1", "V2", "V3", "V0"],
                        [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1]],
                        [1, 0.7, 0.7, 0.7, 0.7],
                        img_background="./img/fig 4-1-3.png",
                        figsize=(7, 5),
                        title="Version Comparison HWI")'''

rs.plot_world_variables_vc(w3_1.time,
                        [empirical_data["Human_Welfare"], w3_1.hwi, w3_2.hwi, w3_3.hwi, w3_sr.hwi],
                        ["Empirical data", label1, label2, label3, "2004 standard run"],
                        [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1]],
                        [1, 0.7, 0.7, 0.7, 0.7],
                        grid=True,
                        figsize=(7, 5),
                        title="Version Comparison HWI")

plt.savefig('exports/Variantenvergleich_HWI_ohne Hintergrund.png')
#plt.show()
