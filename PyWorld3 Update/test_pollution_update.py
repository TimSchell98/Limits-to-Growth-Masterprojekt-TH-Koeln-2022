import pyworld3.pollution_update as po
from pyworld3.utils import plot_world_variables


pol = po.Pollution(pyear = 2050)
pol.set_pollution_table_functions()
pol.init_pollution_variables()
pol.init_pollution_constants()
pol.set_pollution_delay_functions()
pol.init_exogenous_inputs()
pol.run_pollution()

plot_world_variables(pol.time, [pol.pcrum, pol.io, pol.ppgi, pol.aiph, pol.ppga], ["PCRUM", "IO", "PPGI", "AIPH","PPGA"], [[0, 10], [7e10, 1e14],[5e6,3e9],[0,200],[0,3e8]], figsize=(7, 5), title="Pollution Variablen")

plot_world_variables(pol.time, [pol.ppgf, pol.ppgr, pol.ppar], ["PPGF", "PPGR", "PPAR"], [[0, 2], [1e13, 2e17],[3e13,2e17]], figsize=(7, 5), title="Pollution Variablen 2")

plot_world_variables(pol.time, [pol.pp, pol.ppolx, pol.ahlm], ["PP", "PPOLX", "AHLM"], [[2.5e7, 1e19], [2e4, 5e10],[0,50]], figsize=(7, 5), title="Pollution Variablen 3")

plot_world_variables(pol.time, [pol.ahl, pol.ppasr, pol.pptc], ["AHL", "PPASR", "PPTC"], [[1, 100], [1e7, 1e17],[-1e4,-4e10]], figsize=(7, 5), title="Pollution Variablen 4")

plot_world_variables(pol.time, [pol.pptcm, pol.pptcr, pol.ppt], ["PPTCM","PPTCR", "PPT"], [[0, -0.1], [-0.1, 0.2], [0,1.1]], figsize=(7, 5), title="Pollution Variablen 5")

plot_world_variables(pol.time, [pol.ppgf2, pol.pptmi, pol.pii], ["PPGF2","PPTMI","PII"], [[0,1.1],[0,1.3],[1e-7,2e-4]], figsize=(7, 5), title="Pollution Variablen 6")

plot_world_variables(pol.time, [pol.fio70, pol.ymap1,pol.ymap2], ["FIO70","YMAP1","YMAP2"], [[9e-2,2e2],[0,1.1],[0,1.1]], figsize=(7, 5), title="Pollution Variablen 7")

plot_world_variables(pol.time, [pol.apfay, pol.abl, pol.ef], ["APFAY","ABL","EF"], [[0,1.1],[1e5,6e8],[7e4,4e8]], figsize=(7, 5), title="Pollution Variablen 8")


print('pyworld3_03 Update Version')
