#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 14:40:57 2022

@author: ruben willamowski, alexander kling
"""

from pyworld3 import world3 as w3
from pyworld3.utils import plot_world_variables
from matplotlib.pyplot import rcParams, show


def reference_run():
    params = {'lines.linewidth': '3'}
    rcParams.update(params)

    world3 = w3.World3()
    world3.init_world3_constants()
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=True)

    plot_world_variables(world3.time,
                         [world3.nrfr, world3.iopc, world3.fpc, world3.pop,
                          world3.ppolx],
                         ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                         [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                         figsize=(7, 5),
                         grid=1,
                         title="Dynamics of Growth - Reference Run")
    show()

def doubled_resources():
    """Originally:
     Figure 36 WORLD MODEL WITH NATURAL RESOURCE
RESERVES DOUBLED """

    params = {'lines.linewidth': '3'}
    rcParams.update(params)

    world3 = w3.World3()
    world3.init_world3_constants(nri=2e12)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=True)

    plot_world_variables(world3.time,
                         [world3.nrfr, world3.iopc, world3.fpc, world3.pop,
                          world3.ppolx],
                         ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                         [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                         figsize=(7, 5),
                         grid=1,
                         title="World Model with Natural Resources doubled")
    show()

def unlimited_resources():
    """Originally: Figure 37 WORLD MODEL WITH  UNLIMITED RESSOURCES
    The Key Parameter here seems to be the nruf2, which is described on P.390 of Dynamics of Growth
    in a finite World (DGFW) """

    nruf2 = 0.7

    params = {'lines.linewidth': '3'}
    rcParams.update(params)

    world3 = w3.World3()
    world3.init_world3_constants(nri=2e12, nruf1=1, nruf2=nruf2)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=True)

    plot_world_variables(world3.time,
                         [world3.nrfr, world3.iopc, world3.fpc, world3.pop,
                          world3.ppolx],
                         ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                         [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                         figsize=(7, 5),
                         grid=1,
                         title="World Model with unlimited Natural Resources ----- Parameter nruf2 = {}".format(nruf2))
    show()

def unlimited_resources_pollution_control():
    """Originally: Figure 39 WORLD MODEL WITH UNLIMITED RESSOURCES AND POLLUTION CONTROL
    The Key Parameter here seems to be the ppgf2, which is described on P.428 of Dynamics of Growth
    in a finite World (DGFW) """

    nruf2 = 0.65
    ppgf2 = 0.25

    world3 = w3.World3()
    world3.init_world3_constants(nri=2e12, nruf1=1, nruf2=nruf2, ppgf2=ppgf2)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=True)

    plot_world_variables(world3.time,
                         [world3.nrfr, world3.iopc, world3.fpc, world3.pop,
                          world3.ppolx],
                         ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                         [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                         figsize=(7, 5),
                         grid=1,
                         title="World Model with unlimited Natural Resources and Pollution Control \nParameter: nruf2 = {}; ppgf2 = {}".format(
                             nruf2, ppgf2))
    show()

def unlimited_resources_pollution_control_increased_land_yield():
    """Originally: Figure 40 WORLD MODEL WITH "UNLIMITED" RESOURCES, POLLUTION CONTROLS, AND INCREASED
                                AGRICULTURAL PRODUCTIVITY
                Dynamics of Growth Figure: Run 7-16: resource, pollution, and land yield technologies
         """

    nruf2 = 0.6
    ppgf2 = 0.25
    lyf2 = 2

    world3 = w3.World3()
    world3.init_world3_constants(nri=2e12, nruf1=1, nruf2=nruf2, ppgf2=ppgf2, lyf2=lyf2)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=True)

    plot_world_variables(world3.time,
                         [world3.nrfr, world3.iopc, world3.fpc, world3.pop,
                          world3.ppolx],
                         ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                         [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                         figsize=(7, 5),
                         grid=1,
                         title="World Model with unlimited Natural Resources and Pollution Control \nParameter: nruf2 = {}; ppgf2 = {};lyf2 = {}".format(
                             nruf2, ppgf2,lyf2))
    show()

def stab_pop():
    """Originally:
     Figure 44 WORLD MODEL WITH STABILIZED PUPULATION """

    #zpgt=1970 #possibillity to smoth - not appropriate

    params = {'lines.linewidth': '3'}
    rcParams.update(params)

    world3 = w3.World3()
    world3.init_world3_constants(pet=1975)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=True)

    plot_world_variables(world3.time,
                         [world3.nrfr, world3.iopc, world3.fpc, world3.pop,
                          world3.ppolx],
                         ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                         [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                         figsize=(7, 5),
                         grid=1,
                         title="World Model with stabilized population")
    show()

def red_des_comp_fam_size():
    """DGFW: Figure 7-34 Run 7-24: reduction of the desired completed family size """

    params = {'lines.linewidth': '3'}
    rcParams.update(params)

    "Reduction of the Desired Completed Family Size DCFS"
    " zpgt : float, optional - time when desired family size equals 2 children [year]. The default is 4000. "

    world3 = w3.World3()
    world3.init_world3_constants(zpgt=1975)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=True)

    plot_world_variables(world3.time,
                         [world3.nrfr, world3.iopc, world3.fpc, world3.pop,
                          world3.ppolx],
                         ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                         [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                         figsize=(7, 5),
                         grid=1,
                         title="World Model with reduction of the desired completed family size")
    show()
    
def inc_of_ind_a_serv_cap_lt():
    """DGFW: Figure 7-35 Run 7-25: increase of industrial and service capital lifetimes """
    
    "alic2 : float, optional"
    "alic, value after time=pyear [years]. The default is 14."
    
    params = {'lines.linewidth': '3'}
    rcParams.update(params)

    world3 = w3.World3()
    world3.init_world3_constants(alic2=21, alsc2=30)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()
    world3.run_world3(fast=True)

    plot_world_variables(world3.time,
                         [world3.nrfr, world3.iopc, world3.fpc, world3.pop,
                          world3.ppolx],
                         ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                         [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                         figsize=(7, 5),
                         grid=1,
                         title="World Model with increase of industrial and service capital lifetimes ")
    show()


if __name__ == '__main__':
    #reference_run()
    #doubled_resources()
    #unlimited_resources()
    #unlimited_resources_pollution_control()
    #unlimited_resources_pollution_control_increased_land_yield()
    stab_pop()
    #red_des_comp_fam_size()
    #inc_of_ind_a_serv_cap_lt()
