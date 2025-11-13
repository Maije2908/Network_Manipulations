# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:56:46 2024

@author: christoph_m
"""

import skrf as rf
import network_manipulations as netman

if __name__ =='__main__':
        
    # define test files
    path = 'Examples/'
    
    ntwk_1 = rf.Network(path + 'exam_1.s4p') # 4-port, 4001 pnt
    ntwk_2 = rf.Network(path + 'exam_2.s4p') # 4-port, 4001 pnt
    ntwk_3 = rf.Network(path + 'exam_3.s4p') # 4-port, 3995 pnt
    ntwk_4 = rf.Network(path + 'exam_4.s2p') # 2-port, 4001 pnt
    ntwk_5 = rf.Network(path + 'exam_5.s4p') # empty
        
    # set or reset flags
    netman.set_showCMD() 
    
    netman.reset_showCMD()
    
    ### Example useages ###
    # calculate the normalized mean-square error of two network objects 
    # Flags control if answer is in dB or not
    NMSE_reflect, NMSE_transm = netman.calc_Sparam_NMSE(ntwk_1, ntwk_2, valuetype = 'dB')
 
    # store SParameters out of the network file in separate arrays
    number_ports, number_points, frequency, SParameter = netman.extract_Sparam(ntwk_4)
    
    # split up SParameters to desired ones
    SParameter_parts = netman.sliceSparam(['S11','S12'], SParameter)

    # print S-Parameters
    netman.plot_Sparam(frequency, SParameter_parts, number_ports, how='allinone',
                       spacing='log', valuetype='dB',
                       title='Single plot', xlabel='frequency (Hz)', ylabel='|S| dB',
                       legend='legon', legpos='best',
                       save = 'on', savename='single.png')

    netman.plot_Sparam(frequency, SParameter, number_ports, how='subplot',
                       spacing='log', valuetype='dB',
                       title='Many Subplots', xlabel='frequency (Hz)', ylabel='|S| dB',
                       legend='legon', legpos='best',
                       save='on', savename='subplot.png')    
    