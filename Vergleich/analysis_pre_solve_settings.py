'''
Settings File for the Pre-Solver Script
'''
import analysis_parallel_settings as s

print_debug_messages = True
search_range_from_default = 0.25
grid_resolution = 2

parameter_default_dict = {
    s.parameter1_name: s.parameter1_default,
    s.parameter2_name: s.parameter2_default,
    s.parameter3_name: s.parameter3_default
}

parameter_number_dict = {
    s.parameter1_name: 1,
    s.parameter2_name: 2,
    s.parameter3_name: 3
}
