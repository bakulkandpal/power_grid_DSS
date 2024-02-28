# Network reconfiguration with given set of lines to add/remove and best reconfiguration chosen based on brute force search.
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

line_data = pd.read_excel('line_33.xlsx')
load_data = pd.read_excel('load_data_33.xlsx')
active_load=load_data['P (kW)']
reactive_load=load_data['Q (kW)']
case = load_case('case33bw.m')  

# Write lines_possible_remove tuples (from bus, to bus) considering the order of how current is flowing.
lines_possible_remove = [(5,25), (2,22), (1,18), (10,11), (29,30)] # Give set/tuples of lines that can be removed from network.
possible_new_lines = [(21, 32), (17, 24), (21, 17)]  # Give set/tuples of lines that can be added.
new_line_impedances = [(0.0307, 0.0156), (0.045, 0.020), (0.050, 0.025)]  # (R,X) Impedance of the new line_to_add in Ohms


######################### Rest of code below
Base_KVA=10000
V_base=12.66  # In kV
Z_base=(V_base*1000)**2 / (Base_KVA * 1000)
I_base=Base_KVA/V_base  # In Amperes
G = case.G
branches = case.branch_list
branches_data= case.branch_data_list
nbranch=len(branches)

branches_copy = branches.copy()
branches_data_copy = branches_data.copy()    

for line, impedance in zip(possible_new_lines, new_line_impedances):
    branches_copy.append(line)
    branches_data_copy.append(impedance)


## Convert branches_data to pu 
n = len(case.demands)

G = nx.Graph()
G.add_edges_from(branches) # Original branches of network

## Check radial and network connection
def check_radial_and_connected(graph, line_to_remove, line_to_add):
    temp_graph = graph.copy()
    temp_graph.remove_edge(*line_to_remove)  
    temp_graph.add_edge(*line_to_add)  
    
    # Check if the network is still a single connected graph and has no cycles, and so is radial
    is_connected = nx.is_connected(temp_graph)
    has_no_cycles = not bool(list(nx.simple_cycles(temp_graph)))
    
    return is_connected, has_no_cycles

successful_combinations = []   # All scenarios of removing and adding lines that are feasible. Creating the search space for reconfiguration.
for line_to_remove in lines_possible_remove:
    for line_to_add in possible_new_lines:
        is_connected, has_no_cycles = check_radial_and_connected(G, line_to_remove, line_to_add)       
        if is_connected and has_no_cycles:
            successful_combinations.append((line_to_remove, line_to_add))
            

results = []  
for line_to_remove, line_to_add in successful_combinations:
    
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
        
    G_temp = G.copy()  
    source = line_to_add[1]
    target = line_to_remove[1]
    
    try:
        path = nx.shortest_path(G_temp, source, target)
        branches_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]  # Branches between source and target above. Signifies new direction of branches
    except nx.NetworkXNoPath:
        print("No path found")
        continue

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

    # Inserting line_to_add just before the first occurrence where from_bus matches line_to_add[1]
    for i, (from_bus, to_bus) in enumerate(new_branches_list):
        if from_bus == line_to_add[1]: 
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
        
    list_vol, a = perform_load_flow(new_branches_list, new_branches_data)      
    results.append((list_vol, a))

for i, (voltages, _) in enumerate(results):
    plt.figure(figsize=(10, 6))
    plt.plot(voltages[0], marker='o', linestyle='-', label=f'Scenario {i}')
    plt.title(f'Voltage Profile for Scenario {i}')
    plt.xlabel('Bus No.')
    plt.ylabel('Voltage [p.u.]')
    plt.grid(True, axis ='x')
    plt.legend()
    plt.show()