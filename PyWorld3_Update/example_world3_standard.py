# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from pyworld3 import World3
from pyworld3.utils import plot_world_variables

params = {'lines.linewidth': '3'}
plt.rcParams.update(params)

"""
Choose Szenario:
    1: A Referenz Point
    2: More Abundant Nonrenewable Resources
    Mehr hinzufügen
"""
szenario = 2




if szenario == 1:

    world3 = World3(pyear = 4000, pyear_pp_tech = 4000, pyear_res_tech = 4000)
    world3.init_world3_constants()
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)

    plot_world_variables(world3.time,
                     [world3.nrfr, world3.io, world3.f, world3.pop,
                      world3.ppolx],
                     ["NRFR", "IO", "F", "POP", "PPOLX"],
                     [[0, 1.975], [0, 4e12], [0, 6e12], [0, 11e9], [-0.2, 26]],
                     img_background="./img/fig 4-1-1.png",
                     figsize=(7, 5),
                     title="World3 Referenze Run, 2004 Szenario 1")

    plot_world_variables(world3.time,
                     [world3.le, world3.fpc, world3.sopc],
                     ["LE", "FPC", "SOPC"],
                     [[2, 75], [0,1020],[0,1050]],
                     img_background="./img/fig 4-1-2.png",
                     figsize=(7, 5),
                     title="World3 Referenze Run - Material standard of living, 2004 Szenario 1")

    plot_world_variables(world3.time,
                     [world3.hef, world3.hwi],
                     ["HEF", "HWI"],
                     [[0.1, 2.4], [0,0.9]],
                     img_background="./img/fig 4-1-3.png",
                     figsize=(7, 5), title="World3 Referenze Run - Human Wellfare and Footprint, 2004 Szenario 1")

if szenario == 2:
    world3 = World3(pyear = 4000, pyear_pp_tech = 4000, pyear_res_tech = 4000)
    world3.init_world3_constants(nri=2e12)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=False)

    plot_world_variables(world3.time,
                     [world3.nrfr, world3.io, world3.f, world3.pop,
                      world3.ppolx],
                     ["NRFR", "IO", "F", "POP", "PPOLX"],
                     [[0, 1.975], [0, 4e12], [0, 6e12], [0, 11e9], [-0.2, 26]],
                     img_background="./img/fig 4-2-1.jpg",
                     figsize=(7, 5),
                     title="World3 More Resources, 2004 Szenario 2")

    plot_world_variables(world3.time,
                     [world3.le, world3.fpc, world3.sopc],
                     ["LE", "FPC", "SOPC"],
                     [[2, 75], [0,1020],[0,1050]],
                     img_background="./img/fig 4-2-2.jpg",
                     figsize=(7, 5),
                     title="World3 More Resources - Material standard of living, 2004 Szenario 2")

    plot_world_variables(world3.time,
                     [world3.hef, world3.hwi],
                     ["HEF", "HWI"],
                     [[0.1, 2.4], [0,0.9]],
                     img_background="./img/fig 4-2-3.jpg",
                     figsize=(7, 5), title="World3 More Resources - Human Wellfare and Footprint, 2004 Szenario 2")