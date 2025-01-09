import pandas as pd

# - - - - - Global  Settings

# number of simulations per zoom
grid_resolution = 10

# pro Jahr in Simulation
sim_time_step = 1

# year in which the simulation stops
year_max = 2022
year_max1 = year_max + 1

# year in which the simulation starts
year_min = 1900


# - Analysis Settings

# step size [years] for NRMSD calculation
calculation_interval = 1

# period [years] for calculation
calculation_period = 50

# import empiriical settings from excel
empirical_settings = pd.read_excel(
    'empirical_settings.xlsx', index_col='index', sheet_name='settings')

# if true, after all sims plot every result
plot_results = False
# if true, plot nrmsd curve
plot_nrmsd = False

# what variable should be improved
variable_to_improve = "NRMSD_total"

# how much should the start/end limits be from the default. 0.5 = 50%, 1 = 100%, 2 = 200%
parameter_divergence = 0.2

# how much the start and end value should move if edge value is reached
parameter_move_start_end_value = 0.2

# end conditions:
# if nrmsd doesnt improve by X end calibration
nrmsd_delta_end_condition = 1e-11
# if X zooms are completed, end calibration
analysis_number_end_condition = 3
