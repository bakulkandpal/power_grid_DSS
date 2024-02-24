import pandas as pd
from math import asin
import numpy as np
from load_flow_function import perform_load_flow

line_data = pd.read_excel('line_33.xlsx')
load_data = pd.read_excel('load_data_33.xlsx')
network_parameters=[]



list_vol, a = perform_load_flow(network_parameters)


