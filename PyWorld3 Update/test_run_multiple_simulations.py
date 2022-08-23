# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from xlwt import Workbook
from pyworld3 import World3
from pyworld3.utils import plot_world_variables

import time
startTime = time.time()

#Excel sheets für jede Variable die verglichen werden sollen
wb = Workbook()
var = wb.add_sheet("Eingangsparameter")
pop = wb.add_sheet("Population")
d = wb.add_sheet("Death per Year")
b = wb.add_sheet("Birth per Year")
fpc = wb.add_sheet("Food per Capita")
ef = wb.add_sheet("Ecological Footprint")
hwi = wb.add_sheet("Human Welfare Index")

#berechnen der eingangsparameter "sprünge"
sim_anzahl = 10
start_val = 3
end_val = 4
delta = (end_val-start_val)/sim_anzahl

#eingangs Variablen die verändert werden sollen
def dcfsn_f(i, sim_anzahl):
    
    #hier können wir eine funktion einfügen die die eingangs parameter berechnen, dieser wird auch in der excel geschrieben
    var.write(i+1, 0, start_val+i*delta)
    return start_val+i*delta

"""
params = {'lines.linewidth': '3'}
plt.rcParams.update(params)
"""

#ausgelagerte initierung für die verbesserung der Laufzeit
world3 = World3(dt = 1)

for i in range(0,sim_anzahl):
    print("\nSimulation" , end =": ")
    print(i+1)
    print("ETA", end =": ")
    print(round((sim_anzahl-i)*2.8,2), end = "")
    print("s")

    #simulation durchführen
    world3.init_world3_constants(dcfsn = dcfsn_f(i, sim_anzahl))
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)
    
    """
    plot_world_variables(world3.time,
                     [world3.nrfr, world3.io, world3.f, world3.pop,
                      world3.ppolx],
                     ["NRFR", "IO", "F", "POP", "PPOLX"],
                     [[0, 1.975], [0, 4e12], [0, 6e12], [0, 12e9], [0, 40]],
                     img_background="./img/fig 4-1-1.png",
                     figsize=(7, 5),
                     title="World3 Referenze Run, 2004 Szenario 1. Simulation")
    """
    
    #alle Werte der Vergleichsvariablen in Excel schrieben
    for y in range(0,200):
        pop.write(y+1, i+1, world3.pop[y])
        d.write(y+1, i+1, world3.d[y])
        b.write(y+1, i+1, world3.b[y])
        fpc.write(y+1, i+1, world3.fpc[y])
        ef.write(y+1, i+1, world3.ef[y])
        hwi.write(y+1, i+1, world3.hwi[y])

#excel speichern
wb.save('sim-values.xls')

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
