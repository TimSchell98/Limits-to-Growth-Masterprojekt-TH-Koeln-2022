import pyworld3.agriculture as ag
import pyworld3.population as pop
import pyworld3.capital as cap

"""
agr = ag.Agriculture()
agr.set_agriculture_table_functions()
agr.init_agriculture_constants()
agr.init_agriculture_variables()
agr.set_agriculture_delay_functions()
agr.init_exogenous_inputs()
agr.run_agriculture()
"""

"""
pop = pop.Population()
pop.set_population_table_functions()
pop.init_population_constants()
pop.init_population_variables()
pop.init_exogenous_inputs()
pop.set_population_delay_functions()
pop.run_population()
"""

cap = cap.Capital()
cap.set_capital_table_functions()
cap.init_capital_variables()
cap.init_capital_constants()
cap.set_capital_delay_functions()
cap.init_exogenous_inputs()
cap.run_capital()

print('pyworld3_03 Update Version')