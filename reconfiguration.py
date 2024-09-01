# Basic network reconfiguration where one chosen branch or line is removed and another is added to see impact on voltages and current.
import pandas as pd
from math import asin
import numpy as np
import math
from numpy import  sqrt, real, imag, pi
from datafile import load_case
import matplotlib.pyplot as plt
from numpy import inf
from scipy.sparse import dok_matrix, hstack
from pyomo.environ import *
import networkx as nx
from collections import OrderedDict
from load_flow_reconfiguration import perform_load_flow

line_data = pd.read_excel('line_33.xlsx')  # Release 1.0.1
load_data = pd.read_excel('load_data_33.xlsx')
active_load=load_data['P (kW)']
reactive_load=load_data['Q (kW)']
case = load_case('case33bw.m')  

# Write both tuples (from bus, to bus) considering the order of how current is flowing or will flow after new connection.
line_to_remove = (1, 18)  # Choose line to remove. (from bus, to bus) (IEEE 33 bus - substation is bus 0)
line_to_add = (21, 32)   # Choose line to add (based on IEEE 33 bus)
new_line_impedance=(0.0307, 0.0156)  # (R,X) Impedance of the new line_to_add in Ohms


######################### Rest of code below
G = case.G
branches = case.branch_list
branches_data= case.branch_data_list
nbranch=len(branches)

Gt = nx.Graph()
Gt.add_edges_from(branches) # Original branches of network
Gt.remove_edge(*line_to_remove)
Gt.add_edge(*line_to_add)

original_line_to_add = line_to_add
reversed_line_to_add = original_line_to_add[::-1]

try:
    path_one = nx.shortest_path(Gt, 0, original_line_to_add[1])
    path_two = nx.shortest_path(Gt, 0, original_line_to_add[0])
    if original_line_to_add[0] in path_one: 
        line_to_add =  original_line_to_add
    elif original_line_to_add[1] in path_two:
        line_to_add =  reversed_line_to_add
except nx.NetworkXNoPath:
    print("No path")
    
branches_copy = branches.copy()
branches_data_copy = branches_data.copy()    
branches_copy.append(line_to_add)
branches_data_copy.append(new_line_impedance)

Base_KVA=10000
V_base=12.66  # In kV
Z_base=(V_base*1000)**2 / (Base_KVA * 1000)

## Convert branches_data to pu 
n = len(case.demands)

G = nx.Graph()
G.add_edges_from(branches) # Original branches of network

def check_radial_and_connected(graph, line_to_remove, line_to_add):
    temp_graph = graph.copy()
    temp_graph.remove_edge(*line_to_remove)  
    temp_graph.add_edge(*line_to_add)  
    
    # Check if the network is still a single connected graph and has no cycles to keep it radial.
    is_connected = nx.is_connected(temp_graph)
    has_no_cycles = not bool(list(nx.simple_cycles(temp_graph)))
    
    return is_connected, has_no_cycles

## Check radial and network connection
is_connected, has_no_cycles = check_radial_and_connected(G, line_to_remove, line_to_add)

print(f"Is the network still connected? {is_connected}")
print(f"Does the network have no cycles? {has_no_cycles}")

source = line_to_add[1]
target = line_to_remove[1]
try:
    path = nx.shortest_path(G, source, target)
    branches_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
except nx.NetworkXNoPath:
    print("No path found.")


new_branches_list = branches.copy()    
new_branches_list.remove(line_to_remove)
new_branches_list.append(line_to_add)

for branch in branches_in_path:
    if branch not in new_branches_list:
        new_branches_list.append(branch)
        
for branch in branches_in_path:
    reversed_branch = (branch[1], branch[0])
    if reversed_branch in new_branches_list:
        new_branches_list.remove(reversed_branch)
              
if line_to_add in new_branches_list:
    new_branches_list.remove(line_to_add)

for i, (from_bus, to_bus) in enumerate(new_branches_list):
    if from_bus == line_to_add[1]: 
        print(i)
        new_branches_list.insert(i, line_to_add)  
        break     
                 
sorted_branches = sorted(new_branches_list, key=lambda x: x[1])

new_branches_data = []  
for branch in new_branches_list:
    if branch in branches_copy:
        index = branches_copy.index(branch)  # Finding index of branch in branches_copy
    elif branch[::-1] in branches_copy:
        index = branches_copy.index(branch[::-1]) # Finding index of reversed branch in branches_copy
    corresponding_data = branches_data_copy[index]
    new_branches_data.append(corresponding_data)   # Reordering the branch impedance data based on new_branches_list


list_vol, a = perform_load_flow(new_branches_list, new_branches_data)  # Ideally the new_branch_list should have a particular (ascending) order.

plt.plot(list_vol[0], marker='o', linestyle='-', color='b') 
plt.xlabel('Bus No.')
plt.ylabel('Voltage [pu]')
plt.title('Voltages')
#plt.xticks(range(len(list_vol[0])), rotation=90)
plt.show()

I_base=Base_KVA/V_base  # In Amperes

current_absolute = {key: abs(value) for key, value in a.items()}
current_amperes = {key: value * I_base for key, value in current_absolute.items()}
current_values = list(current_amperes.values())

plt.plot(current_values, marker='o', linestyle='-', color='b') 
plt.xlabel('Branch No.')
plt.ylabel('Current [Amperes]')
plt.title('Branch Current')
#plt.xticks(range(len(list_vol[0])), rotation=90)
plt.show()