def calculate_metrics(pyworld_data, real_data, sensivity_variable):
    """
    inputs are two arrays of the same size and a string for naming the datafram
    calculate Rate of Change, NRMSD (Branderhorst 2020)
    """
    # init variables für compare funktion
    d_value_list = []
    d_roc_list = []
    nrmsd_list = []
    n = len(pyworld_data)

    for year_n in np.arange(0, n, 5):
        # d_value
        d_value = (pyworld_data[year_n - 1] - real_data[year_n - 1]) / real_data[year_n - 1]
        d_value_list.append(d_value)
        d_value_sum = sum(d_value_list)

        # roc
        d_roc = (((pyworld_data[year_n - 1] - pyworld_data[year_n - 6]) - (
                    real_data[year_n - 1] - real_data[year_n - 6]))
                 / (real_data[year_n - 1] - real_data[year_n - 6]))
        d_roc_list.append(d_roc)
        d_roc_sum = sum(d_roc_list)

        # nrmsd
        nrmsd = (((((pyworld_data[year_n - 1] - real_data[year_n - 1]) ** 2) / 6)) ** (1 / 2)) / (
                    real_data[year_n - 1] / 6)
        nrmsd_list.append(nrmsd)
        nrmsd_sum = sum(nrmsd_list)

    results_dvalue = pd.DataFrame(data=d_value_sum, index=[sensivity_variable],
                                  columns=['d value'])
    results_droc = pd.DataFrame(data=d_roc_sum, index=[sensivity_variable],
                                columns=['d ROC'])
    results_nrmsd = pd.DataFrame(data=nrmsd_sum, index=[sensivity_variable],
                                 columns=['NRMSD'])

    results = pd.concat([results_dvalue, results_droc, results_nrmsd],
                        axis=1)

    return results
