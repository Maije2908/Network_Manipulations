# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:56:46 2024

@author: christoph_m
"""

import skrf as rf
import network_manipulations as netman

if __name__ =='__main__':
        
    # define test files
    ntwk_1 = rf.Network('exam_1.s4p') # 4-port, 4001 pnt
    ntwk_2 = rf.Network('exam_2.s4p') # 4-port, 4001 pnt
    ntwk_3 = rf.Network('exam_3.s4p') # 4-port, 3995 pnt
    ntwk_4 = rf.Network('exam_4.s2p') # 2-port, 4001 pnt
    ntwk_5 = rf.Network('exam_5.s4p') # empty
        
    # set or reset flags
    netman.set_showCMD() 
    netman.set_showdB()
    
    netman.reset_showCMD()
    netman.reset_showdB()
    
    ### Example useages ###
    # calculate the normalized mean-square error of two network objects 
    # Flags control if answer is in dB or not
    NMSE_reflect, NMSE_transm = netman.CalcSParameterNMSE(ntwk_1, ntwk_2)
 
    