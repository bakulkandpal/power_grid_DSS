import pandas as pd
from math import asin
import numpy as np
from load_flow_function import perform_load_flow
import matplotlib.pyplot as plt

line_data = pd.read_excel('line_33.xlsx')
load_data = pd.read_excel('load_data_33.xlsx')

bus_no = [10, 15, 30]  # Choose bus numbers where load has to be increased
bus_factors = [1, 1, 1]  # Choose the multiplying factor by which load is increased.

network_parameters = {'bus_no': bus_no,'bus_load_factors': bus_factors}

list_vol, a = perform_load_flow(network_parameters)

plt.plot(list_vol[0], marker='o', linestyle='-', color='b') 
plt.xlabel('Bus No.')
plt.ylabel('Voltage [pu]')
plt.show()