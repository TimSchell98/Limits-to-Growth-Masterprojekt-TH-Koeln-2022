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
    
        dcfsn = 3.800000e+00,
        hsid = 3.068586e+01,
        ieat = 2.792292e+00,
        len = 2.800000e+01,
        lpd = 2.766205e+01,
        mtfn = 9.580780e+00,
        rlt = 3.000000e+01, sad=2.041176e+01,
          ici = 2.100000e+11,
          sci = 1.440000e+11,
        lfpf = 8.728440e-01,
       lufdt = 1.205626e+01,
       icor1 = 3.000000e+00,
       scor1 = 9.410980e-01,
       alic1 = 1.400000e+01,
       alsc1 = 2.257800e+01,
      fioac1 = 4.300000e-01,
         ali = 8.912266e+08,
        pali = 2.300000e+09,
         lfh = 7.000000e-01,
        palt = 4.628749e+09,
          pl = 8.528600e-02,
       alai1 = 2.000000e+00,
        lyf1 = 1.000000e+00,
          sd = 4.524500e-02,
        uili = 5.380060e+06,
        alln = 1.187850e+03,
       uildt = 6.683900e-01,
      lferti = 6.000000e+02,
         ilf = 6.000000e+02,
        fspd = 1.650246e+00,
        sfpc = 2.131124e+02,
        pp19 = 2.090517e+07,
        imef = 1.064740e-01,
        imti = 2.903120e+00,
        frpm = 1.643500e-02,
        ghup = 4.000000e-09,
       faipm = 1.526000e-03,
        amti = 1.734027e+00,
        pptd = 8.898340e+01,
       ppgf1 = 1.817604e+00,
         nri = 9.966816e+11,
       nruf1 = 9.598640e-01
    
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
