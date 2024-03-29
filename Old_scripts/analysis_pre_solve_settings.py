'''
Settings File for the Pre-Solver Script
'''
import analysis_parallel_settings as s

print_debug_messages = True
search_range_from_default = 0.25
grid_resolution = 8

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
name_dict_empirical_model = {
    'Population':'POP',
    'Arable_land':'AL',
    'Arable_land_pc':'',
    'Death_rate':'CDR',
    'Birth_rate':'CBR',
    '':'PPOL',
    'Food_per_capita_ve':'FPC'
# TO DO: alle Daten ergänzen
}

if __name__ == '__main__':
    print(name_dict_empirical_model['Population'])