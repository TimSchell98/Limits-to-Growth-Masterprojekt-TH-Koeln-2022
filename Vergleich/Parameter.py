import pandas as pd


class Parameter:
    """
    Class Parameter for unifying all Parameter relevant Settings in one Datatype.
    """
    def __init__(self, name, default_value, standard_variation=True, start_value='', end_value=''):
        self.name = name
        self.default_value = default_value
        self.use_standard_variation = standard_variation
        self.start_value = start_value
        self.end_value = end_value

    def set_start_value(self, start_value):
        self.start_value = start_value

    def set_end_value(self, end_value):
        self.end_value = end_value

    def init_start_end_value(self, divergence):
        if self.default_value - self.default_value * divergence < 0:
            self.set_start_value(0)
        else:
            self.set_start_value(self.default_value - self.default_value * divergence)
        self.set_end_value(self.default_value + self.default_value * divergence)




if __name__ == '__main__':
    parameter_list = pd.read_excel('Parameter.xlsx')
    print(parameter_list)

    for p in range(len(parameter_list)):
        param_obj = Parameter(parameter_list['name'].loc[p],parameter_list['default'].loc[p], parameter_list['standard'].loc[p])
        obj_name = 'param_{}'.format(param_obj.name)
        vars()[obj_name] = param_obj



    print('Testing Class Parameter')