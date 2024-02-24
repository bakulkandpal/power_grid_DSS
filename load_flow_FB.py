# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 12:14:39 2022

@author: rubir
"""





import pandas as pd
from math import asin
import numpy as np
import math
from numpy import  sqrt, real, imag, pi
from datafile import load_case
from numpy import inf
from scipy.sparse import dok_matrix, hstack
from  numpy import* 
from collections import OrderedDict


case = load_case('casecineldi124.m')  
Base_MVA=10
G = case.G
branches = case.branch_list
branches_data= case.branch_data_list
n = len(case.demands)
slots=24
nbranch=len(branches)
fbus_list=[]
tbus_list=[]

for i in range(nbranch):
    
    fbus,tbus=branches[i]
   
    fbus_list.append(fbus)
    tbus_list.append(tbus)

def branch_list_data_dict_combine(branches,branches_data):
        #Creating dictionary both with branch list and data        
        fulldict= {}
        for a,b in zip(branches, branches_data):
            fulldict[a]=b
        return (fulldict)    
fulldict= branch_list_data_dict_combine(branches,branches_data)         
  
def load_flow(branches,branches_data,t,active_load,reactive_load):
   
    n = len(case.demands)
     
    # Creating  demand  data dictionary  
    demand_data_dict ={}  
    
    for i in range(n):
    #print(i)
        demand_data_dict[i]=complex(active_load[i][t]/Base_MVA,reactive_load[i][t]/Base_MVA)
     
    itera=0
    key_list   = list(fulldict.keys())
    value_list = list(fulldict.values())
    z_list=[]
    for r,x in value_list:
      
      z=(complex((r),(x)))
      
      
      z_list.append(z)  
    full_dict_imp=dict(list(zip(key_list,z_list)))
    
    
    v=dok_matrix((n, 1),dtype=complex)
     
    for i in range(n):
       
        v[i]= complex(math.cos(0*pi/180),math.sin(0*pi/180))
    v_slack=v[0]
    
    eps=10
    while eps >0.01:
    
        value_list = list(demand_data_dict.values())
        
        division_list=[]
         
        for i in range(n):
                  d=list(v[i].values())
                 
                  division= value_list[i]/d[0]
                
                  division_list.append(division)
                 
         
            
         
        
        key_list   = list(demand_data_dict.keys())
        I_conj_list=[]
        for i in range(n):
            I_conj = conj(division_list[i])
            I_conj_list.append(I_conj)          
        
        
        
     
        a= {}
        
   
        for i in reversed(range(nbranch)):
          #print(i)
     
          conn = [item for item in range(len(fbus_list)) if fbus_list[item] == tbus_list[i]]
     
         
          a[i]=sum(a[c]    for c in conn      ) +I_conj_list[tbus_list[i]]  
    
       
        for i in reversed(range(nbranch)):
            
            v[fbus_list[i]]=v[ tbus_list[i] ] + a[i]*full_dict_imp[fbus_list[i],tbus_list[i] ]
          
        eps=abs(v[0]-v_slack)
        
        if eps<0.001:
            break
        
    
        v[0]=v_slack
        
        for i in range(nbranch):                     
                v[ tbus_list[i] ]=list(v[fbus_list[i]].values())[0]-a[i]*full_dict_imp[fbus_list[i],tbus_list[i] ]         
    return v,a
    

    
def loss_calculation(v,a):
        loss_list=[]
        for i in range(nbranch):                     
            
       
            loss=abs((list(v[fbus_list[i]].values())[0]-  list(v[tbus_list[i] ].values())[0])*a[i])
            loss_list.append(loss)
            f=abs(a[i])
            
        return loss_list  
    
class loadflow(object):
    pass


def case_powerflow(active_load,reactive_load,s):    
    list_vol=[]
    list_losses_hourly=[] 
    for t in range(slots):
        
        v_old_lines,a=load_flow(branches,branches_data,t,active_load,reactive_load)
        a_list_old=(list(v_old_lines.values())  )
    
        res =  [abs(ele) for ele in a_list_old]
    
        list_vol.append(res)
        
        loss_list      = loss_calculation(v_old_lines,a) # losses for each branches
        sum_loss_list=sum(loss_list)
        list_losses_hourly.append(sum_loss_list)  # saving hourly losses for whole network

    return list_vol ,list_losses_hourly    




    



    