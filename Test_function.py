# -*- coding: utf-8 -*-
"""
last change: 13.11.2025
Author(s): Christoph Maier

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
    
    
    ### Example useages ###
    # calculate the normalized mean-square error of two network objects 
    # Flags control if answer is in dB or not
    NMSE_reflect, NMSE_transm = netman.calc_Sparam_NMSE(ntwk_1, ntwk_2, valuetype = 'dB')
 
    # store SParameters out of the network file in separate arrays
    key= ['Sdd11','Sdc11', 'Sdd12', 'Sdc12', 'Scd11', 'Scc11', 'Scd12', 'Scc12',
          'Sdd21', 'Sdc21', 'Sdd22', 'Sdc22', 'Scd21', 'Scc21', 'Scd22', 'Scc22']
    number_ports_1, number_points_1, frequency_1, SParameter_1 = netman.extract_MMparam(ntwk_1, key)
    
    number_ports_2, number_points_2, frequency_2, SParameter_2 = netman.extract_Sparam(ntwk_3)
    
    # split up SParameters to desired ones
    SParameter_parts = netman.slice_Sparam(['S11','S12'], SParameter_2)

    # print S-Parameters
    netman.plot_Sparam(frequency_1, SParameter_1, number_ports_1, how='allinone',
                       spacing='log', valuetype='dB',
                       title='Single plot', xlabel='frequency (Hz)', ylabel='|S| dB',
                       legend='legon', legpos='best',
                       save = 'on', savename='single.png')

    netman.plot_Sparam(frequency_1, SParameter_1, number_ports_1, how='subplot',
                       spacing='log', valuetype='dB',
                       title='Many Subplots', xlabel='frequency (Hz)', ylabel='|S| dB',
                       legend='legon', legpos='best',
                       save='on', savename='subplot.png')    
    
    netman.plot_comp_Sparam(frequency_1, SParameter_1, frequency_2, SParameter_2,
                            number_ports_1, how='subplot',
                            spacing='log', valuetype='dB',
                            title='Many Subplots', xlabel='frequency (Hz)', ylabel='|S| dB',
                            legend='legon', legpos='best',
                            save='on', savename='compplot.png')
    