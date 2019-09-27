def assign_parameter_value(parameter):
    index = 0
    if parameter == 'Aquifer thickness[m]':
        index = 3
    elif parameter == 'Plume length[m]':
        index = 4
    elif parameter == 'Electron Donor[mg/l]':
        index = 7
    elif parameter == 'Electron Acceptor : O2[mg/l]':
        index = 8
    return index
