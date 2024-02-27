import pandas as pd
from math import asin
import numpy as np
from load_flow_function import perform_load_flow
import matplotlib.pyplot as plt

line_data = pd.read_excel('line_33.xlsx')
load_data = pd.read_excel('load_data_33.xlsx')

def dict_to_list(input_dict):
    plot_list = []
    for label, value in input_dict.items():
        plot_list.append([value])
    return plot_list


########## For modelling network problems.

bus_no = [10, 15, 30]  # Choose bus numbers where load has to be increased
bus_factors = [1, 1, 1]  # Choose the multiplying factor by which load is increased.

network_parameters = {'bus_no': bus_no,'bus_load_factors': bus_factors}

list_vol, a = perform_load_flow(network_parameters)

plt.plot(list_vol[0], marker='o', linestyle='-', color='b') 
plt.xlabel('Bus No.')
plt.ylabel('Voltage [pu]')
plt.title('Voltages')
plt.show()


########## For modelling transformer overload.

total_P = load_data['P (kW)'].sum()
total_Q = load_data['Q (kW)'].sum()

total_KVA = np.sqrt(total_P**2 + total_Q**2)

print(f"Total KVA in Network: {total_KVA}")

########## Line Congestion

Base_KVA=10000
V_base=12.66  # In kV
I_base=Base_KVA/V_base  # In Amperes

current_absolute = {key: abs(value) for key, value in a.items()}
current_amperes = {key: value * I_base for key, value in current_absolute.items()}
current_values = list(current_amperes.values())
current_values.reverse()

plt.plot(current_values, marker='o', linestyle='-', color='b') 
plt.xlabel('Branch No.')
plt.ylabel('Current [Amperes]')
plt.title('Branch Current')
plt.show()