"""
This file contains functions that each represents one of the runs of the world model that were presented in Limits to Growth


created by: A.K.
"""


from pyworld3 import world3 as w3
from pyworld3.utils import plot_world_variables
from matplotlib.pyplot import rcParams, show


def standard_run():
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
                         title="Limits to Growth standard run")
    show()

def doubled_resources():
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


if __name__ == '__main__':
    doubled_resources()
    standard_run()
