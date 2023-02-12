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

world3 = World3(dt = 1, pyear = 4000, year_max = 2100)
world3.init_world3_constants(alai1 = 4.226, ali = 922858170.939, alln = 5282.032, alsc1 = 32.23, amti = 1.226, frpm = 0.017, ici = 198947627818.434,
                             ieat = 3.954, imef = 0.095, imti = 9.304, lferti = 570.392, lfpf = 0.753, mtfn = 11.631, nri = 1089680400241.070, nruf1 = 0.934, pali = 2910390968.145,
                             palt = 11418513098.391, pl = 0.082, ppgf1 = 0.707, sci = 158297265160.523, sd = 0.073, uildt = 0.516, faipm = 0.001, pp19 = 381.470)

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