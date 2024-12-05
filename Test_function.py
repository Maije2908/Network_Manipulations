# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:56:46 2024

@author: christoph_m
"""

import skrf as rf
import numpy as np
import matplotlib.pyplot as plt

import SParam_Calculations as Scalc

if __name__ =='__main__':
        
    ntwk_1 = rf.Network('CMC_leer.s4p') # 4-port, 4001 pnt
    ntwk_2 = rf.Network('MSL_leer.s4p') # 4-port, 4001 pnt
    ntwk_3 = rf.Network('1A.s2p') # 2-port
    ntwk_4 = rf.Network('CMC_leer_mod.s4p') #4-port, 3995 pnt
    ntwk_5 = [] # empty
        
    ShowdB = 0
        
    Scalc.set_showCMD() 
    Scalc.set_showdB()

       
    a, b = Scalc.CalcSParameterNMSE(ntwk_1, ntwk_2)

    