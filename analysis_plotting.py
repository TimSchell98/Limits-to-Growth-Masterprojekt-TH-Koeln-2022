import pandas as pd
from matplotlib import pyplot as plt
import analysis_parallel_settings as s
xticks = [0, 30, 60, 90, 120]
xticks_labels = [1900, 1930, 1960, 1990, 2020]

def plot_data(model_results, empirical_data, parameter_list_full):
    #   -   -   - Plot data -   -   -

    #ToDo: Einheiten an die y-labels schreiben
    #   Achsen teilweise aufteilen und die ylimits verbessern (FossilFuel Consumption)
    #   Plot Titel Aussagekräftiger machen
    #plot population
    for i in range(0, parameter_list_full.shape[0]):
        model_results['pop_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["Population"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Population')
    plt.ylim([1e9, 10e9])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    plt.ylabel(s.empirical_settings['pyworld_unit']['Population'])
    plt.show()

    

    # plot food per capita
    for i in range(0, parameter_list_full.shape[0]):
        model_results['fpc_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["Food_per_capita_ve"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Food per Capita')
    plt.ylim([0, 1000])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    plt.ylabel(s.empirical_settings['pyworld_unit']['Food_per_capita_ve'])
    plt.show()

    # plot food per capita proportion
    for i in range(0, parameter_list_full.shape[0]):
         model_results['fpcp_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["Food_per_capita_proportion"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Food per Capita proportion')
    #plt.ylim([-0.05, 0.05])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    #plt.ylabel(s.empirical_settings['pyworld_unit']['Food_per_capita_ve'])
    plt.show()

    # plot Pollution_proportion
    
    #label=s.empirical_settings.loc[attribute, 'pyworld_name_complete'] + " ["+s.empirical_settings.loc[attribute, 'pyworld_unit'] + "]"
    
    for i in range(0, parameter_list_full.shape[0]):
        model_results['pp_dtp_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["Pollution_proportion"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Pollution proportion')
    plt.ylim([-1, 2])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    #plt.ylabel(s.empirical_settings['pyworld_unit']['-']) #geht nicht
    plt.show()

    # plot Expected_years_of_schooling_proportion
    for i in range(0, parameter_list_full.shape[0]):
        model_results['sopcp_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["Expected_years_of_schooling_proportion"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Service proportion')
    plt.ylim([-0.1, 0.1])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    plt.ylabel('')
    plt.show()

    # plot IPP
    for i in range(0, parameter_list_full.shape[0]):
        model_results['iop_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["IPP_proportion"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Industrial Output proportion')
    plt.ylim([-0.40, 0.40])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    plt.ylabel('')
    plt.show()
    
    # plot Fossil_fuel_consumption_proportion
    for i in range(0, parameter_list_full.shape[0]):
        model_results['nrurp_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["Fossil_fuel_consumption_proportion"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Resources proportion')
    plt.ylim([-0.25, 0.25])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    plt.ylabel('')
    plt.show()

    # plot EF
    for i in range(0, parameter_list_full.shape[0]):
        model_results['ef_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["Ecological_Footprint"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Ecological Footprint')
    plt.ylim([0, 5])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    plt.ylabel('Hectars')
    plt.show()

    # plot HWI
    for i in range(0, parameter_list_full.shape[0]):
        model_results['hwi_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["Human_Welfare"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Human Welfare Index')
    plt.ylim([0, 1])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    plt.ylabel('HWI')
    plt.show()
    
    """
    # plot death rate
    for i in range(0, parameter_list_full.shape[0]):
        model_results['cdr_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["Death_rate"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Death Rate')
    plt.ylim([5, 25])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    plt.ylabel(s.empirical_settings['pyworld_unit']['Death_rate'])
    plt.show()

    # plot birth rate
    for i in range(0, parameter_list_full.shape[0]):
        model_results['cbr_{}'.format(i)].plot(legend=0, color=["b"], linewidth=0.4)
    empirical_data["Birth_rate"].plot(legend=0, color=["r"], linewidth=1.5)
    plt.title('Birth Rate')
    plt.ylim([5, 55])
    plt.xlim([0, 122])
    plt.xticks(ticks=xticks, labels=xticks_labels)
    plt.xlabel('Year')
    plt.ylabel(s.empirical_settings['pyworld_unit']['Birth_rate'])
    plt.show()
    """